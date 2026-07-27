# ===========================
# DivyOS - Theme Manager
# ===========================
#
# Centralizes all colors so every app (notepad, calculator,
# settings, etc.) automatically matches the OS theme and can
# switch between Dark and Light mode with one function call.

from config import (
    BG_COLOR,
    TASKBAR_COLOR,
    START_MENU_COLOR,
    TEXT_COLOR,
    BUTTON_COLOR,
    HOVER_COLOR,
    ACCENT_COLOR,
    BORDER_COLOR,
)

# =========================
# Theme Definitions
# =========================

THEMES = {
    "dark": {
        "bg": BG_COLOR,
        "taskbar": TASKBAR_COLOR,
        "panel": START_MENU_COLOR,
        "text": TEXT_COLOR,
        "button": BUTTON_COLOR,
        "hover": HOVER_COLOR,
        "accent": ACCENT_COLOR,
        "border": BORDER_COLOR,
    },
    "light": {
        "bg": "#F3F3F3",
        "taskbar": "#FFFFFF",
        "panel": "#FFFFFF",
        "text": "#1A1A1A",
        "button": "#E8E8E8",
        "hover": "#D6D6D6",
        "accent": ACCENT_COLOR,   # keep the same Windows blue in both themes
        "border": "#CCCCCC",
    },
}

# Currently active theme name ("dark" or "light")
_current_theme = "dark"


def get_theme():
    """Returns the full color dictionary for the active theme."""
    return THEMES[_current_theme]


def get_color(key):
    """
    Shortcut to get a single color from the active theme.
    Example: get_color("bg") -> "#202020" (in dark mode)
    """
    return THEMES[_current_theme].get(key, "#FF00FF")  # magenta = missing key warning


def set_theme(name):
    """
    Switches the active theme. name must be "dark" or "light".
    Apps should re-read colors (via get_color) after calling this.
    """
    global _current_theme

    if name not in THEMES:
        print(f"[DivyOS] Unknown theme '{name}', staying on '{_current_theme}'")
        return

    _current_theme = name


def toggle_theme():
    """Switches between dark and light mode."""
    set_theme("light" if _current_theme == "dark" else "dark")


def current_theme_name():
    """Returns the name of the currently active theme."""
    return _current_theme