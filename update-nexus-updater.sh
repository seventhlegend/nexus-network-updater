#!/bin/bash

set -e

REPO_URL="https://github.com/YOUR_USERNAME/nexus-updater.git"
INSTALL_DIR="/opt/nexus-updater"
SERVICE_NAME="nexus-updater"

echo "🛑 Stopping systemd service if running..."
sudo systemctl stop ${SERVICE_NAME}.timer || true
sudo systemctl disable ${SERVICE_NAME}.timer || true

echo "🧹 Removing old installation..."
sudo rm -rf $INSTALL_DIR

echo "📥 Cloning latest version from GitHub..."
sudo git clone $REPO_URL $INSTALL_DIR

echo "⚙️ Installing fresh..."
cd $INSTALL_DIR
sudo bash install.sh

echo "🚀 Restarting timer..."
sudo systemctl start ${SERVICE_NAME}.timer
sudo systemctl enable ${SERVICE_NAME}.timer

echo "✅ Fully updated and reinstalled."
