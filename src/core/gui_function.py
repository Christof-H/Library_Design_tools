import tkinter as tk
import re

from functools import partial
from pathlib import Path
from tkinter import filedialog

from models.library import recover_chr_name


def erase_entry(entry: tk.Entry):
    if entry.get():
        entry.delete(0, len(entry.get()))


def open_file_dialog(entry: tk.Entry):
    file_name = filedialog.askopenfilename(title="Select a file")
    if file_name:
        print("File selected :", file_name)
        entry.config(state=tk.NORMAL)
        erase_entry(entry)
        entry.insert(0, file_name)
        entry.config(state=tk.DISABLED)
    return file_name


def open_dialog_display_chr_name(entry_folder: tk.Entry, entry_name: tk.Entry):
    chr_path = Path(open_file_dialog(entry_folder))
    chr_name = recover_chr_name(str(chr_path))
    if chr_name:
        entry_name.config(state=tk.NORMAL)
        erase_entry(entry_name)
        entry_name.insert(0, chr_name)
        entry_name.config(state=tk.DISABLED)


def open_folder_dialog(entry: tk.Entry):
    folder_name = filedialog.askdirectory(title="Select a folder")
    if folder_name:
        print("Folder selected :", folder_name)
        entry.config(state=tk.NORMAL)
        erase_entry(entry)
        entry.insert(0, folder_name)
        entry.config(state=tk.DISABLED)
