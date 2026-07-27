import tkinter as tk
import os
import sys

from config import APP_NAME, WIDTH, HEIGHT, BG_COLOR, WINDOW_OPACITY, TASKBAR_HEIGHT
from core.taskbar import Taskbar
from core.startmenu import StartMenu
from core.explorer import FileExplorer
from core.terminal import Terminal
from core.browser import Browser
from core.ai import DivyAI
from core.ai_window import AIWindow
from core.notepad import Notepad
from core.calculator import Calculator
from core.settings import Settings
from core.appstore import AppStore

import webbrowser

# Pillow is optional but required for PNG/ICO icon support + resizing.
# If it isn't installed, create_icon() gracefully falls back to emoji.
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class Desktop:

    # Default icon size for image-based desktop icons
    ICON_SIZE = (40, 40)

    # =========================
    # Icon Auto-Layout Settings
    # =========================
    # Icons fill top-to-bottom in a column (like Windows). When a
    # column runs out of vertical space (near the taskbar), the next
    # icon automatically starts a new column to the right.
    ICON_START_X = 20
    ICON_START_Y = 20
    ICON_SPACING_X = 100   # horizontal gap between columns
    ICON_SPACING_Y = 100   # vertical gap between icons in a column

    def __init__(self):

        self.root = tk.Tk()

        self.root.title(APP_NAME)
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        # Windows 11 style glass transparency
        self.root.attributes("-alpha", WINDOW_OPACITY)

        # ==========================
        # DivyOS Icon
        # ==========================
        try:
            icon_path = os.path.join(self._get_base_path(), "assets", "divyos.ico")

            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)

        except Exception as e:
            print("Icon Error:", e)

        self.menu = StartMenu(self.root)
        # Alias kept for compatibility with modules (e.g. DivyAI) that
        # expect a `start_menu` attribute.
        self.start_menu = self.menu

        # ==========================
        # AI Assistant
        # ==========================
        self.ai = DivyAI(self)
        self.ai_window = AIWindow(self)

        # ==========================
        # Icon reference tracking
        # ==========================
        # Keeps hard references to every PhotoImage so Tkinter's garbage
        # collector never silently wipes an icon off the desktop.
        self.icon_images = []
        # Keeps references to the desktop icon widgets themselves so we
        # can refresh/rebuild the desktop without touching the taskbar,
        # start menu, or anything else.
        self.icons = []

        # Live references to currently open core windows/instances so
        # the AI (and other code) can reuse or command them.
        self.browser = None
        self.terminal = None
        self.explorer = None
        self.notepad = None
        self.calculator = None
        self.settings = None
        self.appstore = None

    # ==========================
    # Helpers
    # ==========================

    def _get_base_path(self):
        """Resolve the base path whether running from source or frozen (PyInstaller)."""
        if getattr(sys, "frozen", False):
            return sys._MEIPASS
        return os.path.abspath(".")

    def _load_image(self, image, size=None):
        """
        Attempt to load a PNG/ICO icon from assets/icons/.

        `image` may be:
            - a bare name, e.g. "computer" -> tries computer.png, then computer.ico
            - a filename with extension, e.g. "computer.png"
            - a full/relative path

        Returns a Tkinter-compatible PhotoImage, or None if unavailable.
        """
        if not image or not PIL_AVAILABLE:
            return None

        size = size or self.ICON_SIZE
        icons_dir = os.path.join(self._get_base_path(), "assets", "icons")

        candidates = []

        if os.path.isabs(image) or os.path.sep in image:
            candidates.append(image)
        elif os.path.splitext(image)[1]:
            candidates.append(os.path.join(icons_dir, image))
        else:
            candidates.append(os.path.join(icons_dir, image + ".png"))
            candidates.append(os.path.join(icons_dir, image + ".ico"))

        for path in candidates:
            if os.path.exists(path):
                try:
                    img = Image.open(path)
                    img = img.convert("RGBA")
                    img = img.resize(size, Image.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    self.icon_images.append(photo)  # prevent garbage collection
                    return photo
                except Exception as e:
                    print("Icon Load Error:", path, e)
                    return None

        return None

    # ==========================
    # Reusable Desktop Icon System
    # ==========================

    def create_icon(self, image=None, emoji=None, text="", x=0, y=0,
                     command=None, width=90, height=80):
        """
        Create a single desktop icon.

        image   -> name/path of a PNG or ICO in assets/icons/ (auto resized)
        emoji   -> fallback emoji shown if no image is found
        text    -> label shown below the icon
        x, y    -> absolute placement on the desktop
        command -> function called on click

        The icon graphic is always rendered above the text (compound="top"),
        and styling matches the DivyOS dark, borderless, "transparent" look.
        """

        photo = self._load_image(image) if image else None

        if photo is not None:
            btn = tk.Button(
                self.root,
                image=photo,
                text=text,
                compound="top",
                font=("Segoe UI", 9),
                bg=BG_COLOR,
                fg="white",
                bd=0,
                highlightthickness=0,
                relief="flat",
                activebackground="#3B4252",
                activeforeground="white",
                cursor="hand2",
                justify="center",
                command=command
            )
            # Extra safety reference, on top of self.icon_images
            btn.image = photo
        else:
            display_emoji = emoji if emoji else "❔"
            btn = tk.Button(
                self.root,
                text=f"{display_emoji}\n{text}",
                font=("Segoe UI", 11),
                bg=BG_COLOR,
                fg="white",
                bd=0,
                highlightthickness=0,
                relief="flat",
                activebackground="#3B4252",
                activeforeground="white",
                cursor="hand2",
                justify="center",
                command=command
            )

        btn.place(x=x, y=y, width=width, height=height)
        self.icons.append(btn)
        return btn

    def _icon_position(self, index):
        """
        Calculates (x, y) for the icon at `index` (0, 1, 2, ...).

        Icons fill top-to-bottom first. Once a column reaches the
        bottom of the usable desktop area (just above the taskbar),
        the next icon automatically wraps to a new column, starting
        again from the top - just like Windows.
        """

        # Usable vertical space above the taskbar
        usable_height = HEIGHT - TASKBAR_HEIGHT - self.ICON_START_Y

        # How many icons fit in a single column before wrapping
        rows_per_column = max(1, usable_height // self.ICON_SPACING_Y)

        col = index // rows_per_column
        row = index % rows_per_column

        x = self.ICON_START_X + (col * self.ICON_SPACING_X)
        y = self.ICON_START_Y + (row * self.ICON_SPACING_Y)

        return x, y

    def _load_desktop_icons(self):
        """
        Creates every default desktop icon.

        Positions are calculated automatically with _icon_position(),
        so icons fill downward and wrap into a new column near the
        taskbar instead of running off the bottom of the screen.
        """

        icon_defs = [
            dict(image="computer",   emoji="💻", text="Computer",    command=self.open_explorer),
            dict(image="folder",     emoji="📂", text="Files",       command=self.open_explorer),
            dict(image="terminal",   emoji="💻", text="Terminal",    command=self.open_terminal),
            dict(image="browser",    emoji="🌐", text="Browser",     command=self.open_browser),
            dict(image="recyclebin", emoji="🗑️", text="Recycle Bin", command=self.open_explorer),
            dict(image="ai",         emoji="🤖", text="DivyAI",      command=self.ai_window.open),
            dict(image="notepad",    emoji="📝", text="Notepad",     command=self.open_notepad),
            dict(image="calculator", emoji="🧮", text="Calculator",  command=self.open_calculator),
            dict(image="settings",   emoji="⚙️", text="Settings",    command=self.open_settings),
            dict(image="appstore",   emoji="🛍️", text="Divy Store",  command=self.open_appstore),
        ]

        for index, icon_def in enumerate(icon_defs):
            x, y = self._icon_position(index)

            self.create_icon(
                image=icon_def["image"],
                emoji=icon_def["emoji"],
                text=icon_def["text"],
                x=x,
                y=y,
                command=icon_def["command"]
            )

    def refresh_desktop(self):
        """Rebuilds only the desktop icons (taskbar/start menu untouched)."""
        for icon in self.icons:
            icon.destroy()

        self.icons.clear()
        self.icon_images.clear()

        self._load_desktop_icons()

    # ==========================
    # Window / App Launchers
    # ==========================

    def open_explorer(self):
        self.explorer = FileExplorer(self.root)
        return self.explorer

    def open_terminal(self):
        self.terminal = Terminal(self.root)
        return self.terminal

    def open_browser(self):
        self.browser = Browser()
        self.browser.open()
        return self.browser

    def open_notepad(self):
        self.notepad = Notepad(self.root)
        return self.notepad

    def open_calculator(self):
        self.calculator = Calculator(self.root)
        return self.calculator

    def open_settings(self):
        self.settings = Settings(self.root, desktop=self)
        return self.settings

    def open_appstore(self):
        self.appstore = AppStore(self.root)
        return self.appstore

    # ==========================
    # Power / Session Controls
    # ==========================

    def show_desktop(self):
        """Minimizes any open Toplevel windows, revealing the desktop."""
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Toplevel):
                try:
                    widget.withdraw()
                except Exception:
                    pass

    def lock(self):
        """Displays a simple full-screen lock overlay."""
        lock_screen = tk.Toplevel(self.root)
        lock_screen.attributes("-fullscreen", True)
        lock_screen.configure(bg="#000000")
        lock_screen.attributes("-topmost", True)

        tk.Label(
            lock_screen,
            text="🔒 DivyOS Locked",
            font=("Segoe UI", 28, "bold"),
            bg="#000000",
            fg="white"
        ).place(relx=0.5, rely=0.45, anchor="center")

        tk.Button(
            lock_screen,
            text="Unlock",
            font=("Segoe UI", 14),
            bg="#3B4252",
            fg="white",
            bd=0,
            command=lock_screen.destroy
        ).place(relx=0.5, rely=0.55, anchor="center")

    def shutdown(self):
        """Closes DivyOS."""
        try:
            self.root.destroy()
        finally:
            sys.exit(0)

    def restart(self):
        """Closes and relaunches DivyOS."""
        self.root.destroy()
        os.execl(sys.executable, sys.executable, *sys.argv)

    # ==========================
    # AI Command Execution
    # ==========================

    def run_ai_command(self, command):
        """
        Central entry point for AI-driven desktop actions.

        Supported commands:
            ai/divyai, browser, terminal, explorer, settings,
            calculator, notepad, recycle bin, show desktop,
            refresh desktop, shutdown, restart, search <query>,
            appstore/store
        """

        if not command:
            return

        cmd = command.strip().lower()

        try:
            if cmd in ("ai", "divyai"):
                self.ai_window.open()

            elif cmd == "browser":
                self.open_browser()

            elif cmd == "terminal":
                self.open_terminal()

            elif cmd in ("explorer", "files", "computer"):
                self.open_explorer()

            elif cmd == "recycle bin":
                self.open_explorer()

            elif cmd == "show desktop":
                self.show_desktop()

            elif cmd == "refresh desktop":
                self.refresh_desktop()

            elif cmd == "shutdown":
                self.shutdown()

            elif cmd == "restart":
                self.restart()

            elif cmd == "lock":
                self.lock()

            elif cmd.startswith("search "):
                query = command[len("search "):].strip()
                if query:
                    webbrowser.open(
                        "https://www.google.com/search?q=" + query
                    )

            elif cmd == "settings":
                self.open_settings()

            elif cmd == "calculator":
                self.open_calculator()

            elif cmd == "notepad":
                self.open_notepad()

            elif cmd in ("appstore", "store", "divy store"):
                self.open_appstore()

            else:
                self.ai.execute(command)

        except Exception as e:
            print(f"AI Command Error [{command}]:", e)

    def _launch_optional_app(self, module_path, class_name):
        """
        Attempts to launch apps that may not be implemented yet
        without crashing DivyOS if the module doesn't exist.
        """
        try:
            module = __import__(module_path, fromlist=[class_name])
            app_class = getattr(module, class_name)
            app_class(self.root)
        except Exception:
            print(f"'{class_name}' is not available yet in this DivyOS build.")

    # ==========================
    # Right Click Menu
    # ==========================

    def show_menu(self, event):

        menu = tk.Menu(
            self.root,
            tearoff=0,
            bg="#2E3440",
            fg="white",
            activebackground="#4C566A",
            activeforeground="white"
        )

        menu.add_command(label="🔄 Refresh", command=self.refresh_desktop)

        menu.add_separator()

        menu.add_command(
            label="📂 File Explorer",
            command=self.open_explorer
        )

        menu.add_command(
            label="💻 Terminal",
            command=self.open_terminal
        )

        menu.add_command(
            label="🌐 Browser",
            command=self.open_browser
        )

        menu.add_command(
            label="📝 Notepad",
            command=self.open_notepad
        )

        menu.add_command(
            label="🧮 Calculator",
            command=self.open_calculator
        )

        menu.add_command(
            label="⚙️ Settings",
            command=self.open_settings
        )

        menu.add_command(
            label="🛍️ Divy Store",
            command=self.open_appstore
        )

        menu.add_separator()

        menu.add_command(
            label="🖥️ Show Desktop",
            command=self.show_desktop
        )

        menu.add_command(
            label="🔒 Lock",
            command=self.lock
        )

        menu.add_separator()

        menu.add_command(
            label="🔁 Restart",
            command=self.restart
        )

        menu.add_command(
            label="⏻ Shutdown",
            command=self.shutdown
        )

        menu.add_separator()

        menu.add_command(
            label="❌ Exit DivyOS",
            command=self.root.destroy
        )

        menu.tk_popup(event.x_root, event.y_root)

    # ==========================
    # Run Desktop
    # ==========================

    def run(self):

        self._load_desktop_icons()

        self.root.bind("<Button-3>", self.show_menu)

        self.taskbar = Taskbar(
            self.root,
            self.menu.toggle
        )

        tk.Label(
            self.root,
            text="DivyOS v1.0",
            font=("Segoe UI", 14),
            bg=BG_COLOR,
            fg="white"
        ).place(
            relx=1.0,
            rely=1.0,
            anchor="se",
            x=-20,
            y=-60
        )

        self.root.mainloop()