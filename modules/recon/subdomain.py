from colorama import Fore, Style, init
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import subprocess
import os
import shutil
import sys
import datetime
import csv

# Initialize colorama
init(autoreset=True)

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def check_tool_installed(tool_name):
    return shutil.which(tool_name) is not None

def write_to_pdf(domain, all_subs, live_subs):
    pdf_file = f"subdomain_report_{domain}.pdf"
    c = canvas.Canvas(pdf_file, pagesize=letter)
    width, height = letter

    # Title with emoji
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, height - 80, f"📄 Subdomain Discovery Report for {domain}")
    c.setFont("Helvetica", 10)
    c.drawString(72, height - 100, f"Generated on: {datetime.datetime.now()}")

    y = height - 130
    c.setFont("Helvetica-Bold", 12)
    c.drawString(72, y, "Discovered Subdomains:")
    y -= 20
    c.setFont("Helvetica", 10)

    for sub in all_subs:
        if y < 50:
            c.showPage()
            y = height - 50
        c.drawString(72, y, sub)
        y -= 15

    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(72, y, "Live Subdomains:")
    y -= 20
    c.setFont("Helvetica", 10)

    for sub in live_subs:
        if y < 50:
            c.showPage()
            y = height - 50
        c.drawString(72, y, sub)
        y -= 15

    c.save()
    print(Fore.CYAN + f"[+] PDF report saved as {pdf_file}")

def write_to_csv(domain, all_subs, live_subs):
    csv_file = f"subdomain_report_{domain}.csv"
    with open(csv_file, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Discovered Subdomains"])
        for sub in all_subs:
            writer.writerow([sub])
        writer.writerow([])
        writer.writerow(["Live Subdomains"])
        for sub in live_subs:
            writer.writerow([sub])
    print(Fore.CYAN + f"[+] CSV report saved as {csv_file}")

def write_to_html(domain, all_subs, live_subs):
    html_file = f"subdomain_report_{domain}.html"
    with open(html_file, "w") as f:
        f.write(f"<html><head><title>Subdomain Report for {domain}</title></head><body>")
        f.write(f"<h1>📄 Subdomain Discovery Report for {domain}</h1>")
        f.write(f"<p>Generated on: {datetime.datetime.now()}</p>")
        f.write("<h2>Discovered Subdomains:</h2><ul>")
        for sub in all_subs:
            f.write(f"<li>{sub}</li>")
        f.write("</ul><h2>Live Subdomains:</h2><ul>")
        for sub in live_subs:
            f.write(f"<li>{sub}</li>")
        f.write("</ul></body></html>")
    print(Fore.CYAN + f"[+] HTML report saved as {html_file}")

def export_menu(domain, all_subs, live_subs):
    while True:
        print(Fore.YELLOW + "\n📤 Export Options:")
        print("1. Save as PDF")
        print("2. Save as CSV")
        print("3. Save as HTML")
        print("4. Skip export")
        choice = input(Fore.BLUE + "Choose an option (1-4): ").strip()

        if choice == '1':
            write_to_pdf(domain, all_subs, live_subs)
            break
        elif choice == '2':
            write_to_csv(domain, all_subs, live_subs)
            break
        elif choice == '3':
            write_to_html(domain, all_subs, live_subs)
            break
        elif choice == '4':
            print(Fore.YELLOW + "[*] Export skipped.")
            break
        else:
            print(Fore.RED + "[!] Invalid option. Try again.")

def run_subdomain_discovery(target_domain):
    if not check_tool_installed("subfinder"):
        print(Fore.RED + "[-] Error: 'subfinder' not found.")
        return
    if not check_tool_installed("httpx-toolkit"):
        print(Fore.RED + "[-] Error: 'httpx-toolkit' not found.")
        return

    subdomain_file = f"sub{target_domain}.txt"
    live_subdomain_file = f"sub{target_domain}s_alive.txt"

    try:
        print(Fore.GREEN + f"[+] Running subfinder on {target_domain}...")
        subfinder_cmd = ["subfinder", "-d", target_domain, "-all", "-recursive"]
        with open(subdomain_file, "w") as f:
            result = subprocess.run(subfinder_cmd, stdout=f, stderr=subprocess.PIPE, text=True)
        if result.stderr:
            print(Fore.YELLOW + "[-] Subfinder warnings/errors:", result.stderr)

        if not os.path.exists(subdomain_file) or os.path.getsize(subdomain_file) == 0:
            print(Fore.RED + f"[-] No subdomains found for {target_domain}.")
            return

        print(Fore.GREEN + f"[+] Filtering live subdomains with httpx-toolkit...")
        httpx_cmd = ["httpx-toolkit", "-ports", "80,443,8080,8000,8888", "-threads", "200"]
        with open(subdomain_file, "r") as input_file, open(live_subdomain_file, "w") as output_file:
            result = subprocess.run(httpx_cmd, stdin=input_file, stdout=output_file, stderr=subprocess.PIPE, text=True)
        if result.stderr:
            print(Fore.YELLOW + "[-] httpx-toolkit warnings/errors:", result.stderr)

        all_subdomains = []
        live_subdomains = []

        with open(subdomain_file, "r") as f:
            all_subdomains = [line.strip() for line in f if line.strip()]

        if os.path.exists(live_subdomain_file) and os.path.getsize(live_subdomain_file) > 0:
            with open(live_subdomain_file, "r") as f:
                live_subdomains = [line.strip() for line in f if line.strip()]
            print(Fore.GREEN + f"[+] Live subdomains saved to {live_subdomain_file}:")
            print("\n".join(live_subdomains))
        else:
            print(Fore.RED + f"[-] No live subdomains found for {target_domain}.")

        export_menu(target_domain, all_subdomains, live_subdomains)

    except Exception as e:
        print(Fore.RED + f"[-] Error during subdomain discovery: {str(e)}")
    finally:
        if os.path.exists(subdomain_file):
            print(Fore.YELLOW + f"[!] Intermediate file {subdomain_file} retained.")

def main():
    clear_screen()
    while True:
        print(Fore.MAGENTA + "\n=== Subdomain Scanner Menu ===")
        print(Fore.YELLOW + "1. Scan a domain")
        print("2. Exit")
        choice = input(Fore.BLUE + "Choose an option (1/2): ").strip()

        if choice == '1':
            target_domain = input(Fore.BLUE + "\nEnter target domain (e.g., example.com): ").strip()
            if not target_domain:
                print(Fore.RED + "[-] Target domain cannot be empty.")
                continue
            run_subdomain_discovery(target_domain)
        elif choice == '2':
            print(Fore.GREEN + "[+] Exiting. Goodbye!")
            break
        else:
            print(Fore.RED + "[!] Invalid choice. Try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Program terminated by user.")
        sys.exit(0)
