from colorama import Fore, Style, init
import subprocess
import os
import sys

# Initialize colorama for colored output
init()

def clear_screen():
    """Clear the terminal screen (Linux)."""
    os.system('clear')

def Recon_menu():
    """Display the reconnaissance menu and handle user input."""
    while True:
        clear_screen()
        print(Fore.BLUE + Style.BRIGHT + "─" * 65)
        print(Fore.WHITE + Style.BRIGHT + "ADVANCE RECONNAISSANCE")
        print(Fore.BLUE + Style.BRIGHT + "─" * 65)

        options = [
            "1]  Subdomains Discovering and Filtering",
            "2]  Comprehensive SQL injection testing using SQLmap",
            "3]  Single domain recon for potential SQL injectable endpoints",
            "4]  Multiple subdomain recon for SQL injection testing",
            "5]  Exit to Main Menu"
        ]

        for option in options:
            print(f"{Fore.BLUE}│ {Fore.WHITE}{option.ljust(62)}{Fore.BLUE} │")

        try:
            choice = input(Fore.BLUE + Style.BRIGHT + "SELECT SQLi OPTION: ").strip()

            if choice == '1':
                print(Fore.GREEN + "[+] Launching Subdomains Discovering and Filtering...")
                script_path = "modules/recon/subdomain.py"
                if not os.path.exists(script_path):
                    print(Fore.RED + f"[-] Error: {script_path} not found.")
                else:
                    subprocess.run([sys.executable, script_path])
                input(Fore.BLUE + "\nPress Enter to continue...")
            elif choice == '2':
                print(Fore.YELLOW + "[!] SQLmap testing not implemented yet.")
                input(Fore.BLUE + "\nPress Enter to continue...")
            elif choice == '3':
                print(Fore.YELLOW + "[!] Single domain recon not implemented yet.")
                input(Fore.BLUE + "\nPress Enter to continue...")
            elif choice == '4':
                print(Fore.YELLOW + "[!] Multiple subdomain recon not implemented yet.")
                input(Fore.BLUE + "\nPress Enter to continue...")
            elif choice == '5':
                print(Fore.GREEN + "Returning to main menu...")
                break
            else:
                print(Fore.RED + "Invalid option, try again.")
                input(Fore.BLUE + "\nPress Enter to continue...")
        except KeyboardInterrupt:
            print(Fore.RED + "\n[!] Operation cancelled by user.")
            input(Fore.BLUE + "\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        Recon_menu()
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Program terminated by user.")
        sys.exit(0)