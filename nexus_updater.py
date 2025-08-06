#!/usr/bin/env python3
import os
import subprocess
import time
import logging
import requests

# Config
RELEASES_URL = "https://api.github.com/repos/nexus-xyz/nexus-cli/releases/latest"
LOG_FILE = "/opt/nexus-updater/updater.log"
SCREEN_SESSION = "nexus"

# Logger
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def get_latest_version():
    try:
        res = requests.get(RELEASES_URL, timeout=10)
        res.raise_for_status()
        return res.json()["tag_name"].lstrip("v")
    except Exception as e:
        logging.error(f"GitHub API error: {e}")
        raise


def get_installed_version():
    try:
        result = subprocess.run(["nexus-cli", "-V"], capture_output=True, text=True, check=True)
        return result.stdout.strip().split()[-1]
    except Exception as e:
        logging.warning(f"Could not determine local version: {e}")
        return None


def stop_screen():
    logging.info("Stopping screen session...")
    try:
        subprocess.run(["screen", "-S", SCREEN_SESSION, "-p", "0", "-X", "stuff", "Q\n"], check=True)
        time.sleep(1)
        subprocess.run(["screen", "-S", SCREEN_SESSION, "-p", "0", "-X", "stuff", "\003"], check=True)
        time.sleep(5)
    except Exception as e:
        logging.warning(f"Could not stop screen session: {e}")


def install_cli():
    logging.info("Installing latest nexus-cli...")
    subprocess.run("curl https://cli.nexus.xyz/ | sh", shell=True, check=True)


def start_screen():
    subprocess.run(["screen", "-S", SCREEN_SESSION, "-d", "-m", "nexus-cli", "start"], check=True)
    time.sleep(2)
    subprocess.run(["screen", "-S", SCREEN_SESSION, "-X", "stuff", "\001d"], check=True)


def main():
    try:
        latest = get_latest_version()
        current = get_installed_version()
        logging.info(f"Installed: {current}, Latest: {latest}")

        if latest == current:
            logging.info("Already up-to-date.")
            return

        stop_screen()
        install_cli()
        start_screen()
        logging.info(f"✅ Updated to {latest} and restarted.")
    except Exception as e:
        logging.error(f"❌ Update failed: {e}")


if __name__ == "__main__":
    main()
