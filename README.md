# 🔍 DirBypassPro - Advanced Directory Bypass Tester

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub Issues](https://img.shields.io/github/issues/caio-henrique/dirbypasspro.svg)](https://github.com/caio-henrique/dirbypasspro/issues)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/caio-henrique/dirbypasspro/graphs/commit-activity)

> **Professional tool for testing directory traversal bypasses and access control vulnerabilities**

## 📋 Table of Contents
- [Features](#-features)
- [Installation](#-installation)
- [Basic Usage](#-basic-usage)
- [Advanced Options](#-advanced-options)
- [Bypass Techniques](#-bypass-techniques)
- [Reports](#-reports)
- [Examples](#-examples)
- [Disclaimer](#-disclaimer)
- [License](#-license)

## 🚀 Features

### 🔥 Core Functionality
| Feature | Description |
|---------|-------------|
| **Multi-threading** | Scan with up to 50 concurrent threads |
| **Smart Detection** | Compare responses (status, size, content hash) |
| **Session Management** | Persistent connections with auth support |
| **Proxy Support** | SOCKS/HTTP/HTTPS proxy integration |

### 🛡️ Bypass Techniques
```python
# Path Manipulation Examples
/admin        → /admin%20
/restricted   → /restricted//
private      → /private%00
```

## 📊 Output Formats
# Supported Formats
- HTML (visual report)
- JSON (machine readable)
- CSV (spreadsheet compatible)


## 🛠️ Installation
### Prerequisites
```
# Verify Python version
python3 --version  # Requires 3.7+
```

## Installation Steps
# Clone repository
git clone https://github.com/caio-henrique/DirBusterPro.git
cd DirBusterPro

# Install dependencies
pip install -r requirements.txt

### Requirements
requests>=2.25.1
urllib3>=1.26.0


## 🎯 Basic Usage

```
python3 dirbypasspro.py <TARGET_URL> <WORDLIST> [OPTIONS]
```

## Example Scan
```
python3 dirbypasspro.py http://example.com/admin paths.txt -t 30 -o report.html
```

## ⚙️ Advanced Options
```
Option	Description	Default
-t	Threads count	20
-o	Output file	None
--proxy	Proxy URL	None
--auth	HTTP Basic Auth (user:pass)	None
--timeout	Request timeout	10
-v	Verbose mode	False
```

## 🔧 Bypass Techniques
### Path Variations
```
[
    "/admin",             # Original
    "/admin/",            # Trailing slash
    "/admin//",           # Double slash
    "/admin%20",          # URL encoded space
    "/admin%00",          # Null byte
    "/admin..;/",         # Path traversal
    "/admin~1",           # Short filename
    "/.%2fadmin"          # Dot slash
]
```

### Header Injection
```
{
    "X-Original-URL": "/admin",
    "X-Rewrite-URL": "/admin",
    "X-Forwarded-Host": "localhost",
    "X-Custom-IP-Authorization": "127.0.0.1"
}
```

## 📊 Report Samples
### **HTML Report Preview**

<div class="vulnerability">
  <h3>Bypass Found!</h3>
  <p><strong>Payload:</strong> /admin%2f%2e%2e</p>
  <p><strong>Status:</strong> 200 (OK)</p>
</div>

### CSV Output
```
time,method,payload,url,status,size,bypass
2023-01-01T12:00:00,GET,/admin%00,http://test.com/admin%00,200,1245,True
```

## 💡 Usage Examples

### Example 1: Basic Scan
```
python3 dirbypasspro.py http://vuln-site.com/private common_paths.txt
```

### Example 2: With Proxy
```
python3 dirbypasspro.py http://intranet/admin paths.txt --proxy socks5://127.0.0.1:9050
```

### Example 3: Full Audit
```
python3 dirbypasspro.py https://secure.com/panel admin_paths.txt \
  -t 50 \
  --auth admin:Password123 \
  --ignore-ssl \
  -o full_audit.html
```

## ⚠️ Legal Disclaimer

This tool was developed for educational purposes and authorized security testing. The use of this tool is entirely the user's responsibility. Make sure you have explicit authorization before testing any system.

### Responsible Use

- ✅ Test only on your own systems or with explicit authorization
- ✅ Respect the terms of service of the APIs used
- ✅ Use rate limiting to avoid server overload
- ❌ Do not use for malicious or illegal activities

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

### 🔒 Developed by [CHDEVSEC](https://github.com/chdevsec) | Pentester Caio

**⭐ If this project was useful to you, consider giving it a star!**

[![GitHub followers](https://img.shields.io/github/followers/chdevsec.svg?style=social&label=Follow)](https://github.com/chdevsec)

</div>

## 📚 Tags and Keywords

`pentest` `reconnaissance` `subdomain-enumeration` `vulnerability-scanner` `bug-bounty` `cybersecurity` `web-security` `ethical-hacking` `security-testing` `python` `automation` `google-dorking` `dns-enumeration` `web-fuzzing` `security-audit` `information-gathering` `osint` `red-team` `penetration-testing` `security-tools` `recon` `subdomain-discovery` `web-reconnaissance` `pentesting-tools` `security-scanner` `vulnerability-assessment` `web-application-security` `subdomain-takeover` `directory-bruteforce` `sensitive-file-detection`

