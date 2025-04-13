import os
import tkinter as tk
from tkinter import filedialog

def get_urls_from_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select a text file with URLs", filetypes=[("Text Files", "*.txt")])
    if not file_path:
        return []
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]
    return urls

def select_download_directory():
    root = tk.Tk()
    root.withdraw()
    download_path = filedialog.askdirectory(title="Select Download Folder")
    return os.path.abspath(download_path) if download_path else None