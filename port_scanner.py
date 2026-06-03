import socket
import sys
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# =========================================================
# 1. SCANNER ENGINE LOGIC
# =========================================================
def scan_single_port(target_ip, port):
    """Attempts a clean TCP handshake connection to verify port state."""
    try:
        # Initialize a standard IPv4 Stream Socket (TCP connection mechanism)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set a strict timeout constraint so the script doesn't hang indefinitely
        s.settimeout(1.0)
        
        # Execute the handshake attempt
        result = s.connect_ex((target_ip, port))
        
        # connect_ex returns 0 if the connection transaction succeeded perfectly
        if result == 0:
            print(f"  [+] Port {port:<5} is OPEN   --> Service: {socket.getservbyname(port, 'tcp') if safe_get_service(port) else 'Unknown'}")
        
        s.close()
    except Exception:
        pass

def safe_get_service(port):
    """Helper tool to safely resolve standard port service definitions."""
    try:
        socket.getservbyname(port, 'tcp')
        return True
    except Exception:
        return False

# =========================================================
# 2. TARGET CONFIGURATION & EXECUTION PIPELINE
# =========================================================
def run_scanner():
    TARGET_HOST = "127.0.0.1"
    
    try:
        target_ip = socket.gethostbyname(TARGET_HOST)
    except socket.gaierror:
        print("\n [-] Failed to resolve target hostname network layer parameter.")
        sys.exit()

    print("-" * 60)
    print(f" Launching Dynamic Security Scan on Host Target: {target_ip}")
    print("-" * 60)

    # DYNAMIC GENERATION: Scan an entire block array range (e.g., ports 79 through 100)
    # This automatically builds a list containing [79, 80, 81, ..., 100]
    ports_to_scan = list(range(79, 101))
    
    # We can add our custom Streamlit port back into the mix explicitly
    ports_to_scan.append(8501)

    # Max workers bumped up to handle the increased packet capacity concurrently
    with ThreadPoolExecutor(max_workers=20) as executor:
        for port in ports_to_scan:
            executor.submit(scan_single_port, target_ip, port)

if __name__ == "__main__":
    run_scanner()