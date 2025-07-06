import psutil
import time
import os
import random
import configparser
import subprocess




def load_config():
    """Load configuration from config.ini file"""
    config = configparser.ConfigParser()
    config_file = '/opt/fakedownloader/config.ini'
    
    print(f"[{time.ctime()}] Loading config from: {config_file}")
    
    # Default configuration
    default_config = {
        'DEFAULT': {
            'download_url': 'http://your-server.com/file',
            'destination': 'downloaded_file',
            'chunk_size': '102400',
            'interval_minutes': '30'
        }
    }
    
    # Try to load existing config file
    if os.path.exists(config_file):
        print(f"[{time.ctime()}] Config file exists, reading...")
        config.read(config_file)
        
        # Debug: print what we read
        try:
            url = config.get('DEFAULT', 'download_url')
            interval = config.get('DEFAULT', 'interval_minutes')
            print(f"[{time.ctime()}] Read URL: '{url}'")
            print(f"[{time.ctime()}] Read interval: {interval} minutes")
            if not url or url.strip() == '':
                print(f"[{time.ctime()}] ERROR: URL is empty!")
                raise ValueError("URL is empty")
        except Exception as e:
            print(f"[{time.ctime()}] Error reading config: {e}")
            raise
    else:
        print(f"[{time.ctime()}] Config file not found, creating default...")
        # Create default config
        config.read_dict(default_config)
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        with open(config_file, 'w') as f:
            config.write(f)
    
    return config

def get_default_interface():
    """Get the default network interface automatically"""
    try:
        # Get all network interfaces
        interfaces = psutil.net_if_addrs()
        
        # Common interface names to check in order of preference
        preferred_interfaces = ['eth0', 'enp0s3', 'ens33', 'en0', 'wlan0', 'wlp2s0']
        
        # First try preferred interfaces
        for interface in preferred_interfaces:
            if interface in interfaces:
                return interface
        
        # If no preferred interface found, get the first non-loopback interface
        for interface in interfaces:
            if interface != 'lo' and not interface.startswith('docker') and not interface.startswith('veth'):
                return interface
                
        # Fallback to eth0 if nothing else works
        return 'eth0'
    except:
        return 'eth0'

# Load configuration
config = load_config()

INTERFACE = get_default_interface()  # Auto-detect network interface
URL = config.get('DEFAULT', 'download_url')  # Download URL
DESTINATION = config.get('DEFAULT', 'destination')  # Temporary download name
CHUNK_SIZE = int(config.get('DEFAULT', 'chunk_size'))  # Chunk size
INTERVAL_MINUTES = int(config.get('DEFAULT', 'interval_minutes'))  # Download interval in minutes

def get_io(interface):
    io = psutil.net_io_counters(pernic=True)[interface]
    return io.bytes_sent, io.bytes_recv

def download_file():
    print(f"[{time.ctime()}] ===== Starting download cycle =====")
    print(f"[{time.ctime()}] Download URL: {URL}")
    print(f"[{time.ctime()}] Interface: {INTERFACE}")
    
    # Remove any previously downloaded file
    if os.path.exists(DESTINATION):
        os.remove(DESTINATION)
        print(f"[{time.ctime()}] ✓ Removed previous download: {DESTINATION}")
    
    # Get initial network stats
    sent0, recv0 = get_io(INTERFACE)
    print(f"[{time.ctime()}] 📊 Initial network stats - Sent: {sent0/1024:.2f} KB, Received: {recv0/1024:.2f} KB")
    print(f"[{time.ctime()}] 🚀 Starting download...")

    # Use wget to download the file
    try:
        print(f"[{time.ctime()}] 📥 Downloading from: {URL}")
        result = subprocess.run([
            'wget', 
            '--quiet',  # Suppress output
            '--output-document=' + DESTINATION,  # Save to destination file
            '--timeout=300',  # 5 minute timeout
            '--tries=3',  # Retry 3 times
            URL
        ], capture_output=True, text=True, timeout=300)  # 5 minute timeout
        
        if result.returncode != 0:
            print(f"[{time.ctime()}] ❌ Download failed: {result.stderr}")
            return
        
        # Get file size
        if os.path.exists(DESTINATION):
            file_size = os.path.getsize(DESTINATION)
            print(f"[{time.ctime()}] ✅ Download completed successfully - File size: {file_size/1024:.2f} KB")
        else:
            print(f"[{time.ctime()}] ❌ Download completed but file not found")
            return
        
    except subprocess.TimeoutExpired:
        print(f"[{time.ctime()}] ⏰ Download timed out after 5 minutes")
        return
    except Exception as e:
        print(f"[{time.ctime()}] 💥 Download error: {e}")
        return

    # Get final network stats
    sent1, recv1 = get_io(INTERFACE)
    upload = sent1 - sent0
    download = recv1 - recv0
    ratio = upload / download if download else float('inf')

    print(f"[{time.ctime()}] 📈 Download complete.")
    print(f"[{time.ctime()}] 📊 Network usage - Upload: {upload / 1024:.2f} KB | Download: {download / 1024:.2f} KB | Ratio: {ratio:.2f}")

    # Clean up downloaded file
    if os.path.exists(DESTINATION):
        os.remove(DESTINATION)
        print(f"[{time.ctime()}] 🗑️ File removed: {DESTINATION}")
    
    print(f"[{time.ctime()}] ===== Download cycle completed =====")

def main_loop():
    print(f"[{time.ctime()}] 🎯 FakeDownloader started successfully!")
    print(f"[{time.ctime()}] ⏱️ Download interval: {INTERVAL_MINUTES} minutes")
    print(f"[{time.ctime()}] 🌐 Network interface: {INTERFACE}")
    print(f"[{time.ctime()}] 🔗 Download URL: {URL}")
    print(f"[{time.ctime()}] ==========================================")
    
    while True:
        download_file()
        sleep_time = INTERVAL_MINUTES * 60  # Convert minutes to seconds
        print(f"[{time.ctime()}] 😴 Sleeping for {INTERVAL_MINUTES} minutes until next download...")
        print(f"[{time.ctime()}] ⏰ Next download at: {time.ctime(time.time() + sleep_time)}")
        print(f"[{time.ctime()}] ==========================================")
        time.sleep(sleep_time)

if __name__ == "__main__":
    main_loop()
