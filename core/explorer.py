import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from core.window import AppWindow


class FileExplorer:

    def __init__(self, root):

        app = AppWindow(root, "📂 File Explorer", 900, 600)

        self.app = app
        self.window = app.content

        app.window.lift()

        # Current user's home folder
        self.current_path = os.path.expanduser("~")

        # =========================
        # Path Bar
        # =========================
        self.path = tk.Label(
            self.window,
            text=self.current_path,
            bg="#303030",
            fg="white",
            anchor="w",
            padx=10,
            pady=5
        )
        self.path.pack(fill="x")

        # =========================
        # Toolbar
        # =========================
        toolbar = tk.Frame(self.window, bg="#252525")
        toolbar.pack(fill="x")

        tk.Button(
            toolbar,
            text="⬅ Back",
            command=self.go_back,
            bg="#404040",
            fg="white"
        ).pack(side="left", padx=5, pady=5)

        tk.Button(
            toolbar,
            text="⬆ Up",
            command=self.go_up,
            bg="#404040",
            fg="white"
        ).pack(side="left", padx=5, pady=5)

        tk.Button(
            toolbar,
            text="🔄 Refresh",
            command=lambda: self.load_directory(self.current_path),
            bg="#404040",
            fg="white"
        ).pack(side="left", padx=5, pady=5)

        # =========================
        # File List
        # =========================
        self.tree = ttk.Treeview(
            self.window,
            columns=("Type", "Size"),
            show="tree headings"
        )

        self.tree.heading("#0", text="Name")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Size", text="Size")

        self.tree.column("#0", width=400)
        self.tree.column("Type", width=120)
        self.tree.column("Size", width=120)

        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<Double-1>", self.open_item)

        self.load_directory(self.current_path)

    # =========================
    # Load Folder
    # =========================
    def load_directory(self, path):

        self.tree.delete(*self.tree.get_children())

        self.current_path = path

        self.path.config(text=path)

        try:

            for item in sorted(os.listdir(path)):

                full = os.path.join(path, item)

                if os.path.isdir(full):

                    self.tree.insert(
                        "",
                        "end",
                        text=item,
                        values=("Folder", "")
                    )

                else:

                    try:
                        size = os.path.getsize(full)

                        if size < 1024:
                            size = f"{size} B"
                        elif size < 1024 * 1024:
                            size = f"{size // 1024} KB"
                        else:
                            size = f"{size // (1024*1024)} MB"

                    except:
                        size = ""

                    self.tree.insert(
                        "",
                        "end",
                        text=item,
                        values=("File", size)
                    )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # =========================
    # Open Folder
    # =========================
    def open_item(self, event):

        selected = self.tree.focus()

        if not selected:
            return

        name = self.tree.item(selected)["text"]

        full = os.path.join(self.current_path, name)

        if os.path.isdir(full):
            self.load_directory(full)

    # =========================
    # Go Up
    # =========================
    def go_up(self):

        parent = os.path.dirname(self.current_path)

        if parent != self.current_path:
            self.load_directory(parent)

    # =========================
    # Back
    # =========================
    def go_back(self):
        self.go_up()