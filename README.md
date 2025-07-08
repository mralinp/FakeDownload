# 🚀 FakeDownloader

**A lightweight Linux systemd service to simulate periodic network activity.**  
Ideal for artificially increasing the bandwidth footprint of a server (e.g., to throttle or mask actual usage patterns).

## 📦 Features

- Downloads a remote file at regular intervals (default: every 30 minutes)
- Removes the file after each download to save space
- Simulates network usage to affect perceived upload/download statistics
- Automatically detects active network interface
- Lightweight, persistent, and systemd-managed

## ⚡ Quick Installation

```bash
bash <(curl -Ls https://raw.githubusercontent.com/mralinp/FakeDownload/main/install.sh)
```

## ⚙️ Configuration

Edit the config.ini file to customize behavior:

```ini
[settings]
download_url = https://example.com/largefile.zip   # URL to download
destination = downloaded_file                      # Temporary filename
chunk_size = 102400                                # Chunk size in bytes
interval_minutes = 30                              # Download interval in mins, min=1
```

`download_url`: Remote file URL to simulate download.

`destination`: Temporary local file name. This file is deleted after the download finishes.

`chunk_size`: Size of download chunks (in bytes) for more granular bandwidth control.

`interval_minutes` = Rest time between downloads in minutes, minimum rest time is **one** minute.

🧠 The service auto-detects the active network interface — no need for manual network configuration.

## 🧰 Service Management

Control the service using systemctl:

| Action            | Command                                |
| ----------------- | -------------------------------------- |
| Start the service | `sudo systemctl start fakedownloader`  |
| Stop the service  | `sudo systemctl stop fakedownloader`   |
| Enable at boot    | `sudo systemctl enable fakedownloader` |
| Check status      | `sudo systemctl status fakedownloader` |
| View logs         | `sudo journalctl -u fakedownloader -f` |

## 🔍 How It Works

1. Every 30 minutes, the service:
   - Downloads the specified file using chunked HTTP reads
   - Logs the amount of data downloaded/uploaded
   - Deletes the downloaded file to conserve disk space
   - Sleeps for 30–45 minutes before repeating
2. Runs as a persistent systemd service and automatically restarts if it crashes.

## 📑 Logs

Logs are available via journalctl and include:

- Timestamps for each download cycle
- Download/upload byte counts
- File deletion confirmations
- Sleep intervals between runs

## ✅ Use Case

This is useful when:

- You want to throttle actual server usage visibility (e.g., disguise download rate)
- You’re trying to reach a minimum network usage quota
- You need to simulate network traffic for load balancing, ISP behavior testing, or evasion scenarios

## 💡 Notes

- Make sure the download_url points to a large enough file to simulate meaningful traffic.
- The download does not affect disk space long-term, as the file is removed immediately after completion.

## 📄 License

MIT © mralinp
