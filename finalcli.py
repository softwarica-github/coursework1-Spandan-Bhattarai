import sys
import requests

class WordlistGenerator:
    def __init__(self):
        self.mode_options = {
            "1": ("Subdomain Enumeration", "https://raw.githubusercontent.com/danTaler/WordLists/master/Subdomain.txt"),
            "2": ("Subdirectory Scanner", "https://raw.githubusercontent.com/v0re/dirb/master/wordlists/common.txt")
        }

    def generate_wordlist(self):
        print("Select mode:")
        for key, value in self.mode_options.items():
            print(f"{key}. {value[0]}")

        mode = input("Enter mode number: ")
        if mode in self.mode_options:
            mode_name, url = self.mode_options[mode]
            output_file = input("Enter output file name: ")
            if output_file:
                self.download_wordlist(url, output_file)
                print(f"Wordlist generated successfully: {output_file}\n")
        else:
            print("Invalid mode selection.")

    def download_wordlist(self, url, output_file):
        response = requests.get(url)
        if response.status_code == 200:
            with open(output_file, 'wb') as f:
                f.write(response.content)
        else:
            print(f"Failed to download wordlist from {url}")

class Scanner:
    def __init__(self):
        pass

    def scan(self, target_url, wordlist_file):
        raise NotImplementedError("Subclasses must implement scan method.")

class SubdomainScanner(Scanner):
    def scan(self, target_url, wordlist_file):
        with open(wordlist_file, 'r') as wordlist:
            words = wordlist.read().splitlines()

        output_file = input("Enter output file name: ")
        if output_file:
            with open(output_file, 'w') as output:
                for word in words:
                    subdomain_https = f"https://{word}.{target_url}"
                    try:
                        requests.get(subdomain_https)
                        status_code = requests.get(subdomain_https).status_code
                        output.write(f"Target: {subdomain_https}\nStatus Code: {status_code}\n\n")
                    except requests.RequestException:
                        pass
        
        print("The output has been saved to:", wordlist_file,"\n")

class SubdirectoryScanner(Scanner):
    def scan(self, target_url, wordlist_file, output_file):
        with open(wordlist_file, 'r') as wordlist:
            words = wordlist.read().splitlines()

        with open(output_file, 'w') as output:
            for word in words:
                url = f"{target_url}/{word}"
                try:
                    response = requests.get(url, verify=True)
                    response.raise_for_status()  # Raises an HTTPError for non-2xx status codes
                    status_code = response.status_code
                    output.write(f"Target: {url}\nStatus Code: {status_code}\n\n")
                except requests.RequestException as e:
                    # print(f"Failed {url}: {e}")
                    pass

        print("The output has been saved to:", output_file, "\n")

def main():
    if len(sys.argv) == 1:
        while True:
            print("Choose an option:")
            print("1. Subdirectory Scan")
            print("2. Subdomain Scan")
            print("3. Wordlist Generator")
            print("4. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                target_url = input("Enter the target URL: ")
                wordlist_file = input("Enter wordlist filename: ")
                output_file = input("Enter output filename to save successful scans: ")
                scanner = SubdirectoryScanner()
                scanner.scan(target_url, wordlist_file, output_file)
            elif choice == "2":
                target_url = input("Enter the target URL: ")
                wordlist_file = input("Enter wordlist filename: ")
                scanner = SubdomainScanner()
                scanner.scan(target_url, wordlist_file)
            elif choice == "3":
                generator = WordlistGenerator()
                generator.generate_wordlist()
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please choose again.")
    else:
        choice = sys.argv[1]
        if choice == "1":
            target_url = input("Enter the target URL: ")
            wordlist_file = input("Enter wordlist filename: ")
            output_file = input("Enter output filename to save successful scans: ")
            scanner = SubdirectoryScanner()
            scanner.scan(target_url, wordlist_file, output_file)
        elif choice == "2":
            target_url = input("Enter the target URL: ")
            wordlist_file = input("Enter wordlist filename: ")
            scanner = SubdomainScanner()
            scanner.scan(target_url, wordlist_file)
        elif choice == "3":
            generator = WordlistGenerator()
            generator.generate_wordlist()
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    import pyfiglet
    from termcolor import colored

    font = pyfiglet.Figlet(font='slant')
    print(colored(font.renderText('         Web'),'red'))
    print(colored(font.renderText('Enumerator'),'red'))

    print(" "*38,"BY Spandan Bhattarai",)
    print("[+] Github: https://github.com/Spandan-Bhattarai\n")
    main()
