from colorama import Fore, init
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import subprocess
import os
import shutil
import datetime
import csv
import sys

init(autoreset=True)

def check_tool_installed(tool_name):
    return shutil.which(tool_name) is not None

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def resolve_ip(domain):
    try:
        result = subprocess.run(["host", domain], capture_output=True, text=True)
        lines = result.stdout.splitlines()
        for line in lines:
            if "has address" in line:
                return line.split()[-1]
    except Exception as e:
        print(Fore.RED + f"[-] Failed to resolve IP: {e}")
    return None

def run_nmap(domain):
    output_file_prefix = f"nmap_fullscan_{domain.replace('.', '_')}"
    try:
        print(Fore.GREEN + f"[+] Running Nmap full scan on {domain}...")
        nmap_cmd = [
            "nmap", "-p-", "--min-rate", "1000", "-T4", "-A", domain,
            "-oA", output_file_prefix
        ]
        subprocess.run(nmap_cmd, check=True)
        return output_file_prefix + ".gnmap"
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"[-] Nmap failed: {e}")
        return None

def parse_nmap_output(file_path):
    open_ports = []
    with open(file_path, "r") as f:
        for line in f:
            if line.startswith("Host:") and "Ports:" in line:
                parts = line.strip().split("\t")
                ip = parts[1].split(" ")[0]
                ports_info = parts[-1].replace("Ports: ", "").split(", ")
                for entry in ports_info:
                    if "/open/" in entry:
                        open_ports.append(f"{ip}: {entry}")
    return open_ports

def write_pdf(domain, open_ports):
    file = f"nmap_report_{domain.replace('.', '_')}.pdf"
    c = canvas.Canvas(file, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, height - 80, f"🛡️ Nmap Full Port Scan Report for {domain}")
    c.setFont("Helvetica", 10)
    c.drawString(72, height - 100, f"Generated on: {datetime.datetime.now()}")

    y = height - 130
    c.setFont("Helvetica-Bold", 12)
    c.drawString(72, y, "Open Ports:")
    y -= 20
    c.setFont("Helvetica", 10)

    for port in open_ports:
        if y < 50:
            c.showPage()
            y = height - 50
        c.drawString(72, y, port)
        y -= 15

    c.save()
    print(Fore.CYAN + f"[+] PDF saved as {file}")

def write_csv(domain, open_ports):
    file = f"nmap_report_{domain.replace('.', '_')}.csv"
    with open(file, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Open Ports"])
        for port in open_ports:
            writer.writerow([port])
    print(Fore.CYAN + f"[+] CSV saved as {file}")

def write_html(domain, open_ports):
    file = f"nmap_report_{domain.replace('.', '_')}.html"
    with open(file, "w") as f:
        f.write(f"<html><head><title>Nmap Report for {domain}</title></head><body>")
        f.write(f"<h1>🛡️ Nmap Full Port Scan Report for {domain}</h1>")
        f.write(f"<p>Generated on: {datetime.datetime.now()}</p>")
        f.write("<h2>Open Ports:</h2><ul>")
        for port in open_ports:
            f.write(f"<li>{port}</li>")
        f.write("</ul></body></html>")
    print(Fore.CYAN + f"[+] HTML saved as {file}")

def export_menu(domain, open_ports):
    while True:
        print(Fore.YELLOW + "\n📤 Export Options:")
        print("1. Save as PDF")
        print("2. Save as CSV")
        print("3. Save as HTML")
        print("4. Skip export")
        choice = input(Fore.BLUE + "Choose an option (1-4): ").strip()

        if choice == '1':
            write_pdf(domain, open_ports)
            break
        elif choice == '2':
            write_csv(domain, open_ports)
            break
        elif choice == '3':
            write_html(domain, open_ports)
            break
        elif choice == '4':
            print(Fore.YELLOW + "[*] Export skipped.")
            break
        else:
            print(Fore.RED + "[!] Invalid option. Try again.")

def main():
    clear_screen()
    print(Fore.MAGENTA + "=== Automated Nmap Full Scanner ===")
    domain = input(Fore.BLUE + "\nEnter target domain (e.g., example.com): ").strip()
    if not domain:
        print(Fore.RED + "[-] Domain cannot be empty.")
        return

    ip = resolve_ip(domain)
    if not ip:
        print(Fore.RED + f"[-] Could not resolve IP for {domain}")
        return

    print(Fore.GREEN + f"[+] IP address of {domain} is {ip}")
    gnmap_file = run_nmap(domain)
    if not gnmap_file:
        return

    open_ports = parse_nmap_output(gnmap_file)
    if open_ports:
        print(Fore.GREEN + f"[+] Open ports on {domain}:")
        for port in open_ports:
            print(Fore.YELLOW + f" - {port}")
    else:
        print(Fore.RED + "[-] No open ports found.")
    
    export_menu(domain, open_ports)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Program interrupted by user.")
        sys.exit(0)
