#!/usr/bin/env python3
# nexus_updater.py
# 
# This file is part of the Nexus Updater project.
# Copyright (C) 2025 SeventhLegend
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import os
import subprocess
import time
import logging
import requests

# Config
RELEASES_URL = "https://api.github.com/repos/nexus-xyz/nexus-cli/releases/latest"
LOG_FILE = "/opt/nexus-updater/error.log"
SCREEN_NAME = "nexus"

# Logger: only log WARNING and ERROR
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


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
        logging.warning(f"Could not determine installed version: {e}")
        return None


def kill_all_nexus_screens():
    try:
        result = subprocess.run(["screen", "-ls"], capture_output=True, text=True, check=True)
        lines = result.stdout.strip().splitlines()
        for line in lines:
            if f".{SCREEN_NAME}" in line:
                session_id = line.strip().split("\t")[0]
                logging.warning(f"Killing screen session: {session_id}")
                subprocess.run(["screen", "-S", session_id, "-X", "quit"], check=True)
        time.sleep(2)
    except Exception as e:
        logging.error(f"Failed to kill existing screen sessions: {e}")


def install_cli():
    try:
        subprocess.run("curl https://cli.nexus.xyz/ | sh", shell=True, check=True)
    except Exception as e:
        logging.error(f"CLI installation failed: {e}")
        raise


def start_fresh_nexus_screen():
    try:
        subprocess.run(["screen", "-S", SCREEN_NAME, "-d", "-m"], check=True)
        time.sleep(1)
        subprocess.run(["screen", "-S", SCREEN_NAME, "-X", "stuff", "nexus-cli start\n"], check=True)
        time.sleep(1)
        subprocess.run(["screen", "-S", SCREEN_NAME, "-X", "stuff", "\001d"], check=True)  # Ctrl+A D
    except Exception as e:
        logging.error(f"Failed to start fresh screen: {e}")
        raise


def main():
    try:
        latest = get_latest_version()
        current = get_installed_version()

        if latest == current:
            return  # No update needed

        kill_all_nexus_screens()
        install_cli()
        start_fresh_nexus_screen()

    except Exception as e:
        logging.error(f"Update process failed: {e}")


if __name__ == "__main__":
    main()
