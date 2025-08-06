#!/bin/bash

SERVICE_NAME="nexus-updater"
INSTALL_DIR="/opt/nexus-updater"

echo "🗑 Removing Nexus Updater..."

sudo systemctl disable --now ${SERVICE_NAME}.timer || true
sudo rm -f /etc/systemd/system/${SERVICE_NAME}.service
sudo rm -f /etc/systemd/system/${SERVICE_NAME}.timer
sudo rm -rf $INSTALL_DIR
sudo systemctl daemon-reload

echo "✅ Nexus Updater removed."
