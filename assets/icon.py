import tkinter as tk
import time
import os
import sys

from config import (
    TASKBAR_COLOR,
    TEXT_COLOR,
    ACCENT_COLOR,
    BORDER_COLOR,
    TASKBAR_HEIGHT,
    DEFAULT_FONT,
)

# Pillow is optional but required for PNG/ICO logo support.
# If it isn't installed, the Start button falls back to the ⊞ symbol.
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class Taskbar:

    START_LOGO_SIZE = (24, 24)

    def __init__(self, root, start_callback):

        self.root = root

        # Keeps a hard reference so the logo image never disappears
        self.start_logo_image = None

        # =========================
        # Taskbar Frame
        # =========================
        self.frame = tk.Frame(
            root,
            bg=TASKBAR_COLOR,
            height=TASKBAR_HEIGHT,
            highlightthickness=1,
            highlightbackground=BORDER_COLOR
        )

        self.frame.pack(side="bottom", fill="x")
        self.frame.pack_propagate(False)

        # =========================
        # Start Button
        # =========================
        logo = self._load_start_logo()

        if logo is not None:
            self.start_btn = tk.Button(
                self.frame,
                image=logo,
                bg=TASKBAR_COLOR,
                bd=0,
                highlightthickness=0,
                relief="flat",
                activebackground=ACCENT_COLOR,
                cursor="hand2",
                command=start_callback
            )
            self.start_btn.image = logo  # extra safety reference
        else:
            self.start_btn = tk.Button(
                self.frame,
                text="⊞",
                font=("Segoe UI", 16, "bold"),
                bg=TASKBAR_COLOR,
                fg=TEXT_COLOR,
                bd=0,
                highlightthickness=0,
                relief="flat",
                activebackground=ACCENT_COLOR,
                activeforeground=TEXT_COLOR,
                cursor="hand2",
                command=start_callback
            )

        self.start_btn.pack(side="left", padx=10)

        # Win11-style hover highlight
        self._add_hover_effect(self.start_btn, ACCENT_COLOR, TASKBAR_COLOR)

        # =========================
        # Running Apps
        # =========================
        self.apps_frame = tk.Frame(
            self.frame,
            bg=TASKBAR_COLOR
        )

        self.apps_frame.pack(side="left", padx=15)

        # =========================
        # Clock
        # =========================
        self.clock = tk.Label(
            self.frame,
            bg=TASKBAR_COLOR,
            fg=TEXT_COLOR,
            font=DEFAULT_FONT
        )

        self.clock.pack(side="right", padx=15)

        self.update_clock()

    def _get_base_path(self):
        """Resolve the base path whether running from source or frozen (PyInstaller)."""
        if getattr(sys, "frozen", False):
            return sys._MEIPASS
        return os.path.abspath(".")

    def _load_start_logo(self):
        """
        Attempts to load the DivyOS start button logo from:
            assets/icons/start.png
            assets/icons/start.ico

        Returns a Tkinter-compatible PhotoImage, or None if unavailable
        (in which case the ⊞ symbol is used instead).
        """
        if not PIL_AVAILABLE:
            return None

        icons_dir = os.path.join(self._get_base_path(), "assets", "icons")

        candidates = [
            os.path.join(icons_dir, "start.png"),
            os.path.join(icons_dir, "start.ico"),
        ]

        for path in candidates:
            if os.path.exists(path):
                try:
                    img = Image.open(path)
                    img = img.convert("RGBA")
                    img = img.resize(self.START_LOGO_SIZE, Image.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    self.start_logo_image = photo  # prevent garbage collection
                    return photo
                except Exception as e:
                    print("Start Logo Load Error:", path, e)
                    return None

        return None

    def _add_hover_effect(self, widget, hover_bg, normal_bg):
        """Adds a simple Windows-11-style hover glow to a button."""
        widget.bind("<Enter>", lambda e: widget.config(bg=hover_bg))
        widget.bind("<Leave>", lambda e: widget.config(bg=normal_bg))

    def update_clock(self):

        self.clock.config(
            text=time.strftime("%d/%m/%Y   %H:%M")
        )

        self.root.after(1000, self.update_clock)

    def add_running_app(self, name, callback):

        btn = tk.Button(
            self.apps_frame,
            text=name,
            bg=TASKBAR_COLOR,
            fg=TEXT_COLOR,
            bd=0,
            highlightthickness=0,
            relief="flat",
            padx=10,
            activebackground=ACCENT_COLOR,
            activeforeground=TEXT_COLOR,
            command=callback
        )

        btn.pack(side="left", padx=3)

        # Same hover glow effect on running app buttons
        self._add_hover_effect(btn, ACCENT_COLOR, TASKBAR_COLOR)

        return btn