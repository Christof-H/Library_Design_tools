import tkinter as tk
import re

from functools import partial
from pathlib import Path
from tkinter import filedialog

from models.library import recover_chr_name
import data_function as df


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


def button_load_parameters(entry: tk.Entry):
    # variable globale ????
    src_folder_path = Path(__file__).absolute().parent
    parameters = {}
    if entry.get():
        param_path = Path(entry.get())
        input_parameters = (df.load_parameters(param_path, src_folder_path))
        #print(input_parameters)
    return parameters

def display_univ_primers_combobox(path: Path):
    univ_primer_dic = df.universal_primer_format(path)


def fill_entry_param(entry: tk.Entry, input):
    pass


def recover_all_parameters():
    pass


def check_all_settings(entries_dic):
    """Return True if all parameters have good type expected, else return False with a pop-up error window"""
    pass
