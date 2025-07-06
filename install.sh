#!/bin/bash

# Exit on any error
set -e

INSTALL_DIR="/opt/fakedownloader"
SERVICE_NAME="fakedownloader"

echo "=== FakeDownloader Service Installer ==="

# Check if service is already installed
if systemctl is-active --quiet $SERVICE_NAME 2>/dev/null || [ -d "$INSTALL_DIR" ]; then
    echo "FakeDownloader is already installed!"
    echo ""
    echo "Choose an option:"
    echo "1) Reinstall (remove and install fresh)"
    echo "2) Uninstall (remove completely)"
    echo "3) Exit"
    echo ""
    read -p "Enter your choice (1-3): " choice
    
    case $choice in
        1)
            echo "Reinstalling FakeDownloader..."
            # Stop and disable service
            systemctl stop $SERVICE_NAME 2>/dev/null || true
            systemctl disable $SERVICE_NAME 2>/dev/null || true
            # Remove service file
            rm -f /etc/systemd/system/$SERVICE_NAME.service
            # Remove installation directory
            rm -rf "$INSTALL_DIR"
            systemctl daemon-reload
            echo "Removed existing installation."
            ;;
        2)
            echo "Uninstalling FakeDownloader..."
            # Stop and disable service
            systemctl stop $SERVICE_NAME 2>/dev/null || true
            systemctl disable $SERVICE_NAME 2>/dev/null || true
            # Remove service file
            rm -f /etc/systemd/system/$SERVICE_NAME.service
            # Remove installation directory
            rm -rf "$INSTALL_DIR"
            systemctl daemon-reload
            echo "FakeDownloader has been uninstalled."
            exit 0
            ;;
        3)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid choice. Exiting..."
            exit 1
            ;;
    esac
fi

# Update system and install dependencies
echo "Installing system dependencies..."
apt update --yes
apt install python3 python3-pip python3-venv git curl wget --yes

# Clone the project to /opt
echo "Cloning FakeDownloader project..."
if [ ! -d "$INSTALL_DIR" ]; then
    git clone https://github.com/mralinp/FakeDownload.git "$INSTALL_DIR"
    cd "$INSTALL_DIR"
else
    cd "$INSTALL_DIR"
    git pull origin main
fi

# Get download URL from user and validate it
echo ""
echo "Please enter the download URL when prompted."
echo "The script will validate the URL before proceeding."
echo ""

# Get download URL from user and validate it
echo ""
echo "Please enter the download URL when prompted."
echo "The script will validate the URL before proceeding."
echo ""

# Get download URL from user and validate it
echo ""
echo "Please enter the download URL when prompted."
echo "The script will validate the URL before proceeding."
echo ""

# Get URL from user or environment variable
if [ -z "$DOWNLOAD_URL" ]; then
    read -p "Enter the download URL: " DOWNLOAD_URL
else
    echo "Using DOWNLOAD_URL from environment: $DOWNLOAD_URL"
fi

# Validate the URL
while true; do
    # Basic URL validation
    if [[ $DOWNLOAD_URL =~ ^https?:// ]]; then
        echo "Testing URL accessibility..."
        if curl --output /dev/null --silent --head --fail "$DOWNLOAD_URL"; then
            echo "URL is valid and accessible!"
            break
        else
            echo "Error: URL is not accessible. Please check the URL and try again."
            read -p "Enter the download URL: " DOWNLOAD_URL
        fi
    else
        echo "Error: Invalid URL format. URL must start with http:// or https://"
        read -p "Enter the download URL: " DOWNLOAD_URL
    fi
done

# Get download interval from user
echo ""
echo "Please enter the download interval in minutes."
echo "Recommended: 30 minutes (minimum: 1 minute)"
echo ""

if [ -z "$DOWNLOAD_INTERVAL" ]; then
    read -p "Enter download interval (minutes): " DOWNLOAD_INTERVAL
else
    echo "Using DOWNLOAD_INTERVAL from environment: $DOWNLOAD_INTERVAL"
fi

# Validate the interval
while true; do
    if [[ $DOWNLOAD_INTERVAL =~ ^[0-9]+$ ]] && [ $DOWNLOAD_INTERVAL -ge 1 ]; then
        echo "Download interval set to $DOWNLOAD_INTERVAL minutes"
        break
    else
        echo "Error: Please enter a valid number (minimum 1 minute)"
        read -p "Enter download interval (minutes): " DOWNLOAD_INTERVAL
    fi
done

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python packages..."
pip install -r requirements.txt

# Create config.ini file with user's URL and interval
echo "Creating configuration file..."
cat > config.ini << EOF
[DEFAULT]
download_url = ${DOWNLOAD_URL}
destination = downloaded_file
chunk_size = 102400
interval_minutes = ${DOWNLOAD_INTERVAL}
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

