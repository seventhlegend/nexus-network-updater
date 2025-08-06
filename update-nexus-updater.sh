#!/bin/bash

set -e

REPO_URL="https://github.com/seventhlegend/nexus-network-updater.git"
INSTALL_DIR="/opt/nexus-updater"
SERVICE_NAME="nexus-updater"

echo "🔍 Detecting current path..."
SELF_PATH=$(realpath "$0")
SELF_DIR=$(dirname "$SELF_PATH")

echo "🛑 Stopping service if running..."
sudo systemctl stop ${SERVICE_NAME}.timer || true
sudo systemctl disable ${SERVICE_NAME}.timer || true

echo "⬆️ Going up one level..."
cd "$SELF_DIR/.."

echo "🧹 Removing existing repo directory: $SELF_DIR"
sudo rm -rf "$SELF_DIR"

echo "📥 Cloning fresh copy into same location..."
sudo git clone $REPO_URL "$SELF_DIR"

echo "⚙️ Installing fresh copy..."
cd "$SELF_DIR"
sudo bash install.sh

echo "🚀 Restarting timer..."
sudo systemctl enable --now ${SERVICE_NAME}.timer

echo "✅ Reinstallation complete."
