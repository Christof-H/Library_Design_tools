import tkinter as tk


class Tooltip:
    """It creates a tooltip for a given widget as the mouse goes on it.

    inspired by :
    https://stackoverflow.com/questions/3221956/how-do-i-display-tooltips-in-tkinter/36221216#36221216

    Add a few modifications to simplify the tooltip class and improve visual rendering
    """

    def __init__(self, widget: tk.Button | tk.Label, text: str):
        self.widget = widget
        self.text = text
        self.id_process = None  # to stock event process id
        self.bg = "#EDC873"
        self.fg = None
        self.wrap_length = 400
        self.wait = 800
        self.text_width = 300
        self.top_level_window = None
        self.widget.bind("<Enter>", self.mouse_enter)
        self.widget.bind("<Leave>", self.mouse_exit)

    def mouse_enter(self, event=None):
        self.schedule_tooltip()

    def mouse_exit(self, event=None):
        self.unschedule_tooltip()
        self.clear_tooltip()

    def schedule_tooltip(self):
        # deletion of the display process if it had one
        self.unschedule_tooltip()
        # Storing the id of the tooltip display process (for possible modification)
        self.id_process = self.widget.after(self.wait, self.show_tooltip)

    def unschedule_tooltip(self):
        new_id = self.id_process
        self.id_process = None
        if new_id:
            self.widget.after_cancel(new_id)

    def clear_tooltip(self):
        if self.top_level_window:
            self.top_level_window.destroy()
        self.top_level_window = None

    def show_tooltip(self):
        self.top_level_window = tk.Toplevel(master=self.widget)
        # removes the entire window frame
        self.top_level_window.wm_overrideredirect(True)
        # determines the position of the mouse at the moment of entry
        x_mouse, y_mouse = self.widget.winfo_pointerxy()
        # adds an offset to the mouse coordinates
        x = x_mouse + 15
        y = y_mouse + 15
        self.top_level_window.wm_geometry(f"+{x}+{y}")

        # creation of a frame for backgroung colour problems with padding in the label
        frame = tk.Frame(self.top_level_window, background=self.bg)
        label = tk.Label(
            frame,
            text=self.text,
            justify=tk.LEFT,
            background=self.bg,
            relief=tk.SOLID,
            borderwidth=0,
            wraplength=self.wrap_length,
        )
        label.grid(padx=5, pady=5, sticky=tk.NSEW)
        frame.grid()


#####################################################################################
#                                   Tests :
#####################################################################################
def test():
    root = tk.Tk()
    root.minsize(width=200, height=100)

    bouton1 = tk.Button(master=root, text="bouton 1")
    bouton1.pack(pady=20, padx=50)
    bouton2 = tk.Button(master=root, text="bouton 2")
    bouton2.pack(pady=20, padx=50)
    text1 = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc libero justo, dapibus vitae mauris et, \
venenatis molestie ante. Vivamus quis pellentesque lorem."
    text2 = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras et sem nulla. \
Maecenas arcu nisi, ultricies ut placerat et, bibendum a nulla. Suspendisse in tellus non est dignissim rutrum ac."
    tooltip1 = Tooltip(widget=bouton1, text=text1)
    tooltip2 = Tooltip(widget=bouton2, text=text2)

    root.mainloop()


if __name__ == "__main__":
    test()
