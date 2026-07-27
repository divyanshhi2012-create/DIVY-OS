# ===========================
# DivyOS - Divy Store
# ===========================
#
# A simple app store front-end for DivyOS. It cannot embed the
# real Microsoft Store (no public API exists for that), but it
# CAN launch the actual Microsoft Store app on Windows and jump
# straight to a search or a specific product page, using the
# official ms-windows-store: URI scheme.
#
# On non-Windows systems, or if the Store isn't available, it
# falls back to opening the Store's web listing in the browser.

import tkinter as tk
import os
import sys
import webbrowser

from core.utils import center_window
from core.theme import get_color
from config import TITLE_FONT, DEFAULT_FONT


class AppStore:

    # A small curated list of featured apps (name -> Store product ID).
    # Product IDs are the 12-character codes Microsoft assigns to each
    # app; you can find them in any Store app's URL.
    FEATURED_APPS = [
        ("Spotify", "9NCBCSZSJRSB"),
        ("WhatsApp", "9NKSQGP7F2NH"),
        ("VLC", "9NBLGGH4VVNH"),
        ("Notion", "9NTHTQD3TCJC"),
    ]

    def __init__(self, root):

        self.root = root

        # =========================
        # Window
        # =========================
        self.window = tk.Toplevel(root)
        self.window.title("Divy Store")

        center_window(self.window, 520, 480)

        self.window.configure(bg=get_color("bg"))
        self.window.resizable(False, False)

        # =========================
        # Header
        # =========================
        tk.Label(
            self.window,
            text="🛍️ Divy Store",
            font=TITLE_FONT,
            bg=get_color("bg"),
            fg=get_color("text")
        ).pack(pady=(20, 5))

        tk.Label(
            self.window,
            text="Powered by Microsoft Store",
            font=("Segoe UI", 9),
            bg=get_color("bg"),
            fg=get_color("hover")
        ).pack(pady=(0, 15))

        # =========================
        # Search Bar
        # =========================
        search_frame = tk.Frame(self.window, bg=get_color("panel"))
        search_frame.pack(fill="x", padx=20, pady=(0, 15))

        self.search_var = tk.StringVar()

        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=DEFAULT_FONT,
            bg=get_color("panel"),
            fg=get_color("text"),
            insertbackground=get_color("text"),
            bd=0,
            relief="flat"
        )
        search_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(10, 0))
        search_entry.bind("<Return>", lambda e: self.search())

        tk.Button(
            search_frame,
            text="🔍 Search Store",
            font=DEFAULT_FONT,
            bg=get_color("accent"),
            fg="#FFFFFF",
            bd=0,
            relief="flat",
            cursor="hand2",
            command=self.search
        ).pack(side="right", padx=5, pady=5)

        # =========================
        # Featured Apps
        # =========================
        tk.Label(
            self.window,
            text="Featured Apps",
            font=("Segoe UI", 13, "bold"),
            bg=get_color("bg"),
            fg=get_color("text")
        ).pack(anchor="w", padx=20, pady=(10, 5))

        list_frame = tk.Frame(self.window, bg=get_color("bg"))
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        for name, product_id in self.FEATURED_APPS:
            self._create_app_row(list_frame, name, product_id)

        # =========================
        # Footer
        # =========================
        tk.Button(
            self.window,
            text="Open Microsoft Store",
            font=DEFAULT_FONT,
            bg=get_color("button"),
            fg=get_color("text"),
            bd=0,
            relief="flat",
            cursor="hand2",
            command=self.open_store_home
        ).pack(pady=(5, 20))

    # ==========================
    # App Row
    # ==========================

    def _create_app_row(self, parent, name, product_id):

        row = tk.Frame(parent, bg=get_color("panel"))
        row.pack(fill="x", pady=4)

        tk.Label(
            row,
            text=name,
            font=DEFAULT_FONT,
            bg=get_color("panel"),
            fg=get_color("text"),
            anchor="w"
        ).pack(side="left", padx=15, pady=10)

        tk.Button(
            row,
            text="Get",
            font=("Segoe UI", 9, "bold"),
            bg=get_color("accent"),
            fg="#FFFFFF",
            bd=0,
            relief="flat",
            cursor="hand2",
            padx=15,
            command=lambda: self.open_product(product_id)
        ).pack(side="right", padx=15, pady=8)

    # ==========================
    # Microsoft Store Integration
    # ==========================

    def open_product(self, product_id):
        """
        Opens a specific app's page in the real Microsoft Store app
        using its official URI scheme. Falls back to the web listing
        if the Store app can't be launched (e.g. not on Windows).
        """
        uri = f"ms-windows-store://pdp/?productid={product_id}"

        if not self._try_open_uri(uri):
            web_url = f"https://apps.microsoft.com/detail/{product_id}"
            webbrowser.open(web_url)

    def search(self):
        """
        Opens the Microsoft Store app with search results for
        whatever the user typed. Falls back to the web Store search
        if the native app can't be launched.
        """
        query = self.search_var.get().strip()

        if not query:
            return

        uri = f"ms-windows-store://search/?query={query.replace(' ', '%20')}"

        if not self._try_open_uri(uri):
            web_url = f"https://apps.microsoft.com/search?query={query.replace(' ', '%20')}"
            webbrowser.open(web_url)

    def open_store_home(self):
        """Opens the Microsoft Store app's home page."""
        uri = "ms-windows-store://home"

        if not self._try_open_uri(uri):
            webbrowser.open("https://apps.microsoft.com/")

    def _try_open_uri(self, uri):
        """
        Attempts to launch a Windows URI (like ms-windows-store:).
        Returns True on apparent success, False if it's not possible
        on this platform (e.g. macOS/Linux, or Store not installed).
        """
        if sys.platform != "win32":
            return False

        try:
            os.startfile(uri)
            return True
        except Exception as e:
            print("Store Launch Error:", e)
            return False