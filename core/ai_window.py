# ==============================================================================
# DivyOS - DivyAI Window (HyperOS Assistant Edition)
# ==============================================================================

import tkinter as tk

from config import WINDOW_OPACITY
from core.theme import get_color, get_theme
from core.utils import center_window, draw_rounded_rect


class AIWindow:

    WIDTH = 440
    HEIGHT = 540

    def __init__(self, desktop):
        """
        desktop -> reference to the Desktop instance, so commands
                   typed here can be routed to run_ai_command().
        """
        self.desktop = desktop
        self.root = desktop.root
        self.window = None
        self.history_box = None
        self.entry_var = None

    def open(self):
        """Opens the DivyAI window, or focuses it if already open."""

        if self.window and self.window.winfo_exists():
            self.window.lift()
            self.window.focus_force()
            return

        # Dynamic Theme Colors
        panel_color = get_color("panel")
        bg_color = get_color("bg")
        text_color = get_color("text")
        accent_color = get_color("accent")
        border_color = get_color("border")
        button_color = get_color("button")
        hover_color = get_color("hover")
        font_family = get_color("font_family")

        self.window = tk.Toplevel(self.root)
        self.window.title("DivyAI Assistant")
        self.window.overrideredirect(True)
        self.window.attributes("-alpha", WINDOW_OPACITY)
        self.window.configure(bg=bg_color)

        center_window(self.window, self.WIDTH, self.HEIGHT)

        # ======================================================================
        # HyperOS Card Background Canvas
        # ======================================================================
        canvas = tk.Canvas(
            self.window,
            width=self.WIDTH,
            height=self.HEIGHT,
            bg=bg_color,
            highlightthickness=0,
        )
        canvas.pack(fill="both", expand=True)

        draw_rounded_rect(
            canvas,
            0,
            0,
            self.WIDTH,
            self.HEIGHT,
            radius=get_color("corner_radius"),
            fill=panel_color,
            outline=border_color,
            width=1,
        )

        content = tk.Frame(canvas, bg=panel_color)
        canvas.create_window(
            0,
            0,
            window=content,
            anchor="nw",
            width=self.WIDTH,
            height=self.HEIGHT,
        )

        # ======================================================================
        # Header (HyperOS Assistant Bar)
        # ======================================================================
        header = tk.Frame(content, bg=panel_color)
        header.pack(fill="x", pady=(16, 8), padx=18)

        title_label = tk.Label(
            header,
            text="✦ DivyAI Assistant",
            font=(font_family, 13, "bold"),
            bg=panel_color,
            fg=accent_color,
        )
        title_label.pack(side="left")

        close_btn = tk.Button(
            header,
            text="✕",
            font=(font_family, 11, "bold"),
            bg=panel_color,
            fg=text_color,
            bd=0,
            highlightthickness=0,
            relief="flat",
            activebackground=hover_color,
            activeforeground=accent_color,
            cursor="hand2",
            command=self.close,
        )
        close_btn.pack(side="right")
        close_btn.bind(
            "<Enter>", lambda e: close_btn.config(bg=hover_color, fg="#FF3B30")
        )
        close_btn.bind(
            "<Leave>", lambda e: close_btn.config(bg=panel_color, fg=text_color)
        )

        # ======================================================================
        # Chat / Command History Frame
        # ======================================================================
        history_frame = tk.Frame(content, bg=button_color)
        history_frame.pack(fill="both", expand=True, padx=18, pady=8)

        self.history_box = tk.Text(
            history_frame,
            bg=button_color,
            fg=text_color,
            font=(font_family, 10),
            bd=0,
            wrap="word",
            state="disabled",
            padx=12,
            pady=12,
            insertbackground=text_color,
        )
        self.history_box.pack(fill="both", expand=True)

        self._print_message(
            "DivyAI",
            "Hello! I am your HyperOS Assistant.\n"
            "Commands: notepad, calculator, settings, browser, terminal, "
            "explorer, appstore, search <query>, shutdown, restart",
        )

        # ======================================================================
        # Quick Command Chips (HyperOS Pill Buttons)
        # ======================================================================
        chips_frame = tk.Frame(content, bg=panel_color)
        chips_frame.pack(fill="x", padx=18, pady=(4, 8))

        quick_commands = ["notepad", "calculator", "settings", "browser"]
        for cmd in quick_commands:
            self._create_chip(chips_frame, cmd)

        # ======================================================================
        # Input Field & Send Action
        # ======================================================================
        input_row = tk.Frame(content, bg=panel_color)
        input_row.pack(fill="x", padx=18, pady=(4, 18))

        self.entry_var = tk.StringVar()

        entry = tk.Entry(
            input_row,
            textvariable=self.entry_var,
            font=(font_family, 10),
            bg=button_color,
            fg=text_color,
            insertbackground=text_color,
            bd=0,
            relief="flat",
        )
        entry.pack(
            side="left", fill="x", expand=True, ipady=10, padx=(0, 10)
        )
        entry.bind("<Return>", lambda e: self._send())
        entry.focus_set()

        send_btn = tk.Button(
            input_row,
            text="➔",
            font=(font_family, 12, "bold"),
            bg=accent_color,
            fg="#FFFFFF",
            bd=0,
            highlightthickness=0,
            relief="flat",
            cursor="hand2",
            width=3,
            activebackground=get_color("accent_hover"),
            activeforeground="#FFFFFF",
            command=self._send,
        )
        send_btn.pack(side="right")

        # Allow dragging the window by its header
        header.bind("<B1-Motion>", self._drag_window)
        header.bind("<ButtonPress-1>", self._start_drag)

    # ==========================================================================
    # Window Dragging Mechanics
    # ==========================================================================

    def _start_drag(self, event):
        self._drag_x = event.x
        self._drag_y = event.y

    def _drag_window(self, event):
        x = self.window.winfo_x() + (event.x - self._drag_x)
        y = self.window.winfo_y() + (event.y - self._drag_y)
        self.window.geometry(f"+{x}+{y}")

    # ==========================================================================
    # Quick Command Chips Creation
    # ==========================================================================

    def _create_chip(self, parent, command_text):
        button_color = get_color("button")
        hover_color = get_color("hover")
        text_color = get_color("text")
        font_family = get_color("font_family")

        chip = tk.Button(
            parent,
            text=command_text,
            font=(font_family, 9),
            bg=button_color,
            fg=text_color,
            bd=0,
            highlightthickness=0,
            relief="flat",
            padx=10,
            pady=4,
            cursor="hand2",
            command=lambda: self._run_command(command_text),
        )
        chip.pack(side="left", padx=(0, 6))
        chip.bind("<Enter>", lambda e: chip.config(bg=hover_color))
        chip.bind("<Leave>", lambda e: chip.config(bg=button_color))
        return chip

    # ==========================================================================
    # Command Handling
    # ==========================================================================

    def _send(self):
        text = self.entry_var.get().strip()
        if not text:
            return

        self.entry_var.set("")
        self._run_command(text)

    def _run_command(self, command):
        self._print_message("You", command)

        if hasattr(self.desktop, "run_ai_command"):
            self.desktop.run_ai_command(command)
            self._print_message("DivyAI", f"Executed: {command}")
        else:
            self._print_message(
                "DivyAI", "Desktop system connection unavailable."
            )

    # ==========================================================================
    # Message Printing & Tagging
    # ==========================================================================

    def _print_message(self, sender, text):
        accent_color = get_color("accent")
        text_color = get_color("text")
        font_family = get_color("font_family")

        self.history_box.config(state="normal")
        self.history_box.insert("end", f"{sender}\n", ("sender",))
        self.history_box.insert("end", f"{text}\n\n", ("body",))

        self.history_box.tag_config(
            "sender",
            foreground=accent_color,
            font=(font_family, 10, "bold"),
        )
        self.history_box.tag_config(
            "body", foreground=text_color, font=(font_family, 10)
        )

        self.history_box.see("end")
        self.history_box.config(state="disabled")

    # ==========================================================================
    # Close Action
    # ==========================================================================

    def close(self):
        if self.window:
            self.window.destroy()
            self.window = None