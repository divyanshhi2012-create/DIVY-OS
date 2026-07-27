# ===========================
# DivyOS - Notepad
# ===========================
#
# A simple text editor, styled to match the current DivyOS
# theme (dark/light) and using the shared utils/icons system.

import tkinter as tk
from tkinter import filedialog, messagebox

from core.utils import center_window
from core.theme import get_color
from config import DEFAULT_FONT, TITLE_FONT


class Notepad:

    def __init__(self, root, filepath=None):

        self.root = root
        self.filepath = filepath

        # =========================
        # Window
        # =========================
        self.window = tk.Toplevel(root)
        self.window.title("Notepad - DivyOS")

        center_window(self.window, 700, 500)

        self.window.configure(bg=get_color("bg"))
        self.window.minsize(400, 300)

        # =========================
        # Menu Bar
        # =========================
        self.menu_bar = tk.Menu(self.window)

        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.window.destroy)

        self.menu_bar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Cut", command=lambda: self.text.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", command=lambda: self.text.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", command=lambda: self.text.event_generate("<<Paste>>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=self.select_all)

        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)

        self.window.config(menu=self.menu_bar)

        # =========================
        # Text Area
        # =========================
        self.text = tk.Text(
            self.window,
            bg=get_color("panel"),
            fg=get_color("text"),
            insertbackground=get_color("text"),   # cursor color
            selectbackground=get_color("accent"),
            selectforeground="#FFFFFF",
            font=("Consolas", 12),
            bd=0,
            wrap="word",
            undo=True
        )
        self.text.pack(fill="both", expand=True, padx=2, pady=2)

        # =========================
        # Status Bar
        # =========================
        self.status_bar = tk.Label(
            self.window,
            text="Ln 1, Col 1",
            bg=get_color("taskbar"),
            fg=get_color("text"),
            font=DEFAULT_FONT,
            anchor="e"
        )
        self.status_bar.pack(fill="x", side="bottom")

        self.text.bind("<KeyRelease>", self._update_status)
        self.text.bind("<ButtonRelease>", self._update_status)

        # =========================
        # Keyboard Shortcuts
        # =========================
        self.window.bind("<Control-n>", lambda e: self.new_file())
        self.window.bind("<Control-o>", lambda e: self.open_file())
        self.window.bind("<Control-s>", lambda e: self.save_file())

        # Warn before closing if there are unsaved changes
        self.window.protocol("WM_DELETE_WINDOW", self.close)

        # Load a file immediately if one was passed in
        if self.filepath:
            self._load_into_editor(self.filepath)

        self.text.focus_set()

    # ==========================
    # File Actions
    # ==========================

    def new_file(self):
        if self._confirm_discard_changes():
            self.text.delete("1.0", tk.END)
            self.filepath = None
            self.window.title("Notepad - DivyOS")

    def open_file(self):
        path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if path:
            self._load_into_editor(path)

    def _load_into_editor(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            self.text.delete("1.0", tk.END)
            self.text.insert("1.0", content)
            self.filepath = path
            self.window.title(f"Notepad - {path.split('/')[-1].split(chr(92))[-1]}")

        except Exception as e:
            messagebox.showerror("Error", f"Could not open file:\n{e}")

    def save_file(self):
        if self.filepath:
            self._write_to_disk(self.filepath)
        else:
            self.save_file_as()

    def save_file_as(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if path:
            self.filepath = path
            self._write_to_disk(path)

    def _write_to_disk(self, path):
        try:
            content = self.text.get("1.0", "end-1c")
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

            self.window.title(f"Notepad - {path.split('/')[-1].split(chr(92))[-1]}")

        except Exception as e:
            messagebox.showerror("Error", f"Could not save file:\n{e}")

    def select_all(self):
        self.text.tag_add("sel", "1.0", "end")

    # ==========================
    # Helpers
    # ==========================

    def _update_status(self, event=None):
        line, col = self.text.index(tk.INSERT).split(".")
        self.status_bar.config(text=f"Ln {line}, Col {int(col) + 1}")

    def _confirm_discard_changes(self):
        """Placeholder for a future 'unsaved changes' check."""
        return True

    def close(self):
        self.window.destroy()