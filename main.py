import requests, os, sys, colorama
from colorama import Fore, Back
colorama.init(autoreset=True)

apikey = "" # CriminalIP API Key 

def main():
    vulnerable = []
    safe = []
    os.system("title [IP Mass CriminalIP Vulnerability Scanner]")

    if ".txt" in sys.argv[1]:
        with open(sys.argv[1], "r") as f:
            for line in f:
                ip = line.strip()

                url = 'https://api.criminalip.io/v1/asset/ip/report'
                headers = {
                    "x-api-key": apikey
                }   

                params = {
                    'ip' : f"{ip}",
                    'full' : True
                }

                r = requests.request("GET", url, headers=headers, params=params)   
                result = r.json()
                
                if r.status_code == 500:
                    print(Fore.RED + "[-] Internal Server Error")
                    input("Please press ENTER to continue")
                    continue

                try:
                    if result['vulnerability']['count'] > 0:
                        print(f"{Fore.RED}[+] {ip} is vulnerable with {result['vulnerability']['count']} vulnerabilities")
                        vulnerable.append(ip)
                    else:
                        print(f"{Fore.LIGHTCYAN_EX}[-] {ip} is not vulnerable")
                        safe.append(ip)
                except KeyError:
                    print(f"{Fore.LIGHTCYAN_EX}[-] {ip} is not vulnerable")
                    safe.append(ip)

        x = input("Finished! Would you like to save the results? (y/n): ")
        if x.lower() == "y":
            try:
                with open("vulnerable_IPs.txt", "w") as f:
                    for ip in vulnerable:
                        f.write(f"{ip}\n")
                print("Saved vulnerable_IPs.txt")
            except Exception as e:
                print(f"Error saving vulnerable_IPs.txt: {e}")

            try:
                with open("safe_IPs.txt", "w") as f:
                    for ip in safe:
                        f.write(f"{ip}\n")
                print("Saved safe_IPs.txt")
            except Exception as e:
                print(f"Error saving safe_IPs.txt: {e}")

        else:
            print("Exiting...")
            exit(0)
    else:
        print("Usage: python main.py <iplists.txt>")
        input()

if __name__ == "__main__":
    try:
        ip_list_file = sys.argv[1]
        print(f"Scanning {len(open(ip_list_file, 'r').readlines())} IPs")
        main()
    except IndexError:
        print("Usage: python main.py <iplists.txt>")
        input()
        sys.exit()