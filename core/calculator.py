# ===========================
# DivyOS - Calculator
# ===========================
#
# A simple calculator app, styled to match the current DivyOS
# theme (dark/light) and using the shared utils system.

import tkinter as tk

from core.utils import center_window, safe_run
from core.theme import get_color
from config import TITLE_FONT


class Calculator:

    BUTTON_LAYOUT = [
        ["C", "⌫", "%", "÷"],
        ["7", "8", "9", "×"],
        ["4", "5", "6", "−"],
        ["1", "2", "3", "+"],
        ["±", "0", ".", "="],
    ]

    # Maps display symbols to real Python operators
    OPERATOR_MAP = {
        "÷": "/",
        "×": "*",
        "−": "-",
        "+": "+",
    }

    def __init__(self, root):

        self.root = root
        self.expression = ""

        # =========================
        # Window
        # =========================
        self.window = tk.Toplevel(root)
        self.window.title("Calculator - DivyOS")

        center_window(self.window, 320, 460)

        self.window.configure(bg=get_color("bg"))
        self.window.resizable(False, False)

        # =========================
        # Display
        # =========================
        self.display_var = tk.StringVar(value="0")

        self.display = tk.Label(
            self.window,
            textvariable=self.display_var,
            bg=get_color("panel"),
            fg=get_color("text"),
            font=("Segoe UI", 32),
            anchor="e",
            padx=15,
            height=2
        )
        self.display.pack(fill="x", padx=10, pady=(15, 10))

        # =========================
        # Button Grid
        # =========================
        grid_frame = tk.Frame(self.window, bg=get_color("bg"))
        grid_frame.pack(fill="both", expand=True, padx=10, pady=10)

        for row_index, row in enumerate(self.BUTTON_LAYOUT):
            grid_frame.rowconfigure(row_index, weight=1)

            for col_index, label in enumerate(row):
                grid_frame.columnconfigure(col_index, weight=1)
                self._create_button(grid_frame, label, row_index, col_index)

        # =========================
        # Keyboard Support
        # =========================
        self.window.bind("<Key>", self._on_key_press)
        self.window.bind("<Return>", lambda e: self._on_button(  "="))
        self.window.bind("<BackSpace>", lambda e: self._on_button("⌫"))
        self.window.focus_set()

    # ==========================
    # Button Creation
    # ==========================

    def _create_button(self, parent, label, row, col):

        is_operator = label in ("÷", "×", "−", "+", "=")
        is_utility = label in ("C", "⌫", "%", "±")

        if label == "=":
            bg = get_color("accent")
        elif is_operator:
            bg = get_color("button")
        elif is_utility:
            bg = get_color("hover")
        else:
            bg = get_color("panel")

        btn = tk.Button(
            parent,
            text=label,
            font=("Segoe UI", 16),
            bg=bg,
            fg=get_color("text"),
            bd=0,
            highlightthickness=0,
            relief="flat",
            activebackground=get_color("accent"),
            activeforeground=get_color("text"),
            cursor="hand2",
            command=lambda: self._on_button(label)
        )

        btn.grid(row=row, column=col, sticky="nsew", padx=4, pady=4, ipady=10)

        return btn

    # ==========================
    # Button Logic
    # ==========================

    def _on_button(self, label):

        if label == "C":
            self.expression = ""

        elif label == "⌫":
            self.expression = self.expression[:-1]

        elif label == "±":
            self._toggle_sign()

        elif label == "%":
            self._apply_percent()

        elif label == "=":
            self._evaluate()
            return

        elif label in self.OPERATOR_MAP:
            self.expression += self.OPERATOR_MAP[label]

        else:
            # Digits and decimal point
            self.expression += label

        self._update_display()

    def _toggle_sign(self):
        if self.expression.startswith("-"):
            self.expression = self.expression[1:]
        else:
            self.expression = "-" + self.expression

    def _apply_percent(self):
        try:
            value = float(self.expression) / 100
            self.expression = self._format_number(value)
        except (ValueError, ZeroDivisionError):
            pass

    def _evaluate(self):
        try:
            # Only allow safe characters - digits, operators, decimal point
            allowed = set("0123456789+-*/(). ")
            if not all(ch in allowed for ch in self.expression):
                raise ValueError("Invalid characters")

            result = eval(self.expression, {"__builtins__": {}})
            self.expression = self._format_number(result)

        except (ZeroDivisionError,):
            self.expression = "Error: ÷0"
        except Exception:
            self.expression = "Error"

        self._update_display()

    def _format_number(self, value):
        """Removes trailing .0 from whole-number results."""
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return str(round(value, 10))

    def _update_display(self):
        text = self.expression if self.expression else "0"

        # Show operators as their pretty symbols on-screen
        for symbol, operator in self.OPERATOR_MAP.items():
            text = text.replace(operator, f" {symbol} ")

        self.display_var.set(text.strip() or "0")

    # ==========================
    # Keyboard Input
    # ==========================

    def _on_key_press(self, event):
        char = event.char

        if char.isdigit() or char == ".":
            self._on_button(char)

        elif char == "+":
            self._on_button("+")
        elif char == "-":
            self._on_button("−")
        elif char == "*":
            self._on_button("×")
        elif char == "/":
            self._on_button("÷")
        elif char == "%":
            self._on_button("%")
        elif char.lower() == "c":
            self._on_button("C")