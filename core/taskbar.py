import tkinter as tk
import time

from config import (
    TASKBAR_COLOR,
    TEXT_COLOR,
    ACCENT_COLOR,
    BORDER_COLOR,
    TASKBAR_HEIGHT,
    DEFAULT_FONT,
    RADIUS_LARGE,
    RADIUS_MEDIUM,
)

from core.utils import draw_rounded_rect

# Pillow is optional but required for a PNG/ICO Start logo.
# If it isn't installed, the Start button falls back to the ⊞ symbol.
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

import os
import sys


class Taskbar:

    START_LOGO_SIZE = (22, 22)
    MARGIN = 12          # gap from screen edges, floating pill effect
    PILL_PADDING = 6      # inner padding around buttons

    def __init__(self, root, start_callback):

        self.root = root
        self.start_logo_image = None

        # =========================
        # Outer wrapper (transparent, holds the floating pill)
        # =========================
        self.wrapper = tk.Frame(root, bg=root["bg"], height=TASKBAR_HEIGHT + self.MARGIN)
        self.wrapper.pack(side="bottom", fill="x")
        self.wrapper.pack_propagate(False)

        # =========================
        # Rounded Canvas Pill
        # =========================
        self.canvas = tk.Canvas(
            self.wrapper,
            height=TASKBAR_HEIGHT,
            bg=root["bg"],
            highlightthickness=0
        )
        self.canvas.pack(fill="x", padx=self.MARGIN, pady=(0, self.MARGIN // 2))

        self.canvas.bind("<Configure>", self._redraw_pill)

        # =========================
        # Content frame placed ON TOP of the rounded canvas
        # =========================
        self.frame = tk.Frame(self.canvas, bg=TASKBAR_COLOR)
        self.canvas_window = self.canvas.create_window(
            0, 0, window=self.frame, anchor="nw"
        )

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
            self.start_btn.image = logo
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

        self.start_btn.pack(side="left", padx=(18, 10), pady=10)
        self._add_hover_effect(self.start_btn, ACCENT_COLOR, TASKBAR_COLOR)

        # =========================
        # Running Apps
        # =========================
        self.apps_frame = tk.Frame(self.frame, bg=TASKBAR_COLOR)
        self.apps_frame.pack(side="left", padx=10)

        # =========================
        # Clock
        # =========================
        self.clock = tk.Label(
            self.frame,
            bg=TASKBAR_COLOR,
            fg=TEXT_COLOR,
            font=DEFAULT_FONT
        )
        self.clock.pack(side="right", padx=18)

        self.update_clock()

    # ==========================
    # Rounded Pill Rendering
    # ==========================

    def _redraw_pill(self, event=None):
        """Redraws the rounded taskbar background whenever it resizes."""
        self.canvas.delete("pill")

        width = self.canvas.winfo_width()
        height = TASKBAR_HEIGHT

        draw_rounded_rect(
            self.canvas, 0, 0, width, height,
            radius=RADIUS_LARGE,
            fill=TASKBAR_COLOR,
            outline=BORDER_COLOR,
            width=1,
            tags="pill"
        )

        self.canvas.tag_lower("pill")
        self.canvas.itemconfig(self.canvas_window, width=width, height=height)
        self.canvas.coords(self.canvas_window, 0, 0)

    # ==========================
    # Start Logo Loading
    # ==========================

    def _get_base_path(self):
        if getattr(sys, "frozen", False):
            return sys._MEIPASS
        return os.path.abspath(".")

    def _load_start_logo(self):
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
                    img = Image.open(path).convert("RGBA")
                    img = img.resize(self.START_LOGO_SIZE, Image.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    self.start_logo_image = photo
                    return photo
                except Exception as e:
                    print("Start Logo Load Error:", path, e)
                    return None

        return None

    # ==========================
    # Helpers
    # ==========================

    def _add_hover_effect(self, widget, hover_bg, normal_bg):
        widget.bind("<Enter>", lambda e: widget.config(bg=hover_bg))
        widget.bind("<Leave>", lambda e: widget.config(bg=normal_bg))

    def update_clock(self):
        self.clock.config(text=time.strftime("%d/%m/%Y   %H:%M"))
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
            padx=14,
            pady=8,
            activebackground=ACCENT_COLOR,
            activeforeground=TEXT_COLOR,
            cursor="hand2",
            command=callback
        )
        btn.pack(side="left", padx=4)
        self._add_hover_effect(btn, ACCENT_COLOR, TASKBAR_COLOR)
        return btn