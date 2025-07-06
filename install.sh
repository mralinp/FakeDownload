#!/bin/bash

# Exit on any error
set -e

echo "=== FakeDownloader Service Installer ==="

# Update system and install dependencies
echo "Installing system dependencies..."
apt update --yes
apt install python3 python3-pip python3-venv git --yes

# Get download URL from user
echo ""
read -p "Enter the download URL: " DOWNLOAD_URL

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python packages..."
pip install -r requirements.txt

# Create .env file with user's URL
echo "Creating configuration file..."
cat > .env << EOF
# Download configuration
DOWNLOAD_URL=${DOWNLOAD_URL}
# INTERFACE will be auto-detected
DESTINATION=downloaded_file
CHUNK_SIZE=102400
EOF

# Copy systemd service file
echo "Setting up systemd service..."
cp fakedownloader.service /etc/systemd/system/

# Reload systemd and enable service
systemctl daemon-reload
systemctl enable fakedownloader.service

# Start the service
echo "Starting FakeDownloader service..."
systemctl start fakedownloader.service

echo ""
echo "=== Installation Complete! ==="
echo "Service is now running and will start automatically on boot."
echo ""
echo "Useful commands:"
echo "  Check status: systemctl status fakedownloader"
echo "  View logs: journalctl -u fakedownloader -f"
echo "  Stop service: systemctl stop fakedownloader"
echo "  Restart service: systemctl restart fakedownloader"

