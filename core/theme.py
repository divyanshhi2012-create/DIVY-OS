# ==============================================================================
# DivyOS - Theme Manager (HyperOS Edition)
# ==============================================================================
#
# Centralizes all design tokens (colors, fonts, radii) so every app 
# (notepad, calculator, settings, taskbar, etc.) automatically matches the OS theme.

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

# ==============================================================================
# Theme Definitions
# ==============================================================================

THEMES = {
    # Xiaomi HyperOS Dark Theme (Default)
    "hyperos": {
        "bg": "#0A0A0C",          # Pure Dark AMOLED Background
        "taskbar": "#121215",     # Floating Dock Glass Color
        "panel": "#1C1C1E",       # Rounded Card / Control Center Panel
        "text": "#FFFFFF",        # High Contrast Primary Text
        "text_secondary": "#8E8E93", # Subtitle / Hint Text
        "button": "#2C2C2E",      # Control Tile Button
        "hover": "#3A3A3C",       # Soft Hover Glow
        "accent": "#FF5B00",      # Signature Xiaomi HyperOS Orange
        "accent_hover": "#E05000",# Darker Orange on Hover
        "border": "#2C2C2E",      # Subtle Glass Border
        "active_glow": "#FF5B00", # Active Window Indicator
        "font_family": "Segoe UI",
        "corner_radius": 16,      # HyperOS Signature Curved Corners
    },
    "dark": {
        "bg": BG_COLOR,
        "taskbar": TASKBAR_COLOR,
        "panel": START_MENU_COLOR,
        "text": TEXT_COLOR,
        "text_secondary": "#A0A0A0",
        "button": BUTTON_COLOR,
        "hover": HOVER_COLOR,
        "accent": ACCENT_COLOR,
        "accent_hover": ACCENT_COLOR,
        "border": BORDER_COLOR,
        "active_glow": ACCENT_COLOR,
        "font_family": "Segoe UI",
        "corner_radius": 8,
    },
    "light": {
        "bg": "#F2F2F7",          # HyperOS Soft Gray Light BG
        "taskbar": "#FFFFFF",
        "panel": "#FFFFFF",
        "text": "#000000",
        "text_secondary": "#6C6C70",
        "button": "#E5E5EA",
        "hover": "#D1D1D6",
        "accent": "#FF5B00",      # HyperOS Accent maintained in Light mode
        "accent_hover": "#E05000",
        "border": "#E5E5EA",
        "active_glow": "#FF5B00",
        "font_family": "Segoe UI",
        "corner_radius": 16,
    },
}

# Currently active theme name ("hyperos", "dark", or "light")
_current_theme = "hyperos"


def get_theme():
    """Returns the full color dictionary for the active theme."""
    return THEMES[_current_theme]


def get_color(key):
    """
    Shortcut to get a single color or metric from the active theme.
    Example: get_color("bg") -> "#0A0A0C" (in hyperos mode)
    """
    return THEMES[_current_theme].get(key, "#FF00FF")  # magenta = missing key warning


def set_theme(name):
    """
    Switches the active theme. name can be "hyperos", "dark", or "light".
    Apps should re-read colors (via get_color) after calling this.
    """
    global _current_theme

    if name not in THEMES:
        print(f"[DivyOS] Unknown theme '{name}', staying on '{_current_theme}'")
        return

    _current_theme = name


def toggle_theme():
    """Switches between hyperos, dark, and light mode sequentially."""
    global _current_theme
    if _current_theme == "hyperos":
        set_theme("light")
    elif _current_theme == "light":
        set_theme("dark")
    else:
        set_theme("hyperos")


def current_theme_name():
    """Returns the name of the currently active theme."""
    return _current_theme