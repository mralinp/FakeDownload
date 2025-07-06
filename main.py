import psutil
import time
import requests
import os
import random
import configparser




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
            'chunk_size': '102400'
        }
    }
    
    # Try to load existing config file
    if os.path.exists(config_file):
        print(f"[{time.ctime()}] Config file exists, reading...")
        config.read(config_file)
        
        # Debug: print what we read
        try:
            url = config.get('DEFAULT', 'download_url')
            print(f"[{time.ctime()}] Read URL: '{url}'")
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

def get_io(interface):
    io = psutil.net_io_counters(pernic=True)[interface]
    return io.bytes_sent, io.bytes_recv

def download_file():
    # Remove any previously downloaded file
    if os.path.exists(DESTINATION):
        os.remove(DESTINATION)
        print(f"[{time.ctime()}] Removed previous download: {DESTINATION}")
    
    sent0, recv0 = get_io(INTERFACE)
    print(f"[{time.ctime()}] Starting download...")

    response = requests.get(URL, stream=True)
    with open(DESTINATION, 'wb') as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
                f.write(chunk)

    sent1, recv1 = get_io(INTERFACE)
    upload = sent1 - sent0
    download = recv1 - recv0
    ratio = upload / download if download else float('inf')

    print(f"[{time.ctime()}] Download complete.")
    print(f"Upload: {upload / 1024:.2f} KB | Download: {download / 1024:.2f} KB | Ratio: {ratio:.2f}")

    if os.path.exists(DESTINATION):
        os.remove(DESTINATION)
        print(f"[{time.ctime()}] File removed.\n")

def main_loop():
    while True:
        download_file()
        sleep_time = 1800  # 30 minutes (1800 seconds)
        print(f"Sleeping for {sleep_time // 60} minutes...\n")
        time.sleep(sleep_time)

if __name__ == "__main__":
    main_loop()
