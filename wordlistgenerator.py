import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import os

class WordlistGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wordlist Generator")

        # Frame for URL input
        self.mode_frame = tk.Frame(root, padx=10, pady=10)
        self.mode_frame.pack()

        self.mode_label = tk.Label(self.mode_frame, text="Select Mode:")
        self.mode_label.grid(row=0, column=0)

        self.mode_var = tk.StringVar()
        self.mode_var.set("Subdomain Enumeration")

        self.mode_options = ["Subdomain Enumeration", "Subdirectory Scanner", "Custom Wordlist"]
        self.mode_menu = tk.OptionMenu(self.mode_frame, self.mode_var, *self.mode_options)
        self.mode_menu.grid(row=0, column=1)

        # Run button
        self.run_button = tk.Button(root, text="Generate Wordlist", command=self.generate_wordlist)
        self.run_button.pack(pady=10)

    def generate_wordlist(self):
        mode = self.mode_var.get()

        if mode == "Subdomain Enumeration":
            url = "https://raw.githubusercontent.com/danTaler/WordLists/master/Subdomain.txt"
            output_file = "subdomain.txt"
        elif mode == "Subdirectory Scanner":
            url = "https://raw.githubusercontent.com/v0re/dirb/master/wordlists/common.txt"
            output_file = "subdirectory.txt"
        elif mode == "Custom Wordlist":
            self.open_custom_wordlist_window()
            return

        self.download_wordlist(url, output_file)
        messagebox.showinfo("Wordlist Generated", f"Wordlist generated successfully: {output_file}")

    def download_wordlist(self, url, output_file):
        response = requests.get(url)
        if response.status_code == 200:
            with open(output_file, 'wb') as f:
                f.write(response.content)
        else:
            messagebox.showerror("Error", f"Failed to download wordlist from {url}")

    def open_custom_wordlist_window(self):
        CustomWordlistWindow()

class CustomWordlistWindow:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Custom Wordlist Generator")

        self.letters_label = tk.Label(self.window, text="Letters:")
        self.letters_label.grid(row=0, column=0)

        self.letters_entry = tk.Entry(self.window)
        self.letters_entry.grid(row=0, column=1)

        self.min_length_label = tk.Label(self.window, text="Min Length:")
        self.min_length_label.grid(row=1, column=0)

        self.min_length_entry = tk.Entry(self.window)
        self.min_length_entry.grid(row=1, column=1)

        self.max_length_label = tk.Label(self.window, text="Max Length:")
        self.max_length_label.grid(row=2, column=0)

        self.max_length_entry = tk.Entry(self.window)
        self.max_length_entry.grid(row=2, column=1)

        self.generate_button = tk.Button(self.window, text="Generate", command=self.generate_wordlist)
        self.generate_button.grid(row=3, columnspan=2)

    def generate_wordlist(self):
        letters = self.letters_entry.get()
        min_length = int(self.min_length_entry.get())
        max_length = int(self.max_length_entry.get())

        wordlist = self.generate_wordlist_from_input(letters, min_length, max_length)

        output_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if output_file:
            with open(output_file, 'w') as f:
                f.write('\n'.join(wordlist))
            messagebox.showinfo("Wordlist Generated", f"Wordlist generated successfully: {output_file}")
            self.window.destroy()

    def generate_wordlist_from_input(self, letters, min_length, max_length):
        wordlist = []

        for length in range(min_length, max_length + 1):
            self._generate_wordlist_recursive(letters, "", length, wordlist)

        return wordlist

    def _generate_wordlist_recursive(self, letters, current_word, length, wordlist):
        if length == 0:
            wordlist.append(current_word)
            return

        for char in letters:
            self._generate_wordlist_recursive(letters, current_word + char, length - 1, wordlist)

if __name__ == "__main__":
    root = tk.Tk()
    app = WordlistGeneratorApp(root)
    root.mainloop()
