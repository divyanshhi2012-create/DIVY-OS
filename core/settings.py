# ===========================
# DivyOS - Settings
# ===========================
#
# Central settings panel for DivyOS. Currently controls:
#   - Dark / Light theme (via core/theme.py)
#   - Window transparency
#   - Basic system info display
#
# Built to be easily expandable with more settings tabs later
# (network, sound, personalization, etc.)

import tkinter as tk
from tkinter import ttk

from core.utils import center_window
from core.theme import get_color, get_theme, set_theme, current_theme_name
from config import APP_NAME, VERSION, TITLE_FONT, DEFAULT_FONT


class Settings:

    def __init__(self, root, desktop=None):
        """
        root     -> the main Tk root window
        desktop  -> optional reference to the Desktop instance, so
                    Settings can trigger a live theme refresh across
                    the whole OS (desktop icons, taskbar, start menu)
        """

        self.root = root
        self.desktop = desktop

        # =========================
        # Window
        # =========================
        self.window = tk.Toplevel(root)
        self.window.title("Settings - DivyOS")

        center_window(self.window, 600, 420)

        self.window.configure(bg=get_color("bg"))
        self.window.resizable(False, False)

        # =========================
        # Sidebar (categories)
        # =========================
        self.sidebar = tk.Frame(self.window, bg=get_color("panel"), width=170)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="⚙ Settings",
            font=TITLE_FONT,
            bg=get_color("panel"),
            fg=get_color("text")
        ).pack(pady=(20, 30), padx=15, anchor="w")

        self.nav_buttons = {}
        self._create_nav_button("Personalization", self.show_personalization)
        self._create_nav_button("System", self.show_system)
        self._create_nav_button("About", self.show_about)

        # =========================
        # Content Area
        # =========================
        self.content = tk.Frame(self.window, bg=get_color("bg"))
        self.content.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Start on the Personalization tab
        self.show_personalization()

    # ==========================
    # Sidebar Navigation
    # ==========================

    def _create_nav_button(self, label, command):

        btn = tk.Button(
            self.sidebar,
            text=label,
            font=DEFAULT_FONT,
            bg=get_color("panel"),
            fg=get_color("text"),
            bd=0,
            highlightthickness=0,
            relief="flat",
            anchor="w",
            padx=15,
            pady=10,
            activebackground=get_color("accent"),
            activeforeground=get_color("text"),
            cursor="hand2",
            command=command
        )
        btn.pack(fill="x")

        btn.bind("<Enter>", lambda e: btn.config(bg=get_color("hover")))
        btn.bind("<Leave>", lambda e: btn.config(bg=get_color("panel")))

        self.nav_buttons[label] = btn

        return btn

    def _clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    # ==========================
    # Personalization Tab
    # ==========================

    def show_personalization(self):
        self._clear_content()

        tk.Label(
            self.content,
            text="Personalization",
            font=TITLE_FONT,
            bg=get_color("bg"),
            fg=get_color("text")
        ).pack(anchor="w", pady=(0, 20))

        # ---- Theme toggle ----
        theme_row = tk.Frame(self.content, bg=get_color("bg"))
        theme_row.pack(fill="x", pady=10)

        tk.Label(
            theme_row,
            text="App Theme",
            font=DEFAULT_FONT,
            bg=get_color("bg"),
            fg=get_color("text")
        ).pack(side="left")

        self.theme_var = tk.StringVar(value=current_theme_name())

        theme_dropdown = ttk.Combobox(
            theme_row,
            textvariable=self.theme_var,
            values=["dark", "light"],
            state="readonly",
            width=10
        )
        theme_dropdown.pack(side="right")
        theme_dropdown.bind("<<ComboboxSelected>>", self._on_theme_change)

        # ---- Transparency slider ----
        opacity_row = tk.Frame(self.content, bg=get_color("bg"))
        opacity_row.pack(fill="x", pady=10)

        tk.Label(
            opacity_row,
            text="Window Transparency",
            font=DEFAULT_FONT,
            bg=get_color("bg"),
            fg=get_color("text")
        ).pack(side="left")

        current_alpha = self.root.attributes("-alpha")

        self.opacity_slider = tk.Scale(
            opacity_row,
            from_=0.6,
            to=1.0,
            resolution=0.01,
            orient="horizontal",
            bg=get_color("bg"),
            fg=get_color("text"),
            highlightthickness=0,
            troughcolor=get_color("panel"),
            command=self._on_opacity_change
        )
        self.opacity_slider.set(current_alpha)
        self.opacity_slider.pack(side="right", fill="x", expand=True, padx=(20, 0))

        # ---- Note about live theme refresh ----
        tk.Label(
            self.content,
            text="Note: theme changes apply to newly opened windows.\nRestart DivyOS to fully re-theme the desktop and taskbar.",
            font=("Segoe UI", 9),
            bg=get_color("bg"),
            fg=get_color("hover"),
            justify="left"
        ).pack(anchor="w", pady=(30, 0))

    def _on_theme_change(self, event=None):
        selected = self.theme_var.get()
        set_theme(selected)

        # Refresh the Settings window itself immediately so the
        # user sees the effect without needing to reopen it.
        self.window.destroy()
        Settings(self.root, self.desktop)

    def _on_opacity_change(self, value):
        try:
            self.root.attributes("-alpha", float(value))
        except Exception:
            pass

    # ==========================
    # System Tab
    # ==========================

    def show_system(self):
        self._clear_content()

        tk.Label(
            self.content,
            text="System",
            font=TITLE_FONT,
            bg=get_color("bg"),
            fg=get_color("text")
        ).pack(anchor="w", pady=(0, 20))

        info_rows = [
            ("Operating System", APP_NAME),
            ("Version", VERSION),
            ("Theme", current_theme_name().capitalize()),
        ]

        for label, value in info_rows:
            row = tk.Frame(self.content, bg=get_color("bg"))
            row.pack(fill="x", pady=6)

            tk.Label(
                row, text=label, font=DEFAULT_FONT,
                bg=get_color("bg"), fg=get_color("text")
            ).pack(side="left")

            tk.Label(
                row, text=value, font=DEFAULT_FONT,
                bg=get_color("bg"), fg=get_color("accent")
            ).pack(side="right")

    # ==========================
    # About Tab
    # ==========================

    def show_about(self):
        self._clear_content()

        tk.Label(
            self.content,
            text="About DivyOS",
            font=TITLE_FONT,
            bg=get_color("bg"),
            fg=get_color("text")
        ).pack(anchor="w", pady=(0, 20))

        tk.Label(
            self.content,
            text=f"{APP_NAME} {VERSION}",
            font=("Segoe UI", 14, "bold"),
            bg=get_color("bg"),
            fg=get_color("accent")
        ).pack(anchor="w", pady=(0, 10))

        tk.Label(
            self.content,
            text="A custom desktop environment built with Python and Tkinter.",
            font=DEFAULT_FONT,
            bg=get_color("bg"),
            fg=get_color("text"),
            wraplength=380,
            justify="left"
        ).pack(anchor="w")