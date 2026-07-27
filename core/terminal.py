import tkinter as tk


class Terminal:

    def __init__(self, root):

        self.window = tk.Toplevel(root)

        self.window.title("Terminal")
        self.window.geometry("700x400")
        self.window.configure(bg="black")

        tk.Label(
            self.window,
            text="DivyOS Terminal",
            bg="black",
            fg="lime",
            font=("Consolas", 14)
        ).pack(pady=10)

        self.output = tk.Text(
            self.window,
            bg="black",
            fg="lime",
            insertbackground="white",
            font=("Consolas", 11)
        )
        self.output.pack(fill="both", expand=True)

        self.output.insert("end", "Welcome to DivyOS Terminal\n")