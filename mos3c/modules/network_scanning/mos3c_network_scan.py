# mos3c_network_scan.py

import os
import socket
import subprocess
from concurrent.futures import ThreadPoolExecutor

def scan_port(ip, port):
    """Scan a single port on a given IP address."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((ip, port))
    sock.close()
    return port if result == 0 else None

def scan_ports(ip, ports):
    """Scan a range of ports on a given IP address."""
    open_ports = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(scan_port, ip, port): port for port in ports}
        for future in futures:
            port = future.result()
            if port:
                open_ports.append(port)
    return open_ports

def network_scan(target, port_range):
    """Perform a network scan on the target IP address."""
    print(f"Scanning {target} for open ports...")
    open_ports = scan_ports(target, port_range)
    if open_ports:
        print(f"Open ports on {target}: {', '.join(map(str, open_ports))}")
    else:
        print(f"No open ports found on {target}.")

def main():
    target = input("Enter the target IP address: ")
    port_range = range(1, 1025)  # Scanning ports 1 to 1024
    network_scan(target, port_range)

if __name__ == "__main__":
    main()