import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import subprocess

def open_file(file_path, output_area):
    with open(file_path, 'r') as file:
        content = file.read()
        output_area.delete(1.0, tk.END)
        output_area.insert(tk.END, content)

def create_menu(parent, label):
    menu = tk.Menu(parent, tearoff=0)
    parent.add_cascade(label=label, menu=menu)
    return menu

def show_about():
    messagebox.showinfo("About", "Web-Enumeration Scan Program\nVersion 1.0\n(c) 2024 Spandan")

def exit_program():
    root.destroy()

def run_webscan():
    process = subprocess.Popen(["python", "webscan.py"])
    process.wait()
    open_file("webscan_output.txt", output_area)

def run_subdomainscan():
    process = subprocess.Popen(["python", "subdomainscan.py"])
    process.wait()
    open_file("subdomainscan.txt", output_area)

def run_wordlistgenerator():
    process = subprocess.Popen(["python", "wordlistgenerator.py"])
    process.wait()


def main():
    global root
    root = tk.Tk()
    root.title("Python Menu Program")

    menu_bar = tk.Menu(root)

    file_menu = create_menu(menu_bar, "File Enumeration")
    file_menu.add_command(label="Sub-directory Enumeration", command=run_webscan)
    file_menu.add_command(label="Sub-domain Enumeration", command=run_subdomainscan)
    file_menu.add_command(label="Wordlist Generator", command=run_wordlistgenerator)

    help_menu = create_menu(menu_bar, "Help")
    help_menu.add_command(label="About", command=show_about)
    help_menu.add_command(label="Exit", command=exit_program)

    root.config(menu=menu_bar)

    global output_area
    output_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=200, height=100)
    output_area.pack(padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()