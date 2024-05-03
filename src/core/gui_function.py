import _tkinter
import tkinter as tk
import re

from functools import partial
from pathlib import Path
from tkinter import filedialog, messagebox

from models.library import recover_chr_name
import core.data_function as df


def change_state_widget(entry: tk.Entry, var_radio_b: tk.StringVar):
    if entry["state"] == tk.NORMAL and var_radio_b.get() == "nbr_probes":
        entry.config(state=tk.DISABLED)
    else:
        entry.config(state=tk.NORMAL)


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


def display_univ_primers_combobox(path: Path):
    univ_primer_dic = df.universal_primer_format(path)


def button_load_parameters(
    entry: tk.Entry, entries_dic: dict, values_widgets_dic: dict, input_parameters: dict
) -> None:
    src_folder_path = Path(__file__).absolute().parent
    if entry.get():
        param_path = Path(entry.get())
        input_parameters.update(df.load_parameters(param_path, src_folder_path))
        print(input_parameters)
        fill_entry_param(entry_dic=entries_dic, parameters=input_parameters)
        fill_values_widgets(
            values_widget_dic=values_widgets_dic, parameters=input_parameters
        )
    else:
        print("popup message error")


def fill_entry_param(entry_dic: dict, parameters: dict):
    for entry_name, entry in entry_dic.items():
        if entry_name == "output_folder" and not entry.get():
            parent_folder = (
                Path(__file__).absolute().parents[2].joinpath("Library_Design_Results")
            )
            entry.config(state=tk.NORMAL)
            entry.insert(0, str(parent_folder))
            entry.config(state=tk.DISABLED)
        elif parameters.get(entry_name):
            entry.config(state=tk.NORMAL)
            erase_entry(entry=entry)
            entry.insert(0, parameters.get(entry_name))
            entry.config(state=tk.DISABLED)


def fill_values_widgets(values_widget_dic: dict, parameters: dict):
    for str_var_name, var_widget in values_widget_dic.items():
        if parameters.get(str_var_name):
            var_widget.set(parameters.get(str_var_name))


def set_mess_box_error(param_name: str, type: str):
    messagebox.showerror(
        "Input error",
        f"The type of {param_name} is not correct.\nPlease enter an {type}.",
    )


def set_mess_box_warning(param_name: str):
    messagebox.showwarning(
        "Warning !",
        f"The {param_name} is not correct.\nPlease select a correct value.",
    )


def check_recover_settings(
    parameters: dict, entries_widgets: dict, var_widgets: dict
) -> None:
    """Return True if all parameters have good type expected, else return False with a pop-up error window"""
    # update of entry values in input_parameters
    for entry_name, entry in entries_widgets.items():
        if entry_name != "chromosome_file":
            parameters.update({entry_name: Path(entry.get())})
        else:
            parameters.update({entry_name: entry.get()})

    # update of values (textvariables) in input_parameters
    for var_name, var_wid in var_widgets.items():
        if var_name == "design_type":
            parameters.update({var_name: var_wid.get()})
            try:
                parameters.update({"resolution": var_widgets.get("resolution").get()})
            except _tkinter.TclError:
                set_mess_box_error(param_name="locus size", type="integer")
        elif var_name == "nbr_bcd_rt_by_probe":
            try:
                parameters.update({var_name: var_wid.get()})
            except _tkinter.TclError:
                set_mess_box_error(
                    param_name="number of RTs/Brcds by probe", type="integer"
                )
        elif var_name == "bcd_rt_file":
            parameters.update({var_name: var_wid.get()})
        elif var_name == "nbr_probe_by_locus":
            try:
                parameters.update({var_name: var_wid.get()})
            except _tkinter.TclError:
                set_mess_box_error(
                    param_name="number of probes by locus", type="integer"
                )
        elif var_name == "start_lib":
            try:
                parameters.update({var_name: var_wid.get()})
            except _tkinter.TclError:
                set_mess_box_error(
                    param_name="Library starting coordinates", type="integer"
                )
        elif var_name == "nbr_loci_total":
            try:
                parameters.update({var_name: var_wid.get()})
            except _tkinter.TclError:
                set_mess_box_error(param_name="total loci", type="integer")
        elif var_name == "primer_univ":
            if var_wid.get() == "Choose universal primer couple":
                set_mess_box_warning(param_name="universal primer")
            else:
                parameters.update({var_name: var_wid.get()})
    print(parameters)
