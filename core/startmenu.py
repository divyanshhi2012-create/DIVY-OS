# ==============================================================================
# DivyOS - Start Menu (HyperOS Launcher Edition)
# ==============================================================================

import tkinter as tk

from config import (
    RADIUS_LARGE,
    START_MENU_HEIGHT,
    START_MENU_WIDTH,
    WINDOW_OPACITY,
)
from core.theme import get_color, get_theme
from core.utils import draw_rounded_rect


class StartMenu:

    def __init__(self, root, desktop=None):
        self.root = root
        self.desktop = desktop
        self.window = None

    def toggle(self):

        if self.window:
            self.window.destroy()
            self.window = None
            return

        # Fetch Dynamic Theme Colors
        panel_color = get_color("panel")
        bg_color = get_color("bg")
        text_color = get_color("text")
        accent_color = get_color("accent")
        border_color = get_color("border")
        font_family = get_color("font_family")

        self.window = tk.Toplevel(self.root)
        self.window.geometry(f"{START_MENU_WIDTH}x{START_MENU_HEIGHT}+20+240")
        self.window.overrideredirect(True)
        self.window.attributes("-alpha", WINDOW_OPACITY)
        self.window.configure(bg=bg_color)

        # Main Canvas Background
        self.canvas = tk.Canvas(
            self.window,
            width=START_MENU_WIDTH,
            height=START_MENU_HEIGHT,
            bg=bg_color,
            highlightthickness=0,
        )
        self.canvas.pack(fill="both", expand=True)

        draw_rounded_rect(
            self.canvas,
            0,
            0,
            START_MENU_WIDTH,
            START_MENU_HEIGHT,
            radius=get_color("corner_radius"),
            fill=panel_color,
            outline=border_color,
            width=1,
        )

        self.content = tk.Frame(self.canvas, bg=panel_color)
        self.canvas.create_window(
            0,
            0,
            window=self.content,
            anchor="nw",
            width=START_MENU_WIDTH,
            height=START_MENU_HEIGHT,
        )

        self.window.bind("<FocusOut>", lambda e: self.toggle())
        self.window.focus_force()

        # Header Title
        tk.Label(
            self.content,
            text="✦ DivyOS Launcher",
            bg=panel_color,
            fg=accent_color,
            font=(font_family, 14, "bold"),
        ).pack(pady=(20, 15))

        # Apps Grid Container
        apps_frame = tk.Frame(self.content, bg=panel_color)
        apps_frame.pack(fill="both", expand=True, padx=20)

        apps = self._get_app_list()

        columns = 3
        for index, (label, command) in enumerate(apps):
            row = index // columns
            col = index % columns
            apps_frame.columnconfigure(col, weight=1)
            self._create_app_tile(apps_frame, label, command, row, col)

        # Power Controls Row (Bottom Bar)
        power_row = tk.Frame(self.content, bg=panel_color)
        power_row.pack(side="bottom", fill="x", pady=(10, 16), padx=20)

        self._create_power_button(
            power_row, "🔒", self._safe(self._get_desktop_method("lock"))
        )
        self._create_power_button(
            power_row, "🔁", self._safe(self._get_desktop_method("restart"))
        )
        self._create_power_button(
            power_row,
            "⏻",
            self._safe(self._get_desktop_method("shutdown")),
            is_danger=True,
        )

    def _get_app_list(self):
        return [
            ("📂\nFiles", self._safe(self._get_desktop_method("open_explorer"))),
            (
                "⚡\nTerminal",
                self._safe(self._get_desktop_method("open_terminal")),
            ),
            ("🌐\nBrowser", self._safe(self._get_desktop_method("open_browser"))),
            ("📝\nNotepad", self._safe(self._get_desktop_method("open_notepad"))),
            (
                "🧮\nCalculator",
                self._safe(self._get_desktop_method("open_calculator")),
            ),
            (
                "⚙️\nSettings",
                self._safe(self._get_desktop_method("open_settings")),
            ),
            (
                "🛍️\nStore",
                self._safe(self._get_desktop_method("open_appstore")),
            ),
            ("✦\nDivyAI", self._safe(self._get_ai_open())),
            (
                "🗑️\nTrash",
                self._safe(self._get_desktop_method("open_explorer")),
            ),
        ]

    def _get_desktop_method(self, name):
        if self.desktop is not None and hasattr(self.desktop, name):
            return getattr(self.desktop, name)
        return None

    def _get_ai_open(self):
        if self.desktop is not None and hasattr(self.desktop, "ai_window"):
            return self.desktop.ai_window.open
        return None

    def _safe(self, func):
        def wrapped():
            self.toggle()
            if func:
                func()
            else:
                print("[DivyOS] Application unavailable.")

        return wrapped

    def _create_app_tile(self, parent, label, command, row, col):
        button_color = get_color("button")
        hover_color = get_color("hover")
        text_color = get_color("text")
        accent_color = get_color("accent")
        font_family = get_color("font_family")

        tile = tk.Button(
            parent,
            text=label,
            command=command,
            font=(font_family, 10, "bold"),
            bg=button_color,
            fg=text_color,
            bd=0,
            highlightthickness=0,
            relief="flat",
            activebackground=accent_color,
            activeforeground="#FFFFFF",
            cursor="hand2",
            justify="center",
            width=8,
            height=3,
        )
        tile.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")
        tile.bind("<Enter>", lambda e: tile.config(bg=hover_color))
        tile.bind("<Leave>", lambda e: tile.config(bg=button_color))
        return tile

    def _create_power_button(
        self, parent, symbol, command, is_danger=False
    ):
        panel_color = get_color("panel")
        button_color = get_color("button")
        hover_color = "#FF3B30" if is_danger else get_color("hover")
        text_color = get_color("text")
        font_family = get_color("font_family")

        btn = tk.Button(
            parent,
            text=symbol,
            command=command,
            font=(font_family, 13),
            bg=button_color,
            fg=text_color,
            bd=0,
            highlightthickness=0,
            relief="flat",
            activebackground=hover_color,
            activeforeground="#FFFFFF",
            cursor="hand2",
            width=4,
            pady=6,
        )
        btn.pack(side="left", expand=True, padx=4)
        btn.bind(
            "<Enter>",
            lambda e: btn.config(
                bg=hover_color, fg="#FFFFFF" if is_danger else text_color
            ),
        )
        btn.bind(
            "<Leave>",
            lambda e: btn.config(bg=button_color, fg=text_color),
        )
        return btn