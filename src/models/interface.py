import tkinter as tk
from tkinter import ttk


class Interface(tk.Tk):
    # TODO : add docstring for the Interface class
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

    def on_exit(self):
        self.quit()
        self.destroy()

    def create_notebook(self):
        # TODO : add docstring for this method and input/output type
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

    def create_frame_in_notebook(self, title):
        # TODO : add docstring for this method and input/output type
        tab = ttk.Frame(master=self.notebook, width=self.width, height=self.height)
        tab.pack(fill="both", expand=True)
        self.notebook.add(tab, text=title)
        return tab

    def create_labelframe(
        self, parent, text, column, row, columnspan, pady_int=None, pady=None
    ):
        # TODO : add docstring for this method and input/output type
        labelframe = tk.LabelFrame(
            master=parent, text=text, width=self.width, pady=pady_int
        )
        labelframe.grid(
            column=column,
            row=row,
            columnspan=columnspan,
            pady=pady,
            padx=20,
            sticky=tk.EW,
        )
        return labelframe

    def create_label_img(
        self, master, image_path, resize_rate=1, column=None, row=None, padx=None
    ):
        # TODO : add docstring for this method and input/output type
        img = tk.PhotoImage(file=image_path)
        img_resized = img.subsample(resize_rate)
        label_img = tk.Label(master=master, image=img_resized)
        label_img.grid(column=column, row=row, padx=padx)
        # Keep a reference to the photo object to avoid deletion by the garbage collector = return img_resized
        # possibility to put img_resized in label_img.image : label_img.image = img_resized
        return label_img, img_resized

    def create_img_graphic(self, master, image_path, resize_rate=1):
        # TODO : add docstring for this method and input/output type
        img = tk.PhotoImage(file=image_path)
        img_resized = img.subsample(resize_rate)
        label_img = tk.Label(master=master, image=img_resized)
        label_img.place(x=0, y=0, relwidth=1, relheight=1)
        # Keep a reference to the photo object to avoid deletion by the garbage collector
        label_img.image = img_resized
        return label_img

    def create_label(
        self, master, text, column, row, sticky, pady=5, padx=5, columnspan=None
    ):
        # TODO : add docstring for this method and input/output type
        label = tk.Label(master=master, text=text, pady=pady, padx=padx)
        label.grid(sticky=sticky, column=column, row=row, columnspan=columnspan)
        return label

    def create_entry(
        self,
        master,
        width,
        column,
        row,
        pady=None,
        padx=None,
        sticky=None,
        textvariable=None,
    ):
        # TODO : add docstring for this method and input/output type
        input = tk.Entry(master=master, width=width, textvariable=textvariable)
        input.grid(column=column, row=row, pady=pady, padx=padx, sticky=sticky)
        return input

    def create_button(
        self, master, text, column, row, pady=None, padx=None, sticky=None, command=None
    ):
        # TODO : add docstring for this method and input/output type
        button = tk.Button(master=master, text=text, command=command)
        button.grid(column=column, row=row, pady=pady, padx=padx, sticky=sticky)
        return button

    def create_button_place(self, master, text, x, y, command=None):
        # TODO : add docstring for this method and input/output type
        button = tk.Button(master=master, text=text, command=command)
        button.place(x=x, y=y)
        return button

    def create_radiobutton(
        self,
        master,
        text,
        variable,
        value,
        column,
        row,
        pady=None,
        padx=None,
        sticky=None,
        command=None,
    ):
        # TODO : add docstring for this method and input/output type
        radiobutton = tk.Radiobutton(
            master=master, text=text, variable=variable, value=value, command=command
        )
        radiobutton.grid(column=column, row=row, pady=pady, padx=padx, sticky=sticky)
        return radiobutton

    def create_spinbox(
        self,
        master,
        from_,
        to,
        width,
        textvariable,
        column,
        row,
        wrap=False,
        pady=None,
        padx=None,
        sticky=None,
        command=None,
    ):
        # TODO : add docstring for this method and input/output type
        spinbox = tk.Spinbox(
            master=master,
            from_=from_,
            to=to,
            width=width,
            textvariable=textvariable,
            justify=tk.RIGHT,
            wrap=wrap,
            command=command,
        )
        spinbox.grid(column=column, row=row, pady=pady, padx=padx, sticky=sticky)
        return spinbox

    def create_combobox(
        self,
        master,
        values,
        textvariable,
        column,
        row,
        columnspan=None,
        width=None,
        pady=None,
        padx=None,
        sticky=None,
    ):
        # TODO : add docstring for this method and input/output type
        combobox = ttk.Combobox(
            master=master, values=values, textvariable=textvariable, width=width
        )
        combobox.grid(
            column=column,
            row=row,
            columnspan=columnspan,
            pady=pady,
            padx=padx,
            sticky=sticky,
        )
        return combobox

    def create_separator(self, master, column=None, row=None, width=None):
        frame = tk.Frame(
            master=master,
            width=width,
        )
        # TODO : add docstring for this method and input/output type
        frame.grid(column=column, row=row)
        return frame

    def create_frame(self, master, width, height, pady=None):
        frame = tk.Frame(master=master, width=width, height=height)
        frame.pack(pady=pady)
        return frame

    def create_csv_board(
        self,
        master: tk.Frame,
    ):
        # Add a style for Treeview
        tree_style = ttk.Style()

        # Pick a theme
        tree_style.theme_use("default")

        # configure Treeview colors
        tree_style.configure(
            "Treeview",
            background="#D3D3D3",
            forground="black",
            rowheight=25,
            fieldbackground="#D3D3D3",
        )
        # change row selected color
        tree_style.map("Treeview", background=[("selected", "#347083")])

        # Create Treeview and specify the number of row to be displayed by default (17)
        tree = ttk.Treeview(master=master, height=17)
        # deactivates the index column
        tree.configure(show="headings")

        # create a treeview scrollbar
        tree_scroll = tk.Scrollbar(master=master)
        tree.configure(yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=tree.yview)

        return tree, tree_scroll
