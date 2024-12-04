# MAC Spoofer

## Overview
The MAC Spoofer is a cross-platform Python script designed to change or revert the Media Access Control (MAC) address of a network interface. It is a useful tool for enhancing privacy, bypassing network restrictions, or conducting authorized security testing.

This script supports Linux, macOS, and Windows systems, with features like MAC address validation, random MAC generation, and encrypted logging of actions.

---

## Features
- Detect and display the current MAC address of a network interface.
- Change the MAC address to a user-defined or randomly generated one.
- Revert to the original MAC address.
- Log changes to an encrypted file for security and auditing.
- Cross-platform support (Linux, macOS, and Windows).

---

## Requirements
- Python 3.x
- Root or administrative privileges to modify network settings.

---


## Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/Mac-Address-Spoofer.git
cd Mac-Address-Spoofer
```
3. Install dependencies:
```bash
pip install cryptography
```
---

## Usage
Run the Script:
```bash
python3 Mac_spoofer.py
```
---

 ## Logs
All MAC address changes are logged to an encrypted file named Mac_spoofer_encrypted.txt for auditing purposes. Each entry includes:
- Timestamp
- Interface name
- Original MAC address
- New MAC address
The log is encrypted using the Fernet module from the cryptography library.

---

## Cross-Platform Compatibility
The script detects the platform and adapts commands accordingly:
- Linux/macOS: Uses ifconfig for network configuration.
- Windows: Uses netsh for managing interfaces.

---

## Disclaimer
This tool is for educational purposes and authorized testing only. Misuse of this tool for illegal or unethical activities is strictly prohibited.

---

## Author
- Rahma Yaqeen
- LinkedIn: https://linkedin.com/in/fameera-yakeen 
- Email: famirapt@gmail.com

---

## Contribution
Feel free to fork the repository, open issues, or submit pull requests to enhance the functionality or compatibility of the tool.

