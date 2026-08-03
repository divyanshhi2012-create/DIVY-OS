# ==============================================================================
# DivyOS - Desktop Core (HyperOS Edition)
# ==============================================================================

import os
import sys
import tkinter as tk
import webbrowser

from config import APP_NAME, HEIGHT, TASKBAR_HEIGHT, WINDOW_OPACITY, WIDTH
from core.ai import DivyAI
from core.ai_window import AIWindow
from core.appstore import AppStore
from core.browser import Browser
from core.calculator import Calculator
from core.explorer import FileExplorer
from core.notepad import Notepad
from core.programs_window import ProgramsWindow
from core.settings import Settings
from core.startmenu import StartMenu
from core.taskbar import Taskbar
from core.terminal import Terminal
from core.theme import get_color, get_theme
from core.utils import draw_rounded_rect

try:
    from PIL import Image, ImageTk

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class Desktop:

    ICON_SIZE = (34, 34)

    ICON_START_X = 24
    ICON_START_Y = 24
    ICON_SPACING_X = 105
    ICON_SPACING_Y = 115

    def __init__(self):

        self.root = tk.Tk()

        # Dynamic Theme Initialization
        bg_color = get_color("bg")

        self.root.title(APP_NAME)
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.configure(bg=bg_color)
        self.root.resizable(False, False)

        self.root.attributes("-alpha", WINDOW_OPACITY)

        try:
            icon_path = os.path.join(
                self._get_base_path(), "assets", "divyos.ico"
            )
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception as e:
            print("Icon Error:", e)

        self.menu = StartMenu(self.root, desktop=self)
        self.start_menu = self.menu

        self.ai = DivyAI(self)
        self.ai_window = AIWindow(self)
        self.programs_window = ProgramsWindow(self.root)

        self.icon_images = []
        self.icons = []

        self.browser = None
        self.terminal = None
        self.explorer = None
        self.notepad = None
        self.calculator = None
        self.settings = None
        self.appstore = None

    def _get_base_path(self):
        if getattr(sys, "frozen", False):
            return sys._MEIPASS
        return os.path.abspath(".")

    def _load_image(self, image, size=None):
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
                    self.icon_images.append(photo)
                    return photo
                except Exception as e:
                    print("Icon Load Error:", path, e)
                    return None

        return None

    def create_icon(
        self,
        image=None,
        emoji=None,
        text="",
        x=0,
        y=0,
        command=None,
        width=90,
        height=95,
    ):
        """
        HyperOS-style rounded desktop icon tile with smooth hover effects.
        """
        tile_size = 60
        bg_color = get_color("bg")
        tile_bg = get_color("panel")
        accent_color = get_color("accent")
        text_color = get_color("text")
        font_family = get_color("font_family")
        corner_radius = get_color("corner_radius")

        canvas = tk.Canvas(
            self.root,
            width=width,
            height=height,
            bg=bg_color,
            highlightthickness=0,
        )
        canvas.place(x=x, y=y, width=width, height=height)

        tile_x = (width - tile_size) // 2

        shape = draw_rounded_rect(
            canvas,
            tile_x,
            0,
            tile_x + tile_size,
            tile_size,
            radius=corner_radius,
            fill=tile_bg,
            outline=get_color("border"),
            width=1,
        )

        photo = self._load_image(image, size=(32, 32)) if image else None

        if photo is not None:
            icon_item = canvas.create_image(
                width / 2, tile_size / 2, image=photo
            )
            canvas.image = photo
            self.icon_images.append(photo)
        else:
            display_emoji = emoji if emoji else "✦"
            icon_item = canvas.create_text(
                width / 2,
                tile_size / 2,
                text=display_emoji,
                font=(font_family, 22),
                fill=text_color,
            )

        label_item = canvas.create_text(
            width / 2,
            tile_size + 16,
            text=text,
            fill=text_color,
            font=(font_family, 9, "bold"),
        )

        def on_click(event=None):
            if command:
                command()

        def on_enter(event=None):
            canvas.itemconfig(shape, fill=get_color("hover"), outline=accent_color)

        def on_leave(event=None):
            canvas.itemconfig(shape, fill=tile_bg, outline=get_color("border"))

        canvas.tag_bind(shape, "<Button-1>", on_click)
        canvas.tag_bind(icon_item, "<Button-1>", on_click)
        canvas.tag_bind(label_item, "<Button-1>", on_click)
        canvas.bind("<Enter>", on_enter)
        canvas.bind("<Leave>", on_leave)
        canvas.config(cursor="hand2")

        self.icons.append(canvas)
        return canvas

    def _icon_position(self, index):
        usable_height = HEIGHT - TASKBAR_HEIGHT - self.ICON_START_Y
        rows_per_column = max(1, usable_height // self.ICON_SPACING_Y)

        col = index // rows_per_column
        row = index % rows_per_column

        x = self.ICON_START_X + (col * self.ICON_SPACING_X)
        y = self.ICON_START_Y + (row * self.ICON_SPACING_Y)

        return x, y

    def _load_desktop_icons(self):
        icon_defs = [
            dict(
                image="computer",
                emoji="💻",
                text="Computer",
                command=self.open_explorer,
            ),
            dict(
                image="folder",
                emoji="📂",
                text="Files",
                command=self.open_explorer,
            ),
            dict(
                image="terminal",
                emoji="⚡",
                text="Terminal",
                command=self.open_terminal,
            ),
            dict(
                image="browser",
                emoji="🌐",
                text="Browser",
                command=self.open_browser,
            ),
            dict(
                image="recyclebin",
                emoji="🗑️",
                text="Recycle Bin",
                command=self.open_explorer,
            ),
            dict(
                image="ai",
                emoji="✦",
                text="DivyAI",
                command=self.ai_window.open,
            ),
            dict(
                image="notepad",
                emoji="📝",
                text="Notepad",
                command=self.open_notepad,
            ),
            dict(
                image="calculator",
                emoji="🧮",
                text="Calculator",
                command=self.open_calculator,
            ),
            dict(
                image="settings",
                emoji="⚙️",
                text="Settings",
                command=self.open_settings,
            ),
            dict(
                image="appstore",
                emoji="🛍️",
                text="Divy Store",
                command=self.open_appstore,
            ),
            dict(
                image="programs",
                emoji="🗂️",
                text="Programs",
                command=self.open_programs,
            ),
        ]

        for index, icon_def in enumerate(icon_defs):
            x, y = self._icon_position(index)
            self.create_icon(
                image=icon_def["image"],
                emoji=icon_def["emoji"],
                text=icon_def["text"],
                x=x,
                y=y,
                command=icon_def["command"],
            )

    def refresh_desktop(self):
        self.root.configure(bg=get_color("bg"))
        for icon in self.icons:
            icon.destroy()
        self.icons.clear()
        self.icon_images.clear()
        self._load_desktop_icons()

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

    def open_programs(self):
        self.programs_window.open()
        return self.programs_window

    def show_desktop(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Toplevel):
                try:
                    widget.withdraw()
                except Exception:
                    pass

    def lock(self):
        bg_color = get_color("bg")
        accent_color = get_color("accent")
        text_color = get_color("text")
        font_family = get_color("font_family")

        lock_screen = tk.Toplevel(self.root)
        lock_screen.attributes("-fullscreen", True)
        lock_screen.configure(bg=bg_color)
        lock_screen.attributes("-topmost", True)

        tk.Label(
            lock_screen,
            text="🔒 DivyOS Locked",
            font=(font_family, 28, "bold"),
            bg=bg_color,
            fg=text_color,
        ).place(relx=0.5, rely=0.45, anchor="center")

        tk.Button(
            lock_screen,
            text="Unlock System",
            font=(font_family, 12, "bold"),
            bg=accent_color,
            fg="#FFFFFF",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2",
            command=lock_screen.destroy,
        ).place(relx=0.5, rely=0.55, anchor="center")

    def shutdown(self):
        try:
            self.root.destroy()
        finally:
            sys.exit(0)

    def restart(self):
        self.root.destroy()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def run_ai_command(self, command):
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
                query = command[len("search ") :].strip()
                if query:
                    webbrowser.open("https://www.google.com/search?q=" + query)
            elif cmd == "settings":
                self.open_settings()
            elif cmd == "calculator":
                self.open_calculator()
            elif cmd == "notepad":
                self.open_notepad()
            elif cmd in ("appstore", "store", "divy store"):
                self.open_appstore()
            elif cmd in ("programs", "installed apps", "windows apps"):
                self.open_programs()
            else:
                self.ai.execute(command)
        except Exception as e:
            print(f"AI Command Error [{command}]:", e)

    def show_menu(self, event):
        panel_color = get_color("panel")
        text_color = get_color("text")
        hover_color = get_color("hover")

        menu = tk.Menu(
            self.root,
            tearoff=0,
            bg=panel_color,
            fg=text_color,
            activebackground=hover_color,
            activeforeground=text_color,
            bd=1,
            relief="solid",
        )

        menu.add_command(label="🔄 Refresh", command=self.refresh_desktop)
        menu.add_separator()
        menu.add_command(label="📂 File Explorer", command=self.open_explorer)
        menu.add_command(label="⚡ Terminal", command=self.open_terminal)
        menu.add_command(label="🌐 Browser", command=self.open_browser)
        menu.add_command(label="📝 Notepad", command=self.open_notepad)
        menu.add_command(label="🧮 Calculator", command=self.open_calculator)
        menu.add_command(label="⚙️ Settings", command=self.open_settings)
        menu.add_command(label="🛍️ Divy Store", command=self.open_appstore)
        menu.add_command(label="🗂️ Programs", command=self.open_programs)
        menu.add_separator()
        menu.add_command(label="🖥️ Show Desktop", command=self.show_desktop)
        menu.add_command(label="🔒 Lock", command=self.lock)
        menu.add_separator()
        menu.add_command(label="🔁 Restart", command=self.restart)
        menu.add_command(label="⏻ Shutdown", command=self.shutdown)
        menu.add_separator()
        menu.add_command(label="❌ Exit DivyOS", command=self.root.destroy)

        menu.tk_popup(event.x_root, event.y_root)

    def run(self):
        self._load_desktop_icons()
        self.root.bind("<Button-3>", self.show_menu)

        self.taskbar = Taskbar(self.root, self.menu.toggle)

        tk.Label(
            self.root,
            text="DivyOS (HyperOS Edition)",
            font=(get_color("font_family"), 11, "bold"),
            bg=get_color("bg"),
            fg=get_color("text_secondary"),
        ).place(relx=1.0, rely=1.0, anchor="se", x=-24, y=-65)

        self.root.mainloop()