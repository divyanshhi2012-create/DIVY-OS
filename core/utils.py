import tkinter as tk
import traceback
from tkinter import messagebox


# ===========================
# Rounded Rectangle Helpers
# ===========================

def rounded_rect_points(x1, y1, x2, y2, radius):
    return [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1,
    ]


def draw_rounded_rect(canvas, x1, y1, x2, y2, radius=20, **kwargs):
    """
    Draw a rounded rectangle on a Canvas.
    """
    points = rounded_rect_points(x1, y1, x2, y2, radius)

    return canvas.create_polygon(
        points,
        smooth=True,
        splinesteps=36,
        **kwargs
    )


# ===========================
# Rounded Button
# ===========================

def make_rounded_button(
    parent,
    text,
    command=None,
    width=160,
    height=48,
    radius=20,
    bg="#2A2A2C",
    hover_bg="#37373A",
    fg="#FFFFFF",
    font=("Segoe UI", 11),
    canvas_bg=None
):

    if canvas_bg is None:
        canvas_bg = parent.cget("bg")

    canvas = tk.Canvas(
        parent,
        width=width,
        height=height,
        bg=canvas_bg,
        highlightthickness=0,
        bd=0
    )

    shape = draw_rounded_rect(
        canvas,
        2,
        2,
        width - 2,
        height - 2,
        radius=radius,
        fill=bg,
        outline=""
    )

    label = canvas.create_text(
        width / 2,
        height / 2,
        text=text,
        fill=fg,
        font=font
    )

    def click(event=None):
        if command:
            command()

    def enter(event=None):
        canvas.itemconfig(shape, fill=hover_bg)

    def leave(event=None):
        canvas.itemconfig(shape, fill=bg)

    canvas.bind("<Button-1>", click)
    canvas.bind("<Enter>", enter)
    canvas.bind("<Leave>", leave)

    canvas.tag_bind(shape, "<Button-1>", click)
    canvas.tag_bind(label, "<Button-1>", click)

    canvas.config(cursor="hand2")

    return canvas


# ===========================
# Window Utilities
# ===========================

def center_window(window, width, height):
    """
    Center a Tkinter window on the screen.
    """

    window.update_idletasks()

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")


# ===========================
# Safe Function Runner
# ===========================

def safe_run(func, *args, **kwargs):
    """
    Execute any function safely without crashing DivyOS.
    """
    try:
        return func(*args, **kwargs)

    except Exception as e:
        traceback.print_exc()

        try:
            messagebox.showerror(
                "DivyOS Error",
                f"An unexpected error occurred:\n\n{e}"
            )
        except Exception:
            pass

        return None