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

def run_masscan(ip):
    output_file = f"masscan_results_{ip}.txt"
    try:
        print(Fore.GREEN + f"[+] Running masscan on {ip} (all ports)...")
        masscan_cmd = ["sudo", "masscan", "-p0-65535", ip, "--rate", "100000", "-oG", output_file]
        subprocess.run(masscan_cmd, check=True)
        return output_file
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"[-] Masscan failed: {e}")
        return None

def parse_masscan_output(file_path):
    open_ports = []
    total_ports = 65536  # full range 0-65535
    with open(file_path, "r") as f:
        for line in f:
            if "Host:" in line and "Ports:" in line:
                parts = line.strip().split()
                ip_index = parts.index("Host:") + 1
                ip = parts[ip_index]
                ports_raw = " ".join(parts[parts.index("Ports:") + 1:])
                port_entries = ports_raw.split(",")
                for entry in port_entries:
                    port_info = entry.strip().split("/")
                    if len(port_info) >= 3:
                        port = port_info[0]
                        protocol = port_info[2]
                        service = port_info[4] if len(port_info) > 4 else "unknown"
                        open_ports.append(f"{ip}:{port}/{protocol} ({service})")
    return open_ports, total_ports

def write_pdf(ip, open_ports, scanned_ports, open_count, total_ports):
    file = f"masscan_report_{ip}.pdf"
    c = canvas.Canvas(file, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, height - 80, f"Masscan Port Scan Report for {ip}")
    c.setFont("Helvetica", 10)
    c.drawString(72, height - 100, f"Generated on: {datetime.datetime.now()}")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(72, height - 130, "Scanned Port Range:")
    c.setFont("Helvetica", 10)
    c.drawString(72, height - 145, scanned_ports)

    c.setFont("Helvetica-Bold", 12)
    c.drawString(72, height - 170, "Port Status Analytics:")
    percent = (open_count / total_ports) * 100
    c.setFont("Helvetica", 10)
    c.drawString(72, height - 185, f"Open Ports: {open_count} / {total_ports} ({percent:.2f}%)")

    y = height - 215
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

def write_csv(ip, open_ports, scanned_ports, open_count, total_ports):
    file = f"masscan_report_{ip}.csv"
    with open(file, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Scanned Port Range", scanned_ports])
        writer.writerow(["Open Ports", f"{open_count}/{total_ports} ({(open_count/total_ports)*100:.2f}%)"])
        writer.writerow([])
        writer.writerow(["Open Port List"])
        for port in open_ports:
            writer.writerow([port])
    print(Fore.CYAN + f"[+] CSV saved as {file}")

def write_html(ip, open_ports, scanned_ports, open_count, total_ports):
    file = f"masscan_report_{ip}.html"
    percent = (open_count / total_ports) * 100
    with open(file, "w") as f:
        f.write(f"<html><head><title>Masscan Report for {ip}</title></head><body>")
        f.write(f"<h1>Masscan Port Scan Report for {ip}</h1>")
        f.write(f"<p>Generated on: {datetime.datetime.now()}</p>")
        f.write(f"<h2>Scanned Port Range:</h2><p>{scanned_ports}</p>")
        f.write(f"<h2>Port Status Analytics:</h2><p>Open Ports: {open_count} / {total_ports} ({percent:.2f}%)</p>")
        f.write("<h2>Open Ports:</h2><ul>")
        for port in open_ports:
            f.write(f"<li>{port}</li>")
        f.write("</ul></body></html>")
    print(Fore.CYAN + f"[+] HTML saved as {file}")

def export_menu(ip, open_ports, scanned_ports, total_ports):
    open_count = len(open_ports)
    while True:
        print(Fore.YELLOW + "\n\U0001F4E4 Export Options:")
        print("1. Save as PDF")
        print("2. Save as CSV")
        print("3. Save as HTML")
        print("4. Skip export")
        choice = input(Fore.BLUE + "Choose an option (1-4): ").strip()

        if choice == '1':
            write_pdf(ip, open_ports, scanned_ports, open_count, total_ports)
            break
        elif choice == '2':
            write_csv(ip, open_ports, scanned_ports, open_count, total_ports)
            break
        elif choice == '3':
            write_html(ip, open_ports, scanned_ports, open_count, total_ports)
            break
        elif choice == '4':
            print(Fore.YELLOW + "[*] Export skipped.")
            break
        else:
            print(Fore.RED + "[!] Invalid option. Try again.")

def main():
    clear_screen()
    print(Fore.MAGENTA + "=== Automated Masscan Scanner ===")
    domain = input(Fore.BLUE + "\nEnter target domain (e.g., example.com): ").strip()
    if not domain:
        print(Fore.RED + "[-] Domain cannot be empty.")
        return

    ip = resolve_ip(domain)
    if not ip:
        print(Fore.RED + f"[-] Could not resolve IP for {domain}")
        return

    print(Fore.GREEN + f"[+] IP address of {domain} is {ip}")
    output_file = run_masscan(ip)
    if not output_file:
        return

    open_ports, total_ports = parse_masscan_output(output_file)
    if open_ports:
        print(Fore.GREEN + f"[+] Open ports on {ip}:")
        for port in open_ports:
            print(Fore.YELLOW + f" - {port}")
    else:
        print(Fore.RED + "[-] No open ports found.")

    export_menu(ip, open_ports, scanned_ports="TCP 0-65535", total_ports=total_ports)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Program interrupted by user.")
        sys.exit(0)
