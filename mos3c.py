from colorama import Fore, Style, init
import os
import subprocess
import sys
from time import sleep

# Clear screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Menu Interface
def intro():
    while True:
        clear_screen()
        print()
        print(Fore.WHITE + Style.BRIGHT + "─" * 65)
        print(Fore.BLUE + Style.BRIGHT + 'MOSEC - WEB VULN FRAMEWORK')
        print(Fore.WHITE + Style.BRIGHT + "─" * 65)

        border_color = Fore.BLUE + Style.BRIGHT
        option_color = Fore.WHITE + Style.BRIGHT 
        print(border_color + "┌" + "─" * 63 + "┐")

        options = [
            "1]  Advanced Recon methodology",
            "2]  SQL injection",
            "3]  WP Enumeration",
            "4]  Emails Scanner",
            "5]  Network Scanning",
            "6]  Subdomain Scanner",
            "7]  Wayback URLs",
            "8]  Exit"
        ]

        for option in options:
            print(border_color + "│ " + option_color + option.ljust(60) + border_color + "  │")

        try:
            choice = input(Fore.BLUE + Style.BRIGHT + 'ENTER NUMBER TO CONTINUE : ').strip()

            if choice == '1':
                script_path = "modules/recon/mosec_recon.py"
                if not os.path.exists(script_path):
                    print(Fore.RED + f"[-] Error: {script_path} not found.")
                else:
                    print(Fore.GREEN + "[+] Launching Advanced Recon Methodology...")
                    subprocess.run([sys.executable, script_path])
                input(Fore.BLUE + "\nPress Enter to continue...")
            elif choice == '2':
                script_path = "modules/sqli/mos3c_sqli.py"
                if not os.path.exists(script_path):
                    print(Fore.RED + f"[-] Error: {script_path} not found.")
                else:
                    print(Fore.GREEN + "[+] Launching SQL injection module...")
                    subprocess.run([sys.executable, script_path])
                input(Fore.BLUE + "\nPress Enter to continue...")
            elif choice == '3':
                script_path = "modules/wordpress/wordpress.py"
                if not os.path.exists(script_path):
                    print(Fore.RED + f"[-] Error: {script_path} not found.")
                else:
                    print(Fore.YELLOW + "[!] Launching WP Enumeration module...")
                    subprocess.run([sys.executable, script_path])
                input(Fore.BLUE + "\nPress Enter to continue...")
            elif choice == '4':
                print(Fore.YELLOW + "[!] Emails Scanner module not implemented yet.")
                input(Fore.BLUE + "\nPress Enter to continue...")
            elif choice == '5':
                script_path = "modules/network_scanning/mos3c_network_scan.py"
                if not os.path.exists(script_path):
                    print(Fore.RED + f"[-] Error: {script_path} not found.")
                else:
                    print(Fore.GREEN + "[+] Launching SQL injection module...")
                    subprocess.run([sys.executable, script_path])
                input(Fore.BLUE + "\nPress Enter to continue...")
            elif choice == '6':
                print(Fore.YELLOW + "[!] Subdomain Scanner module not implemented yet.")
                input(Fore.BLUE + "\nPress Enter to continue...")
            elif choice == '7':
                print(Fore.YELLOW + "[!] Wayback URLs module not implemented yet.")
                input(Fore.BLUE + "\nPress Enter to continue...")
            elif choice == '8':
                print(Fore.RED + Style.BRIGHT + 'EXITING...')
                print(Fore.RED + Style.BRIGHT + 'THANKS FOR HUNTING WITH US')
                break
            else:
                print(Fore.RED + "[!] Invalid choice. Try again.")
                input(Fore.BLUE + "\nPress Enter to continue...")
        except KeyboardInterrupt:
            print(Fore.RED + "\n[!] Operation cancelled by user.")
            input(Fore.BLUE + "\nPress Enter to continue...")

# Main Entry
def main():
    init(autoreset=True)
    intro()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Program terminated by user.")
        sys.exit(0)