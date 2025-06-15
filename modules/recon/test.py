import subprocess
import socket
import re
import os

# === Configuration ===
domain = "afit.edu.ng"
masscan_output = "masscan-results.txt"
ip_file = "ip.txt"
port_file = "ports.txt"
naabu_output = "naabu-full.txt"
masscan_rate = "10000"

def resolve_domain(domain):
    try:
        ip = socket.gethostbyname(domain)
        print(f"[*] Resolved {domain} to {ip}")
        return ip
    except socket.gaierror:
        print(f"[!] Could not resolve domain: {domain}")
        return None

def run_masscan(ip, output_file, rate="10000"):
    print(f"[*] Running masscan on {ip} with rate {rate}")
    cmd = [
        "sudo", "masscan", "-p0-65535", ip,
        "--rate", rate, "-oL", output_file
    ]
    subprocess.run(cmd, check=True)
    print("[*] Masscan scan completed.")

def extract_ports(masscan_output_file, port_file):
    print("[*] Extracting open ports...")
    with open(masscan_output_file, "r") as f:
        data = f.read()
    ports = sorted(set(map(int, re.findall(r"open tcp (\d+)", data))))
    ports_str = ",".join(map(str, ports))
    with open(port_file, "w") as f:
        f.write(ports_str)
    print(f"[*] Found open ports: {ports_str}")
    return ports_str

def run_naabu(ip_file, ports, output_file):
    print("[*] Running naabu with nmap integration...")
    cmd = [
        "naabu",
        "-list", ip_file,
        "-p", ports,
        "-nmap-cli", "nmap -sV -sC",
        "-o", output_file
    ]
    subprocess.run(cmd, check=True)
    print(f"[*] Naabu scan completed. Results saved to {output_file}")

def main():
    ip = resolve_domain(domain)
    if not ip:
        return

    with open(ip_file, "w") as f:
        f.write(ip + "\n")

    run_masscan(ip, masscan_output, rate=masscan_rate)
    ports = extract_ports(masscan_output, port_file)
    run_naabu(ip_file, ports, naabu_output)

if __name__ == "__main__":
    main()
