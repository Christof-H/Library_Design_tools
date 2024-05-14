import _tkinter
import tkinter as tk
import re

from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from models.library import recover_chr_name
import core.data_function as df
from core.design_process import design_process


def change_state_widget(entry: tk.Entry, var_radio_b: tk.StringVar) -> None:
    if entry["state"] == tk.NORMAL and var_radio_b.get() == "nbr_probes":
        entry.config(state=tk.DISABLED)
    else:
        entry.config(state=tk.NORMAL)


def erase_entry(entry: tk.Entry) -> None:
    if entry.get():
        entry.delete(0, len(entry.get()))


def open_file_dialog(entry: tk.Entry) -> None:
    file_name = filedialog.askopenfilename(title="Select a file")
    if file_name:
        print("File selected :", file_name)
        entry.config(state=tk.NORMAL)
        erase_entry(entry)
        entry.insert(0, file_name)
        entry.config(state=tk.DISABLED)
    return file_name


def open_dialog_display_chr_name(entry_folder: tk.Entry, entry_name: tk.Entry) -> None:
    chr_path = Path(open_file_dialog(entry_folder))
    chr_name = recover_chr_name(str(chr_path))
    if chr_name:
        entry_name.config(state=tk.NORMAL)
        erase_entry(entry_name)
        entry_name.insert(0, chr_name)
        entry_name.config(state=tk.DISABLED)


def open_folder_dialog(entry: tk.Entry) -> None:
    folder_name = filedialog.askdirectory(title="Select a folder")
    if folder_name:
        print("Folder selected :", folder_name)
        entry.config(state=tk.NORMAL)
        erase_entry(entry)
        entry.insert(0, folder_name)
        entry.config(state=tk.DISABLED)


def display_univ_primers_combobox(path: Path) -> list[str]:
    univ_primer_dic = df.universal_primer_format(path)
    univ_primer_display = []
    for key, values in univ_primer_dic.items():
        univ_primer_string = f"{key} - {values[0]} - {values[2]}"
        univ_primer_display.append(univ_primer_string)
    return univ_primer_display


def button_load_parameters(
    entry: tk.Entry, entries_dic: dict, values_widgets_dic: dict, input_parameters: dict
) -> None:
    if entry.get():
        param_path = Path(entry.get())
        input_parameters.update(df.load_parameters(param_path))
        fill_entry_param(entry_dic=entries_dic, parameters=input_parameters)
        fill_values_widgets(
            values_widget_dic=values_widgets_dic, parameters=input_parameters
        )


def fill_entry_param(entry_dic: dict, parameters: dict) -> None:
    for entry_name, entry in entry_dic.items():
        if entry_name == "output_folder" and not entry.get():
            parent_folder = Path(__file__).absolute().parents[2]
            entry.config(state=tk.NORMAL)
            entry.insert(0, str(parent_folder))
            entry.config(state=tk.DISABLED)
        elif parameters.get(entry_name):
            entry.config(state=tk.NORMAL)
            erase_entry(entry=entry)
            entry.insert(0, parameters.get(entry_name))
            entry.config(state=tk.DISABLED)


def fill_values_widgets(values_widget_dic: dict, parameters: dict) -> None:
    for str_var_name, var_widget in values_widget_dic.items():
        if parameters.get(str_var_name):
            var_widget.set(parameters.get(str_var_name))


def set_mess_box_error(param_name: str, type: str) -> None:
    messagebox.showerror(
        title="Input error",
        message=f"The type of {param_name} is not correct.\nPlease enter an {type}.",
    )


def set_mess_box_warning(param_name: str) -> None:
    messagebox.showwarning(
        title="Warning !",
        message=f"The {param_name} is not correct.\nPlease select a correct value.",
    )


