# FakeDownloader

A Linux systemd service that downloads a file every 30 minutes to simulate network activity.

## Quick Install

**Single command installation:**

```bash
curl -sSL https://raw.githubusercontent.com/mralinp/FakeDownloader/main/install.sh | sudo bash
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

The `.env` file contains the following settings:

- `DOWNLOAD_URL`: The URL of the file to download
- `INTERFACE`: Network interface to monitor (default: eth0)
- `DESTINATION`: Temporary filename for downloads (default: downloaded_file)
- `CHUNK_SIZE`: Download chunk size in bytes (default: 102400)

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
