import tkinter as tk


class AIWindow:

    def __init__(self, desktop):
        self.desktop = desktop
        self.window = None

    def open(self):

        # Agar window pehle se khuli hai to usi ko saamne lao
        if self.window is not None:
            self.window.lift()
            return

        # Window create
        self.window = tk.Toplevel(self.desktop.root)
        self.window.title("🧠 DivyAI")
        self.window.geometry("1000x650")
        self.window.configure(bg="#202124")

        # Close button handle
        self.window.protocol("WM_DELETE_WINDOW", self.close)

        # Title
        title = tk.Label(
            self.window,
            text="🧠 DivyAI",
            font=("Segoe UI", 22, "bold"),
            bg="#202124",
            fg="white"
        )
        title.pack(pady=20)

        # Welcome text
        welcome = tk.Label(
            self.window,
            text="Welcome to DivyAI",
            font=("Segoe UI", 14),
            bg="#202124",
            fg="lightgray"
        )
        welcome.pack()

    def close(self):
        self.window.destroy()
        self.window = None