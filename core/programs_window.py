# ===========================
# DivyOS - Programs (Installed Windows Apps)
# ===========================
#
# Shows every real app installed on this Windows PC and launches
# them with a click, styled to match DivyOS's HyperOS theme.

import tkinter as tk

from core.utils import center_window, draw_rounded_rect
from core.installed_apps import InstalledApps
from config import (
    START_MENU_COLOR,
    TEXT_COLOR,
    ACCENT_COLOR,
    BORDER_COLOR,
    BUTTON_COLOR,
    HOVER_COLOR,
    TITLE_FONT,
    DEFAULT_FONT,
    WINDOW_OPACITY,
    RADIUS_LARGE,
)


class ProgramsWindow:

    WIDTH = 480
    HEIGHT = 560

    def __init__(self, root):
        self.root = root
        self.apps_engine = InstalledApps()
        self.window = None
        self.list_frame = None
        self.search_var = None

    def open(self):
        if self.window and self.window.winfo_exists():
            self.window.lift()
            return

        self.window = tk.Toplevel(self.root)
        self.window.overrideredirect(True)
        self.window.attributes("-alpha", WINDOW_OPACITY)
        self.window.configure(bg=self.root["bg"])

        center_window(self.window, self.WIDTH, self.HEIGHT)

        canvas = tk.Canvas(
            self.window, width=self.WIDTH, height=self.HEIGHT,
            bg=self.root["bg"], highlightthickness=0
        )
        canvas.pack(fill="both", expand=True)

        draw_rounded_rect(
            canvas, 0, 0, self.WIDTH, self.HEIGHT,
            radius=RADIUS_LARGE, fill=START_MENU_COLOR,
            outline=BORDER_COLOR, width=1
        )

        content = tk.Frame(canvas, bg=START_MENU_COLOR)
        canvas.create_window(0, 0, window=content, anchor="nw",
                              width=self.WIDTH, height=self.HEIGHT)

        header = tk.Frame(content, bg=START_MENU_COLOR)
        header.pack(fill="x", padx=15, pady=(15, 5))

        tk.Label(
            header, text="🗂️ Programs", font=TITLE_FONT,
            bg=START_MENU_COLOR, fg=TEXT_COLOR
        ).pack(side="left")

        close_btn = tk.Button(
            header, text="✕", font=("Segoe UI", 11),
            bg=START_MENU_COLOR, fg=TEXT_COLOR, bd=0,
            highlightthickness=0, relief="flat",
            activebackground=ACCENT_COLOR, cursor="hand2",
            command=self.close
        )
        close_btn.pack(side="right")

        header.bind("<ButtonPress-1>", self._start_drag)
        header.bind("<B1-Motion>", self._drag_window)

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(
            content, textvariable=self.search_var,
            font=DEFAULT_FONT, bg=BUTTON_COLOR, fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR, bd=0, relief="flat"
        )
        search_entry.pack(fill="x", padx=15, pady=10, ipady=8)
        search_entry.bind("<KeyRelease>", lambda e: self._render_list())

        list_container = tk.Frame(content, bg=START_MENU_COLOR)
        list_container.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        canvas_list = tk.Canvas(list_container, bg=START_MENU_COLOR, highlightthickness=0)
        scrollbar = tk.Scrollbar(list_container, orient="vertical", command=canvas_list.yview)
        self.list_frame = tk.Frame(canvas_list, bg=START_MENU_COLOR)

        self.list_frame.bind(
            "<Configure>",
            lambda e: canvas_list.configure(scrollregion=canvas_list.bbox("all"))
        )
        canvas_list.create_window((0, 0), window=self.list_frame, anchor="nw")
        canvas_list.configure(yscrollcommand=scrollbar.set)

        canvas_list.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self._render_list()

    def _render_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        query = self.search_var.get() if self.search_var else ""
        apps = self.apps_engine.search(query) if query else self.apps_engine.scan()

        if not apps:
            tk.Label(
                self.list_frame,
                text="No installed apps found.",
                bg=START_MENU_COLOR, fg=TEXT_COLOR, font=DEFAULT_FONT
            ).pack(pady=20)
            return

        for app in apps:
            self._create_app_row(app)

    def _create_app_row(self, app):
        row = tk.Button(
            self.list_frame,
            text=app["name"],
            font=DEFAULT_FONT,
            bg=BUTTON_COLOR, fg=TEXT_COLOR,
            bd=0, highlightthickness=0, relief="flat",
            anchor="w", padx=15, pady=10,
            activebackground=ACCENT_COLOR, activeforeground=TEXT_COLOR,
            cursor="hand2",
            command=lambda p=app["path"]: self.apps_engine.launch(p)
        )
        row.pack(fill="x", pady=3)
        row.bind("<Enter>", lambda e: row.config(bg=HOVER_COLOR))
        row.bind("<Leave>", lambda e: row.config(bg=BUTTON_COLOR))

    def _start_drag(self, event):
        self._drag_x = event.x
        self._drag_y = event.y

    def _drag_window(self, event):
        x = self.window.winfo_x() + (event.x - self._drag_x)
        y = self.window.winfo_y() + (event.y - self._drag_y)
        self.window.geometry(f"+{x}+{y}")

    def close(self):
        if self.window:
            self.window.destroy()
            self.window = None