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


def choose_recording():
    root = tk.Tk()
    root.withdraw()
    # Open the file dialog for a single CSV file selection
    file_path = filedialog.askopenfilename(filetypes=[("SVO files", "*.svo")])
    if file_path:
        return file_path
    else:
        print("No SVO file selected.")
        return None

