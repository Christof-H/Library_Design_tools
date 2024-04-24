import tkinter as tk
from tkinter import ttk


class AppInterface(tk.Tk):
    def __init__(
        self,
        dim_width=500,
        dim_height=300,
        width_resize=False,
        height_resize=False,
        tabs=False,
    ):
        super().__init__()
        self.title("Library Design")
        self.width = dim_width
        self.height = dim_height
        self.width_resize = width_resize
        self.height_resize = height_resize
        self.resizable(width=self.width_resize, height=self.height_resize)
        self.minsize(width=self.width, height=self.height)
        if tabs:
            self.create_notebook()
        else:
            self.notebook = None

    def create_notebook(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

    def create_frame_in_notebook(self, title):
        tab = ttk.Frame(master=self.notebook, width=self.width, height=self.height)
        tab.pack(fill="both", expand=True)
        self.notebook.add(tab, text=title)
        return tab

    def create_labelframe(self, parent, text, height):
        labelframe = tk.LabelFrame(
            master=parent, text=text, width=self.width, height=height
        )
        labelframe.pack(pady=10, padx=20, fill="both")
        return labelframe

    def create_label_img(self, master, image_path, resize_rate, column, row):
        img = tk.PhotoImage(file=image_path)
        img_resized = img.subsample(resize_rate)
        label_img = tk.Label(master=master, image=img_resized)
        label_img.grid(column=column, row=row)
        return label_img, img_resized

    def create_label(self, master, text, column, row, sticky, pady=5, padx=5):
        label = tk.Label(master=master, text=text, pady=pady, padx=padx)
        label.grid(sticky=sticky, column=column, row=row)
        return label

    def create_enty(
        self, master, width, column, row, pady=None, padx=None, sticky=None
    ):
        input = tk.Entry(master=master, width=width)
        input.grid(column=column, row=row, pady=pady, padx=padx, sticky=sticky)
        return input

    def create_button(
        self, master, text, column, row, pady=None, padx=None, sticky=None, command=None
    ):
        button = tk.Button(master=master, text=text, command=command)
        button.grid(column=column, row=row, pady=pady, padx=padx, sticky=sticky)
        return button


def main_gui():
    # creating the main window with a Notebook
    my_gui = AppInterface(tabs=True, dim_width=1000, dim_height=650)
    #######################################################################################
    #               creating of the different tabs in the Notebook
    #######################################################################################
    tab_param = my_gui.create_frame_in_notebook("Parameters")
    tab_graphic = my_gui.create_frame_in_notebook("Graphic result")
    tab_board = my_gui.create_frame_in_notebook("Library details")

    #######################################################################################
    #               creating of the different Labelframe in the Parameters tab
    #######################################################################################
    labelframe_file = my_gui.create_labelframe(
        parent=tab_param, text="Files/Folders", height=200
    )
    labelframe_param = my_gui.create_labelframe(
        parent=tab_param, text="Library parameters", height=400
    )
    #######################################################################################
    #               creating of the different widgets in the File/Folder LabelFrame
    #######################################################################################
    info_load_param, info_img = my_gui.create_label_img(
        master=labelframe_file,
        image_path="../resources/info.png",
        resize_rate=4,
        column=0,
        row=0,
    )
    info_chr_folder, chr_folder_img = my_gui.create_label_img(
        master=labelframe_file,
        image_path="../resources/info.png",
        resize_rate=4,
        column=0,
        row=1,
    )
    info_chr_name, chr_name_img = my_gui.create_label_img(
        master=labelframe_file,
        image_path="../resources/info.png",
        resize_rate=4,
        column=0,
        row=2,
    )
    info_output, output_img = my_gui.create_label_img(
        master=labelframe_file,
        image_path="../resources/info.png",
        resize_rate=4,
        column=0,
        row=3,
    )
    label_input_param = my_gui.create_label(
        labelframe_file,
        text="Load input parameters :",
        column=1,
        row=0,
        sticky=tk.W,
    )
    label_chr_path = my_gui.create_label(
        labelframe_file,
        text="Chromosome folder path :",
        column=1,
        row=1,
        sticky=tk.W,
    )
    label_chr_name = my_gui.create_label(
        labelframe_file,
        text="Chromosome file name :",
        column=1,
        row=2,
        pady=5,
        sticky=tk.W,
    )
    label_output_path = my_gui.create_label(
        labelframe_file,
        text="Output folder path :",
        column=1,
        row=3,
        pady=5,
        sticky=tk.W,
    )
    entry_input = my_gui.create_enty(master=labelframe_file, width=50, column=2, row=0)
    entry_chr_folder = my_gui.create_enty(
        master=labelframe_file, width=50, column=2, row=1
    )
    entry_chr_name = my_gui.create_enty(
        master=labelframe_file, width=20, column=2, row=2, sticky=tk.W
    )
    entry_output = my_gui.create_enty(master=labelframe_file, width=50, column=2, row=3)

    button_open_file = my_gui.create_button(
        labelframe_file, text="Open file", column=3, row=0, padx=10, sticky=tk.EW
    )
    button_load_param = my_gui.create_button(
        labelframe_file, text="Load parameters", column=4, row=0, padx=10
    )
    button_load_param = my_gui.create_button(
        labelframe_file, text="Choose folder", column=3, row=1, padx=10
    )
    button_output = my_gui.create_button(
        labelframe_file, text="Choose folder", column=3, row=3, padx=10
    )
    #######################################################################################
    #               creating of the different widgets in the Library parameters LabelFrame
    #######################################################################################

    #                                   info image label
    #######################################################################################
    info_design, info_design_img = my_gui.create_label_img(
        master=labelframe_param,
        image_path="../resources/info.png",
        resize_rate=4,
        column=0,
        row=0,
    )
    info_labelling, info_labelling_img = my_gui.create_label_img(
        master=labelframe_param,
        image_path="../resources/info.png",
        resize_rate=4,
        column=0,
        row=3,
    )
    info_nbr_rt, nbr_rt_img = my_gui.create_label_img(
        master=labelframe_param,
        image_path="../resources/info.png",
        resize_rate=4,
        column=0,
        row=6,
    )
    info_nbr_probe, nbr_probe_img = my_gui.create_label_img(
        master=labelframe_param,
        image_path="../resources/info.png",
        resize_rate=4,
        column=3,
        row=0,
    )
    info_total_loci, total_loci_img = my_gui.create_label_img(
        master=labelframe_param,
        image_path="../resources/info.png",
        resize_rate=4,
        column=3,
        row=1,
    )
    info_lib_start, lib_start_img = my_gui.create_label_img(
        master=labelframe_param,
        image_path="../resources/info.png",
        resize_rate=4,
        column=3,
        row=2,
    )
    info_univ_primer, univ_primer_img = my_gui.create_label_img(
        master=labelframe_param,
        image_path="../resources/info.png",
        resize_rate=4,
        column=3,
        row=3,
    )
    #                                   Text labels
    #######################################################################################

    my_gui.mainloop()


if __name__ == "__main__":
    main_gui()
