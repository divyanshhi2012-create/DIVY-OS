import tkinter as tk

from core.explorer import FileExplorer
from core.terminal import Terminal

from config import (
    START_MENU_COLOR,
    TEXT_COLOR,
    ACCENT_COLOR,
    BORDER_COLOR,
    BUTTON_COLOR,
    HOVER_COLOR,
    START_MENU_WIDTH,
    START_MENU_HEIGHT,
    TITLE_FONT,
    DEFAULT_FONT,
    WINDOW_OPACITY,
)


class StartMenu:

    def __init__(self, root):

        self.root = root

        self.window = None

    def toggle(self):

        if self.window:

            self.window.destroy()

            self.window = None

            return

        self.window = tk.Toplevel(self.root)

        self.window.geometry(f"{START_MENU_WIDTH}x{START_MENU_HEIGHT}+20+250")

        self.window.configure(bg=START_MENU_COLOR)

        self.window.overrideredirect(True)

        # Windows 11 style frosted/glass border + slight transparency
        self.window.attributes("-alpha", WINDOW_OPACITY)

        self.window.configure(
            highlightthickness=1,
            highlightbackground=BORDER_COLOR
        )

        # Close the start menu if it loses focus (click elsewhere)
        self.window.bind("<FocusOut>", lambda e: self.toggle())
        self.window.focus_force()

        tk.Label(

            self.window,

            text="DivyOS",

            bg=START_MENU_COLOR,

            fg=TEXT_COLOR,

            font=TITLE_FONT

        ).pack(pady=20)

        self._create_menu_button(
            "📂 File Explorer",
            lambda: FileExplorer(self.root)
        )

        self._create_menu_button(
            "💻 Terminal",
            lambda: Terminal(self.root)
        )

    def _create_menu_button(self, text, command):
        """Creates a Windows-11-style start menu button with hover glow."""

        btn = tk.Button(
            self.window,
            text=text,
            command=command,
            width=25,
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            font=DEFAULT_FONT,
            bd=0,
            highlightthickness=0,
            relief="flat",
            activebackground=ACCENT_COLOR,
            activeforeground=TEXT_COLOR,
            cursor="hand2",
            pady=8
        )

        btn.pack(pady=8)

        btn.bind("<Enter>", lambda e: btn.config(bg=HOVER_COLOR))
        btn.bind("<Leave>", lambda e: btn.config(bg=BUTTON_COLOR))

        return btn