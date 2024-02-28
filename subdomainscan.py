import tkinter as tk
from tkinter import filedialog
import requests

class SubdomainScanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sub-domain Enumeration Scanner")

        # Frame for URL input
        self.url_frame = tk.Frame(root, padx=10, pady=10)
        self.url_frame.pack()

        self.url_label = tk.Label(self.url_frame, text="Enter the target URL:")
        self.url_label.grid(row=0, column=0)

        self.target_url_entry = tk.Entry(self.url_frame, width=40)
        self.target_url_entry.grid(row=0, column=1)

        # Frame for Wordlist selection
        self.wordlist_frame = tk.Frame(root, padx=10, pady=10)
        self.wordlist_frame.pack()

        self.wordlist_label = tk.Label(self.wordlist_frame, text="Select Wordlist:")
        self.wordlist_label.grid(row=0, column=0)

        self.wordlist_button = tk.Button(self.wordlist_frame, text="Browse", command=self.select_wordlist)
        self.wordlist_button.grid(row=0, column=1)

        # Run button
        self.run_button = tk.Button(root, text="Run Sub-domain Enumeration", command=self.run_subdomainscan)
        self.run_button.pack(pady=10)

    def select_wordlist(self):
        self.wordlist_file = filedialog.askopenfilename(title="Select Wordlist File", filetypes=[("Text files", "*.txt")])

    def run_subdomainscan(self):
        target_url = self.target_url_entry.get()

        output_file = "subdomainscan.txt"
        subdomain_enum(target_url, self.wordlist_file, output_file)

        # Close the application
        self.root.destroy()

def subdomain_enum(target_url, wordlist_file, output_file):
    with open(wordlist_file, 'r') as wordlist:
        words = wordlist.read().splitlines()
    with open(output_file, 'w') as output:
        for word in words:
            subdomain_https = f"https://{word}.{target_url}"
            try:
                requests.get(subdomain_https)
                status_code = requests.get(subdomain_https).status_code
                # output.write(f'{status_code} : {subdomain_https}\n')
                output.write(f"Target: {subdomain_https}\nStatus Code: {status_code}\n\n")
            except requests.RequestException:
                pass

if __name__ == "__main__":
    root = tk.Tk()
    app = SubdomainScanApp(root)
    root.mainloop()
