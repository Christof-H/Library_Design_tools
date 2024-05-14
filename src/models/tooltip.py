import tkinter as tk


class Tooltip:
    def __init__(self, widget: tk.Button | tk.Label):
        self.widget = widget
        self.id_process = None  # to stock event process id
        self.bg = None
        self.fg = None
        self.wait = 800
        self.text_width = 300
        self.top_level_window = None
        self.widget.bind("<Enter>", self.mouse_enter)
        self.widget.bind("<Leave>", self.mouse_exit)

    def mouse_enter(self, event=None):
        self.schedule_tooltip()
        print("j'entre")

    def mouse_exit(self, event=None):
        self.unschedule_tooltip()
        self.clear_tooltip()
        print("je sors")

    def schedule_tooltip(self):
        # On efface le processus d'affichage si il en avait un
        self.unschedule_tooltip()
        # On stocke l'id du processus d'affichage tooltip
        self.id_process = self.widget.after(self.wait, self.show_tooltip)
        print("je programme")

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
        # permet de supprimer tout le cadre de la fenetre
        self.top_level_window.wm_overrideredirect(True)
        x_mouse, y_mouse = self.widget.winfo_pointerxy()
        x = x_mouse + 15
        y = y_mouse + 15
        self.top_level_window.wm_geometry("+%d+%d" % (x, y))


def main():
    root = tk.Tk()
    root.minsize(width=500, height=300)

    bouton1 = tk.Button(master=root, text="bouton 1")
    bouton1.pack(pady=50, padx=50)
    bouton2 = tk.Button(master=root, text="bouton 2")
    bouton2.pack(pady=50, padx=50)

    tooltip1 = Tooltip(bouton1)
    tooltip2 = Tooltip(bouton2)

    root.mainloop()


if __name__ == "__main__":
    main()
