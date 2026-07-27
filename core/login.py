import tkinter as tk
from typing import Callable

try:
    from config import WIDTH, HEIGHT
except Exception:
    # fallback defaults if config is missing or invalid
    WIDTH, HEIGHT = 800, 600


class LoginScreen:

    def __init__(self, callback: Callable[[], None]):
        if not callable(callback):
            raise TypeError("callback must be callable")
        self.callback = callback

    def run(self):
        self.root = tk.Tk()
        self.root.title("Login")
        self.root.configure(bg="#1b1b1b")
        self.root.resizable(False, False)

        # center the window on screen
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - WIDTH) // 2
        y = (sh - HEIGHT) // 2
        self.root.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")

        tk.Label(
            self.root,
            text="Welcome to DivyOS",
            font=("Arial", 30, "bold"),
            bg="#1b1b1b",
            fg="white"
        ).pack(pady=100)

        tk.Button(
            self.root,
            text="Login",
            font=("Arial", 18),
            command=self.login
        ).pack()

        # allow Enter key to trigger login
        self.root.bind("<Return>", lambda e: self.login())

        self.root.mainloop()

    def login(self):
        try:
            self.root.destroy()
        finally:
            # ensure callback is invoked even if destroy raises
            self.callback()