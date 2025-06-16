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
git clone https://github.com/caio-henrique/dirbypasspro.git
cd dirbypasspro

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




