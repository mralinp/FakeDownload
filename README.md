# FakeDownloader

A Linux systemd service that downloads a file every 30 minutes to simulate network activity.

## Quick Install

**Method 1: Interactive installation (recommended):**

```bash
curl -sSL https://raw.githubusercontent.com/mralinp/FakeDownload/main/install.sh | sudo bash
```

**Method 2: Non-interactive installation with URL:**

```bash
DOWNLOAD_URL=http://your-server.com/file curl -sSL https://raw.githubusercontent.com/mralinp/FakeDownload/main/install.sh | sudo bash
```

## Manual Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/mralinp/FakeDownloader.git
   cd FakeDownloader
   ```

2. **Run the setup script:**
   ```bash
   chmod +x install.sh
   sudo ./install.sh
   ```

## Configuration

The `config.ini` file contains the following settings:

- `download_url`: The URL of the file to download
- `destination`: Temporary filename for downloads (default: downloaded_file)
- `chunk_size`: Download chunk size in bytes (default: 102400)

**Note:** The network interface is automatically detected and doesn't need to be configured.

## Service Management

**Start the service:**

```bash
sudo systemctl start fakedownloader
```

**Stop the service:**

```bash
sudo systemctl stop fakedownloader
```

**Check service status:**

```bash
sudo systemctl status fakedownloader
```

**View service logs:**

```bash
sudo journalctl -u fakedownloader -f
```

**Enable auto-start on boot:**

```bash
sudo systemctl enable fakedownloader
```

## How it works

The service downloads the specified file every 30 minutes, measures network I/O, and then removes the downloaded file. It runs continuously as a systemd service and will automatically restart if it crashes.

## Logs

The service logs include:

- Download start/complete timestamps
- Network upload/download statistics
- File removal confirmations
- Sleep duration notifications
