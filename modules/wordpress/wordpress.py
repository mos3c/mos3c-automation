from colorama import Fore, Style
import subprocess
import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def check_dependencies():
    result = subprocess.run("command -v wpscan", shell=True, capture_output=True)
    if result.returncode != 0:
        print(Fore.RED + "[!] WPScan is not installed or not in PATH.")
        install = input(Fore.YELLOW + "Do you want to install WPScan now? (yes/no): ").lower()
        if install == 'yes':
            try:
                subprocess.run("sudo gem install wpscan", shell=True, check=True)
                print(Fore.GREEN + "[+] WPScan installed successfully!")
            except subprocess.CalledProcessError:
                print(Fore.RED + "[!] Failed to install WPScan. Please install it manually.")
                return False
        else:
            print(Fore.RED + "[!] WPScan is required. Exiting to main menu.")
            return False
    return True

def wp_enum_menu():
    clear_screen()
    print(Fore.BLUE + Style.BRIGHT + "─" * 65)
    print(Fore.WHITE + Style.BRIGHT + "WordPress Enumeration Module")
    print(Fore.BLUE + Style.BRIGHT + "─" * 65)

    if not check_dependencies():
        return

    target_url = input(Fore.YELLOW + "Enter the WordPress site URL (e.g., https://example.com): ").strip()
    api_token = input(Fore.YELLOW + "Enter your WPScan API token: ").strip()

    print(Fore.GREEN + f"[+] Running WPScan on: {target_url}\n")
    command = [
        "wpscan",
        "--url", target_url,
        "--disable-tls-checks",
        "--api-token", api_token,
        "-e", "at", "-e", "ap", "-e", "u",
        "--enumerate", "ap",
        "--plugins-detection", "aggressive",
        "--force"
    ]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"[!] WPScan failed: {e}")
    except FileNotFoundError:
        print(Fore.RED + "[!] WPScan not found. Please install it manually.")

if __name__ == '__main__':
    wp_enum_menu()
