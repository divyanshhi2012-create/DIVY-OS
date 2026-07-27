import os
import tkinter as tk
from tkinter import ttk

from core.window import AppWindow


class FileExplorer:

    def __init__(self, root):

        app = AppWindow(root, "📂 File Explorer", 900, 600)

        self.app = app
        self.window = app.content

        app.window.lift()

        self.current_path = os.path.expanduser("~")

        self.path = tk.Label(
            self.window,
            text=self.current_path,
            bg="#303030",
            fg="white",
            anchor="w",
            padx=10
        )

        self.path.pack(fill="x")

        self.tree = ttk.Treeview(
            self.window,
            columns=("Type",),
            show="tree headings"
        )

        self.tree.heading("#0", text="Name")
        self.tree.heading("Type", text="Type")

        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<Double-1>", self.open_item)

        self.load_directory(self.current_path)

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
                        values=("Folder",)
                    )

                else:

                    self.tree.insert(
                        "",
                        "end",
                        text=item,
                        values=("File",)
                    )

        except Exception as e:

            print(e)

    def open_item(self, event):

        selected = self.tree.focus()

        if not selected:
            return

        name = self.tree.item(selected)["text"]

        full = os.path.join(self.current_path, name)

        if os.path.isdir(full):

            self.load_directory(full)