#!/bin/bash
set -e

PROJECT_DIR=$(pwd)
USER=$(whoami)
SERVICE_NAME="ultron"

echo "* Creating virtual environment..."
python3 -m venv ultron
source ultron/bin/activate

echo "* Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "* Preparing systemd service..."
sed "s|{{USER}}|$USER|g; s|{{PROJECT_DIR}}|$PROJECT_DIR|g" install/${SERVICE_NAME}.service >/tmp/${SERVICE_NAME}.service

sudo mv /tmp/${SERVICE_NAME}.service /etc/systemd/system/${SERVICE_NAME}.service

echo "* Enabling and starting service..."
sudo systemctl daemon-reload
sudo systemctl enable ${SERVICE_NAME}
sudo systemctl start ${SERVICE_NAME}

echo "* Service ${SERVICE_NAME} started"
