# ==============================================================================
# DivyOS - Taskbar (HyperOS Dock Edition)
# ==============================================================================

import os
import sys
import time
import tkinter as tk

from config import DEFAULT_FONT, RADIUS_LARGE, TASKBAR_HEIGHT
from core.theme import get_color, get_theme
from core.utils import draw_rounded_rect

# Optional Pillow handling for icons
try:
    from PIL import Image, ImageTk

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class Taskbar:

    START_LOGO_SIZE = (24, 24)
    MARGIN = 16  # Floating bottom margin
    PILL_PADDING = 6

    def __init__(self, root, start_callback):

        self.root = root
        self.start_logo_image = None
        self.running_app_buttons = {}

        # Fetch theme colors dynamically
        bg_color = get_color("bg")
        taskbar_color = get_color("taskbar")
        text_color = get_color("text")
        accent_color = get_color("accent")
        border_color = get_color("border")

        # ======================================================================
        # Outer Wrapper (Transparent background for floating Dock effect)
        # ======================================================================
        self.wrapper = tk.Frame(
            root, bg=bg_color, height=TASKBAR_HEIGHT + self.MARGIN
        )
        self.wrapper.pack(side="bottom", fill="x")
        self.wrapper.pack_propagate(False)

        # ======================================================================
        # Rounded Canvas Pill (HyperOS Dock Background)
        # ======================================================================
        self.canvas = tk.Canvas(
            self.wrapper,
            height=TASKBAR_HEIGHT,
            bg=bg_color,
            highlightthickness=0,
        )
        self.canvas.pack(
            fill="x", padx=self.MARGIN * 2, pady=(0, self.MARGIN // 2)
        )

        self.canvas.bind("<Configure>", self._redraw_pill)

        # ======================================================================
        # Content Frame (Placed ON TOP of Rounded Canvas)
        # ======================================================================
        self.frame = tk.Frame(self.canvas, bg=taskbar_color)
        self.canvas_window = self.canvas.create_window(
            0, 0, window=self.frame, anchor="nw"
        )

        # ======================================================================
        # Left Section: HyperOS Launcher Button
        # ======================================================================
        logo = self._load_start_logo()

        if logo is not None:
            self.start_btn = tk.Button(
                self.frame,
                image=logo,
                bg=taskbar_color,
                bd=0,
                highlightthickness=0,
                relief="flat",
                activebackground=accent_color,
                cursor="hand2",
                command=start_callback,
            )
            self.start_btn.image = logo
        else:
            self.start_btn = tk.Button(
                self.frame,
                text="✦",  # Modern clean symbol for HyperOS launcher
                font=("Segoe UI Symbol", 16, "bold"),
                bg=taskbar_color,
                fg=accent_color,
                bd=0,
                highlightthickness=0,
                relief="flat",
                activebackground=get_color("hover"),
                activeforeground=accent_color,
                cursor="hand2",
                command=start_callback,
            )

        self.start_btn.pack(side="left", padx=(16, 12), pady=8)
        self._add_hover_effect(
            self.start_btn, get_color("hover"), taskbar_color
        )

        # ======================================================================
        # Middle Section: Centered Running Apps Dock
        # ======================================================================
        self.apps_frame = tk.Frame(self.frame, bg=taskbar_color)
        self.apps_frame.pack(side="left", expand=True, padx=10)

        # ======================================================================
        # Right Section: Status Bar & Clock (HyperOS Style)
        # ======================================================================
        self.status_frame = tk.Frame(self.frame, bg=taskbar_color)
        self.status_frame.pack(side="right", padx=(0, 16))

        self.clock = tk.Label(
            self.status_frame,
            bg=taskbar_color,
            fg=text_color,
            font=(get_color("font_family"), 10, "bold"),
        )
        self.clock.pack(side="right")

        self.update_clock()

    # ==========================================================================
    # Rounded Pill Rendering
    # ==========================================================================

    def _redraw_pill(self, event=None):
        """Redraws the rounded taskbar background with HyperOS Glass aesthetic."""
        self.canvas.delete("pill")

        width = self.canvas.winfo_width()
        height = TASKBAR_HEIGHT

        draw_rounded_rect(
            self.canvas,
            0,
            0,
            width,
            height,
            radius=get_color("corner_radius"),
            fill=get_color("taskbar"),
            outline=get_color("border"),
            width=1,
            tags="pill",
        )

        self.canvas.tag_lower("pill")
        self.canvas.itemconfig(self.canvas_window, width=width, height=height)
        self.canvas.coords(self.canvas_window, 0, 0)

    # ==========================================================================
    # Start Logo Loading
    # ==========================================================================

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

    # ==========================================================================
    # Helpers & App Dock Controls
    # ==========================================================================

    def _add_hover_effect(self, widget, hover_bg, normal_bg):
        widget.bind("<Enter>", lambda e: widget.config(bg=hover_bg))
        widget.bind("<Leave>", lambda e: widget.config(bg=normal_bg))

    def update_clock(self):
        """HyperOS Time Format (HH:MM - DD MMM)"""
        current_time = time.strftime("%H:%M  |  %d %b")
        self.clock.config(text=current_time)
        self.root.after(1000, self.update_clock)

    def add_running_app(self, name, callback):
        """Adds a new app tile to the central dock with HyperOS styling."""
        taskbar_color = get_color("taskbar")
        accent_color = get_color("accent")
        hover_color = get_color("hover")
        text_color = get_color("text")

        btn = tk.Button(
            self.apps_frame,
            text=f"•  {name}",
            bg=taskbar_color,
            fg=text_color,
            bd=0,
            highlightthickness=0,
            relief="flat",
            padx=12,
            pady=6,
            font=(get_color("font_family"), 9, "bold"),
            activebackground=hover_color,
            activeforeground=accent_color,
            cursor="hand2",
            command=callback,
        )
        btn.pack(side="left", padx=3)
        self._add_hover_effect(btn, hover_color, taskbar_color)

        self.running_app_buttons[name] = btn
        return btn

    def remove_running_app(self, name):
        """Removes an app tile when closed."""
        if name in self.running_app_buttons:
            self.running_app_buttons[name].destroy()
            del self.running_app_buttons[name]