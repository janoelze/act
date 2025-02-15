# /// script
# command = "vpntoggle"
# description = "Toggle VPN connection using OpenVPN"
# aliases = ["vpntoggle"]
# author = "janoelze"
# dependencies = ["pyotp==2.9.0"]
# ///

# How to use:
# 1. Set the following environment variables:
#    - VPN_USERNAME: Your VPN username
#    - VPN_SECRET_KEY: Your VPN secret key
#    - VPN_CONFIG_PATH: Path to your OpenVPN config file
# 2. Run the script to toggle the VPN connection

import pyotp
import subprocess
import os
import re
import time
import platform
import fcntl

LOCK_FILE = "/tmp/vpn_toggle.lock"

def get_vpn_token(secret_key):
    """Generate a TOTP token using the given secret key."""
    totp = pyotp.TOTP(secret_key)
    return totp.now()

def vpn_connected(config_path):
    """Check if the VPN connection related to the config is active."""
    try:
        result = subprocess.run(["pgrep", "-f", config_path], capture_output=True, text=True)
        return bool(result.stdout.strip())
    except Exception as e:
        print(f"Failed to check VPN connection: {e}")
        return False

def disconnect_vpn(config_path):
    """Disconnect the VPN by killing the process running with the given config."""
    print("VPN is connected. Disconnecting...")
    try:
        # Kill only the openvpn instance with the target config
        subprocess.run(["sudo", "pkill", "-f", config_path], check=True)
        time.sleep(2)
        print("VPN disconnected.")
    except subprocess.CalledProcessError:
        print("Failed to disconnect VPN. It may already be disconnected.")

def connect_vpn(secret_key, username, config_path):
    """Connect to VPN using provided credentials."""
    token = get_vpn_token(secret_key)

    # Prepare credentials file
    creds_file = "/tmp/vpn_creds.txt"
    with open(creds_file, "w") as f:
        f.write(f"{username}\n{token}")

    os.chmod(creds_file, 0o600)

    # Run OpenVPN
    command = [
        "sudo", "openvpn",
        "--config", config_path,
        "--auth-user-pass", creds_file,
        "--verb", "7",
        "--auth-nocache"
    ]

    print("Connecting to VPN...")
    subprocess.Popen(command)

    time.sleep(5)  # Give it time to establish the connection
    os.remove(creds_file)

def toggle_vpn():
    """Toggle VPN connection."""
    # Acquire lock to prevent concurrent runs
    with open(LOCK_FILE, "w") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)

            username = os.environ.get("VPN_USERNAME")
            secret_key = os.environ.get("VPN_SECRET_KEY")
            config_path = os.environ.get("VPN_CONFIG_PATH")

            if not all([username, secret_key, config_path]):
                raise ValueError("Missing required environment variables: VPN_USERNAME, VPN_SECRET_KEY, VPN_CONFIG_PATH")

            print(f"Checking VPN status for config: {config_path}")

            if vpn_connected(config_path):
                disconnect_vpn(config_path)
            else:
                connect_vpn(secret_key, username, config_path)

        except BlockingIOError:
            print("Another instance of the script is already running. Exiting.")
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)

if __name__ == "__main__":
    toggle_vpn()