def check_recover_settings(
    parameters: dict, entries_widgets: dict, var_widgets: dict
) -> tuple[dict, bool]:
    valid_input = True
    # update of entry values in input_parameters (chr_file_path, chr_name, output_folder_path)
    for entry_name, entry in entries_widgets.items():
        if entry_name != "chromosome_file":
            if entry.get():
                parameters.update({entry_name: entry.get()})
            else:
                set_mess_box_warning(param_name="chr. or output path")
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
                valid_input = False
                set_mess_box_error(param_name="locus size", type="integer")
        elif var_name == "nbr_bcd_rt_by_probe":
            try:
                parameters.update({var_name: var_wid.get()})
            except _tkinter.TclError:
                valid_input = False
                set_mess_box_error(
                    param_name="number of RTs/brcds by probe", type="integer"
                )
        elif var_name == "bcd_rt_file":
            parameters.update({var_name: var_wid.get()})
        elif var_name == "nbr_probe_by_locus":
            try:
                parameters.update({var_name: var_wid.get()})
            except _tkinter.TclError:
                valid_input = False
                set_mess_box_error(
                    param_name="number of probes by locus", type="integer"
                )
        elif var_name == "start_lib":
            try:
                parameters.update({var_name: var_wid.get()})
            except _tkinter.TclError:
                valid_input = False
                set_mess_box_error(
                    param_name="Library starting coordinates", type="integer"
                )
        elif var_name == "nbr_loci_total":
            try:
                parameters.update({var_name: var_wid.get()})
            except _tkinter.TclError:
                valid_input = False
                set_mess_box_error(param_name="total loci", type="integer")
        elif var_name == "primer_univ":
            if var_wid.get() == "Choose universal primer couple":
                valid_input = False
                set_mess_box_warning(param_name="universal primer")
            else:
                primer_combobox_choice = var_wid.get()
                primer_univ = re.match(
                    r"(^primer\d{1,2})", primer_combobox_choice
                ).group(1)
                parameters.update({var_name: primer_univ})
    return parameters, valid_input


#
def display_graphic(widget: tk.Label, img_path: Path) -> None:
    img = tk.PhotoImage(file=img_path)
    img_zoom = img.zoom(6)
    img_resized = img_zoom.subsample(8)
    widget.configure(image=img_resized)
    # Keep a reference to the photo object to avoid deletion by the garbage collector : widget.image = img
    widget.image = img_resized


def fill_csv_board(
    master: tk.Frame,
    treeview: ttk.Treeview,
    tree_scroll: tk.Scrollbar,
    id_columns: list[str | int],
    column_names: list[str],
    values: list[list[str | int]],
) -> None:
    # Create columns
    treeview["columns"] = id_columns

    # Erase all rows if a design has already been done
    for row in treeview.get_children():
        treeview.delete(row)

    # fill in the column name for each column
    for id_col, name in zip(id_columns, column_names):
        treeview.heading(column=id_col, text=name)
        treeview.column(column=id_col, width=110, anchor=tk.CENTER)

    # fill in the values for each line
    i = 0
    for value in values:
        if i % 2 == 0:
            treeview.insert(parent="", index=tk.END, values=value, tags="even_row")
            i += 1
        else:
            treeview.insert(parent="", index=tk.END, values=value, tags="odd_row")
            i += 1
    treeview.tag_configure("odd_row", background="white")
    treeview.tag_configure("even_row", background="#EAF2F8")

    tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    treeview.pack()


def start_design(
    parameters: dict,
    entries_widgets: dict,
    var_widgets: dict,
    graphic_img_label: tk.Label,
    summary_img_label: tk.Label,
    frame_board: tk.Frame,
    treeview: ttk.Treeview,
    tree_scroll=tk.Scrollbar,
) -> None:
    updated_parameters, valid_input = check_recover_settings(
        parameters=parameters, entries_widgets=entries_widgets, var_widgets=var_widgets
    )
    if valid_input:
        design_process(
            output_folder=updated_parameters["output_folder"],
            inputs_parameters=updated_parameters,
        )
        # displays library information in graphical form
        graphic_img = updated_parameters["path_result_folder"].joinpath("plot.png")
        display_graphic(widget=graphic_img_label, img_path=graphic_img)

        # recovery detailed information from the library (for board visualisation)
        lib_summary_file_path = updated_parameters["path_result_folder"].joinpath(
            "3_Library_summary.csv"
        )
        sum_columns, sum_values = df.recover_summary(summary_path=lib_summary_file_path)

        # delete img_caution to place csv table where required
        summary_img_label.pack_forget()

        # displays library information in board form treeview_summary
        id_columns = list(range(len(sum_columns)))
        fill_csv_board(
            master=frame_board,
            treeview=treeview,
            id_columns=id_columns,
            column_names=sum_columns,
            values=sum_values,
            tree_scroll=tree_scroll,
        )
    else:
        print(
            "/!\ : The library design process did not take place because there must be a problem in the parameters"
        )
