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

    def create_labelframe(self, parent, mytext, myheight):
        labelframe = tk.LabelFrame(
            master=parent, text=mytext, width=self.width, height=myheight
        )
        labelframe.pack(pady=10, padx=20, fill="both")
        return labelframe

    def create_label(self, master):
        label = tk.Label(master=master, text="mon texte")
        label.pack()
        return label


def main_gui():
    my_gui = AppInterface(tabs=True, dim_width=1000, dim_height=650)
    tab_param = my_gui.create_frame_in_notebook("Parameters")
    tab_graphic = my_gui.create_frame_in_notebook("Graphic result")
    tab_board = my_gui.create_frame_in_notebook("Library details")
    labelframe_file = my_gui.create_labelframe(
        parent=tab_param, mytext="Files/Folders", myheight=200
    )
    labelframe_param = my_gui.create_labelframe(
        parent=tab_param, mytext="Library parameters", myheight=400
    )
    my_gui.mainloop()


if __name__ == "__main__":
    main_gui()
