#!/bin/bash
set -e

INSTALL_DIR="/opt/nexus-updater"
SERVICE_NAME="nexus-updater"

echo "🔧 Installing Nexus Updater..."

sudo mkdir -p $INSTALL_DIR
sudo cp nexus_updater.py $INSTALL_DIR/
sudo cp nexus-updater.service /etc/systemd/system/
sudo cp nexus-updater.timer /etc/systemd/system/
sudo chmod +x $INSTALL_DIR/nexus_updater.py

sudo systemctl daemon-reload
sudo systemctl enable --now ${SERVICE_NAME}.timer

echo "✅ Nexus Updater installed and activated."
echo "Log file: $INSTALL_DIR/updater.log"
