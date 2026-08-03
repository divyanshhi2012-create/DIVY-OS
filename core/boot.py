# ==============================================================================
# DivyOS - Dynamic HyperOS Booting Screen
# ==============================================================================

import tkinter as tk

from config import APP_NAME, BOOT_TIME, HEIGHT, WIDTH
from core.theme import get_color
from core.utils import draw_rounded_rect


class BootScreen:

    WIN_WIDTH = 520
    WIN_HEIGHT = 350

    def __init__(self, callback):
        self.callback = callback
        self.progress = 0
        self.root = None

    def run(self):
        self.root = tk.Tk()
        self.root.title(APP_NAME)
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)

        # Dynamic Theme Colors
        bg_color = get_color("bg")
        panel_color = get_color("panel")
        border_color = get_color("border")
        accent_color = get_color("accent")
        text_color = get_color("text")
        text_sub = get_color("text_secondary")
        font_family = get_color("font_family")

        self.root.configure(bg=bg_color)

        # Screen Center Alignment
        x = (self.root.winfo_screenwidth() - self.WIN_WIDTH) // 2
        y = (self.root.winfo_screenheight() - self.WIN_HEIGHT) // 2
        self.root.geometry(f"{self.WIN_WIDTH}x{self.WIN_HEIGHT}+{x}+{y}")

        # Rounded Glass Card Background
        self.canvas = tk.Canvas(
            self.root,
            width=self.WIN_WIDTH,
            height=self.WIN_HEIGHT,
            bg=bg_color,
            highlightthickness=0,
        )
        self.canvas.pack(fill="both", expand=True)

        draw_rounded_rect(
            self.canvas,
            0,
            0,
            self.WIN_WIDTH,
            self.WIN_HEIGHT,
            radius=get_color("corner_radius"),
            fill=panel_color,
            outline=border_color,
            width=1,
        )

        content = tk.Frame(self.canvas, bg=panel_color)
        self.canvas.create_window(
            0,
            0,
            window=content,
            anchor="nw",
            width=self.WIN_WIDTH,
            height=self.WIN_HEIGHT,
        )

        # HyperOS Glowing Logo Symbol
        tk.Label(
            content,
            text="✦",
            font=(font_family, 48),
            bg=panel_color,
            fg=accent_color,
        ).pack(pady=(45, 0))

        # Title
        tk.Label(
            content,
            text="DivyOS",
            font=(font_family, 24, "bold"),
            bg=panel_color,
            fg=text_color,
        ).pack(pady=(4, 0))

        # Subtitle
        tk.Label(
            content,
            text="HyperOS Assistant Edition",
            font=(font_family, 10),
            bg=panel_color,
            fg=text_sub,
        ).pack(pady=(2, 28))

        # Modern Rounded Progress Bar
        self.bar_width = 320
        self.bar_height = 6
        self.progress_canvas = tk.Canvas(
            content,
            width=self.bar_width,
            height=self.bar_height,
            bg=get_color("button"),
            highlightthickness=0,
        )
        self.progress_canvas.pack()

        # Dynamic Status Label
        self.status = tk.Label(
            content,
            text="Initializing System Core...",
            font=(font_family, 9),
            bg=panel_color,
            fg=text_sub,
        )
        self.status.pack(pady=(12, 0))

        self.animate()
        self.root.mainloop()

    def animate(self):
        self.progress += 2

        # Draw custom smooth progress bar fill
        w = (self.bar_width * self.progress) / 100
        accent_color = get_color("accent")

        self.progress_canvas.delete("bar")
        self.progress_canvas.create_rectangle(
            0, 0, w, self.bar_height, fill=accent_color, outline="", tags="bar"
        )

        # Update status text dynamically
        if self.progress == 20:
            self.status.config(text="Loading HyperOS Design Tokens...")
        elif self.progress == 50:
            self.status.config(text="Starting DivyAI Assistant Engine...")
        elif self.progress == 80:
            self.status.config(text="Preparing Desktop Environment...")

        if self.progress < 100:
            delay = max(10, BOOT_TIME // 50)
            self.root.after(delay, self.animate)
        else:
            self.status.config(text="Welcome to DivyOS")
            self.root.after(400, self.finish)

    def finish(self):
        self.root.destroy()
        if self.callback:
            self.callback()