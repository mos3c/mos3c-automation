from colorama import Fore, Style, init
import subprocess
import os
import sys

init(autoreset=True)

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def Scan_menu():
    while True:
        clear_screen()
        print(Fore.BLUE + Style.BRIGHT + "─" * 65)
        print(Fore.WHITE + Style.BRIGHT + "ADVANCE RECONNAISSANCE")
        print(Fore.BLUE + Style.BRIGHT + "─" * 65)

        options = [
            "1]  Performs a full port scan using Nmap.",
            "2]  Scans for open ports and services using Masscan.",
            "3]  Return to Previous Menu / Exit."
        ]

        for option in options:
            print(f"{Fore.BLUE}│ {Fore.WHITE}{option.ljust(62)}{Fore.BLUE} │")

        print(Fore.BLUE + "─" * 65)

        try:
            choice = input(Fore.BLUE + Style.BRIGHT + "\nSELECT OPTION: ").strip()

            if choice == '1':
                print(Fore.GREEN + "[+] Launching Nmap Full Scan...")
                script_path = "modules/network_scanning/nmap.py"
                if not os.path.exists(script_path):
                    print(Fore.RED + f"[-] Error: {script_path} not found.")
                else:
                    subprocess.run([sys.executable, script_path])
                input(Fore.BLUE + "\nPress Enter to continue...")

            elif choice == '2':
                print(Fore.GREEN + "[+] Launching Masscan Scan...")
                script_path = "modules/network_scanning/masscan.py"
                if not os.path.exists(script_path):
                    print(Fore.RED + f"[-] Error: {script_path} not found.")
                else:
                    subprocess.run([sys.executable, script_path])
                input(Fore.BLUE + "\nPress Enter to continue...")

            elif choice == '3':
                print(Fore.YELLOW + "[*] Returning to previous menu...")
                break

            else:
                print(Fore.RED + "[-] Invalid option, try again.")
                input(Fore.BLUE + "\nPress Enter to continue...")

        except KeyboardInterrupt:
            print(Fore.RED + "\n[!] Operation cancelled by user.")
            input(Fore.BLUE + "\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        Scan_menu()
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Program terminated by user.")
        sys.exit(0)
