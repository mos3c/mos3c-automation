# modules/mosec_sqli.py

from colorama import Fore, Style
import subprocess
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def check_dependencies(tools):
    missing = []
    for tool in tools:
        # Step 1: Check if the tool exists in PATH
        result = subprocess.run(f"command -v {tool}", shell=True, capture_output=True)
        if result.returncode != 0:  # Tool not found
            missing.append(tool)
        else:
            # Step 2: For Python tools, test if they run without import errors
            if tool in ["uro", "ghauri", "sqlmap"]:  # Known Python-based tools
                try:
                    subprocess.run(f"{tool} --version", shell=True, capture_output=True, check=True, timeout=5)
                except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                    missing.append(tool)  # Add to missing if it fails to run
    
    if missing:
        print(Fore.RED + "[!] Missing or broken dependencies: " + ", ".join(missing))
        for tool in missing:
            install_choice = input(Fore.YELLOW + f"Do you want to install {tool}? (yes/no): ").lower()
            if install_choice == 'yes':
                print(Fore.GREEN + f"[+] Attempting to install {tool}...")               
                if tool == "subfinder":
                    install_cmd = "go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"
                elif tool == "gau":
                    install_cmd = "go install github.com/lc/gau/v2/cmd/gau@latest"
                elif tool == "uro":
                    install_cmd = "pip3 install git+https://github.com/s0md3v/uro.git"
                elif tool == "gf":
                    install_cmd = "go install github.com/tomnomnom/gf@latest"
                elif tool == "ghauri":
                    install_cmd = "pip3 install ghauri"
                elif tool == "urldedupe":
                    install_cmd = "go install github.com/ameenmaali/urldedupe@latest"
                elif tool == "httpx-toolkit":
                    install_cmd = "go install github.com/projectdiscovery/httpx/cmd/httpx@latest"
                elif tool == "sqlmap":
                    install_cmd = "git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git ~/sqlmap; ln -s ~/sqlmap/sqlmap.py /usr/local/bin/sqlmap"
                else:
                    install_cmd = f"apt install {tool}"  # Fallback (e.g., grep)
                
                try:
                    subprocess.run(install_cmd, shell=True, check=True)
                    print(Fore.GREEN + f"[+] {tool} installed successfully!")
                    # Re-check if it’s now functional
                    if tool in ["uro", "ghauri", "sqlmap"]:
                        subprocess.run(f"{tool} --version", shell=True, capture_output=True, check=True)
                    else:
                        subprocess.run(f"command -v {tool}", shell=True, capture_output=True, check=True)
                    missing.remove(tool)
                except subprocess.CalledProcessError:
                    print(Fore.RED + f"[!] Failed to install {tool}. Please install it manually.")
            elif install_choice == 'no':
                print(Fore.YELLOW + f"Skipping {tool} installation.")
            else:
                print(Fore.RED + "Invalid input. Skipping installation.")
        
        if missing:  # If any tools are still missing/broken
            print(Fore.RED + "Required tools are still missing or not functional. Returning to menu.")
            return False
    else:
        print(Fore.GREEN + "[+] All dependencies met: " + ", ".join(tools))
    return True

def sqli_menu():
    clear_screen()
    print(Fore.BLUE + Style.BRIGHT + "─" * 65)
    print(Fore.WHITE + Style.BRIGHT + "SQLi Testing Module")
    print(Fore.BLUE + Style.BRIGHT + "─" * 65)
    
    options = [
        "1]  Mass SQL injection testing using Ghauri",
        "2]  Comprehensive SQL injection testing using SQLmap",
        "3]  Single domain recon for potential SQL injectable endpoints",
        "4]  Multiple subdomain recon for SQL injection testing",
        "5]  Exit to Main Menu"
    ]
    
    for option in options:
        print(f"{Fore.BLUE}│ {Fore.WHITE}{option.ljust(62)}{Fore.BLUE} │")
    
    choice = input(Fore.BLUE + Style.BRIGHT + "SELECT SQLi OPTION: ")
    
    if choice == '1':
        # Mass SQLi with Ghauri
        url = input("Enter target URL (e.g., https://example.com): ")
        dependencies = ["subfinder", "gau", "uro", "gf", "ghauri"]
        if not check_dependencies(dependencies):
            return
        print(Fore.GREEN + "[+] Running mass SQLi testing with Ghauri...")
        domain = url.split('/')[2] if '//' in url else url  # Extracts domain from URL (e.g., example.com)
        RUN = f"subfinder -d {domain} -all -silent | gau --threads 50 | uro | gf sqli >sql.txt; ghauri -m sql.txt --batch --dbs --level 3 --confirm"
        subprocess.run(RUN, shell=True)
        
    elif choice == '2':
        url = input("Enter target URL (e.g., https://example.com): ")
        dependencies = ["subfinder", "gau", "urldedupe", "gf", "sqlmap"]
        if not check_dependencies(dependencies):
            return
        print(Fore.GREEN + "[+] Running comprehensive SQLi testing with SQLmap...")
        domain = url.split('/')[2] if '//' in url else url  # Extracts domain from URL
        RUN = f"subfinder -d {domain} -all -silent | gau | urldedupe | gf sqli >sql.txt; sqlmap -m sql.txt --batch --dbs --risk 2 --level 5 --random-agent"
        subprocess.run(RUN, shell=True)
        
    elif choice == '3':
        # Single domain recon
        domain = input("Enter target domain (e.g., example.com): ")
        dependencies = ["subfinder", "httpx-toolkit", "grep"]
        if not check_dependencies(dependencies):
            return
        print(Fore.GREEN + "[+] Running single domain recon for SQLi endpoints...")
        RUN = f"subfinder -d {domain} -all -silent | httpx-toolkit -td -sc -silent | grep -Ei 'asp|php|jsp|jspx|aspx'"
        subprocess.run(RUN, shell=True)
        
    elif choice == '4':
        # Multiple subdomain recon
        subdomain_file = input("Enter path to subdomain list file (e.g., subdomains.txt): ")
        dependencies = ["subfinder", "httpx-toolkit", "grep"]
        if not check_dependencies(dependencies):
            return
        print(Fore.GREEN + "[+] Running multiple subdomain recon for SQLi endpoints...")
        RUN = f"subfinder -d -l {subdomain_file} -all -silent | httpx-toolkit -td -sc -silent | grep -Ei 'asp|php|jsp|jspx|aspx'"
        subprocess.run(RUN, shell=True)
        
    elif choice == '5':
        print(Fore.GREEN + "Returning to main menu...")
        return
    
    else:
        print(Fore.RED + "Invalid option, try again.")
        sqli_menu()

if __name__ == "__main__":
    sqli_menu()