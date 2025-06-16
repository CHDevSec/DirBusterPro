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
