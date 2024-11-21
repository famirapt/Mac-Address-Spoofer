import subprocess
import re
import random
import sys
import platform
import time
import threading
from datetime import datetime
from cryptography.fernet import Fernet

# Check if platform is supported
if platform.system() not in ["Linux", "Darwin", "Windows"]:
    print("[-] Unsupported platform. This script only works on Linux, macOS, and Windows.")
    sys.exit(1)

# Generate a key for encrypting the MAC history log
# Only generate this key once and store it securely
key = Fernet.generate_key()
cipher_suite = Fernet(key)

def validate_interface(interface):
    """Validate the interface name."""
    if not re.match(r"^[a-zA-Z0-9]+$", interface):
        print("[-] Invalid interface name. Please enter a valid interface.")
        sys.exit(1)

def validate_mac(mac):
    """Validate the MAC address format."""
    if not re.match(r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$", mac):
        print("[-] Invalid MAC address format. Please try again.")
        sys.exit(1)

def get_current_mac(interface):
    """Gets the current MAC address of the specified interface."""
    validate_interface(interface)
    try:
        if platform.system() == "Linux" or platform.system() == "Darwin":
            result = subprocess.check_output(["ifconfig", interface]).decode("utf-8")
            mac_address = re.search(r"(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)", result).group(0)
        elif platform.system() == "Windows":
            result = subprocess.check_output(f"getmac /v /fo list | findstr {interface}", shell=True).decode("utf-8")
            mac_address = re.search(r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})", result).group(0)
        return mac_address
    except:
        print(f"[-] Could not read MAC address for {interface}. Please check the interface name.")
        sys.exit(1)

def get_random_mac():
    """Generates a random MAC address."""
    return "02:%02x:%02x:%02x:%02x:%02x" % (
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff),
    )

def change_mac(interface, new_mac):
    """Changes the MAC address of the network interface."""
    validate_interface(interface)
    validate_mac(new_mac)
    if platform.system() == "Linux" or platform.system() == "Darwin":
        subprocess.call(["sudo", "ifconfig", interface, "down"])
        subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
        subprocess.call(["sudo", "ifconfig", interface, "up"])
    elif platform.system() == "Windows":
        subprocess.call(f"netsh interface set interface {interface} disable", shell=True)
        subprocess.call(f"netsh interface set interface {interface} newmac={new_mac}", shell=True)
        subprocess.call(f"netsh interface set interface {interface} enable", shell=True)

def log_action(interface, original_mac, new_mac):
    """Logs MAC address changes to an encrypted file."""
    log_entry = f"{datetime.now()} - Interface: {interface}, Original MAC: {original_mac}, New MAC: {new_mac}\n"
    encrypted_log_entry = cipher_suite.encrypt(log_entry.encode())
    with open("Mac_spoofer_encrypted.txt", "ab") as log_file:
        log_file.write(encrypted_log_entry + b"\n")
    print("[+] Action logged and encrypted.")

def main():
    interface = input("Enter the network interface (e.g., eth0, en0, Wi-Fi): ").strip()
    original_mac = get_current_mac(interface)
    print(f"[+] Current MAC address of {interface} is: {original_mac}")

    choice = input("Do you want to (1) Change MAC address, or (2) Revert to original MAC address? Enter 1 or 2: ").strip()

    if choice == "1":
        new_mac = get_random_mac()
        change_mac(interface, new_mac)
        print(f"[+] MAC address changed to {new_mac}")
        log_action(interface, original_mac, new_mac)
    elif choice == "2":
        change_mac(interface, original_mac)
        print(f"[+] MAC address reverted to original: {original_mac}")
        log_action(interface, original_mac, original_mac)
    else:
        print("[-] Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
