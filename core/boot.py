import tkinter as tk
from tkinter import ttk

from config import APP_NAME, WIDTH, HEIGHT, BOOT_TIME


class BootScreen:

    def __init__(self, callback):
        self.callback = callback
        self.progress = 0

    def run(self):
        self.root = tk.Tk()

        self.root.title(APP_NAME)
        self.root.overrideredirect(True)

        win_width = 700
        win_height = 400

        x = (self.root.winfo_screenwidth() - win_width) // 2
        y = (self.root.winfo_screenheight() - win_height) // 2

        self.root.geometry(f"{win_width}x{win_height}+{x}+{y}")
        self.root.configure(bg="#1E1E1E")

        tk.Label(
            self.root,
            text="DivyOS",
            font=("Segoe UI", 34, "bold"),
            fg="white",
            bg="#1E1E1E"
        ).pack(pady=70)

        self.status = tk.Label(
            self.root,
            text="Booting...",
            font=("Segoe UI", 12),
            fg="#CCCCCC",
            bg="#1E1E1E"
        )
        self.status.pack(pady=10)

        self.bar = ttk.Progressbar(
            self.root,
            orient="horizontal",
            length=450,
            mode="determinate",
            maximum=100
        )
        self.bar.pack(pady=20)

        self.animate()

        self.root.mainloop()

    def animate(self):
        self.progress += 2
        self.bar["value"] = self.progress

        if self.progress < 100:
            self.root.after(BOOT_TIME // 50, self.animate)
        else:
            self.status.config(text="Welcome to DivyOS")
            self.root.after(500, self.finish)

    def finish(self):
        self.root.destroy()
        self.callback()