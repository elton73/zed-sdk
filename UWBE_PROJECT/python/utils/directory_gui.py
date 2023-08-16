import tkinter as tk
from tkinter import filedialog

def browse_directory():
    root = tk.Tk()
    root.withdraw()

    # Open the file dialog for directory selection
    directory_path = filedialog.askdirectory()

    if directory_path:
        return directory_path
    else:
        print("No directory selected.")
        return "q"