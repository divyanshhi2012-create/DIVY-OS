# ===========================
# DivyOS Configuration
# ===========================

APP_NAME = "DivyOS"
VERSION = "v1.0"

# Window Size
WIDTH = 1280
HEIGHT = 720

# ===========================
# Colors (HyperOS-inspired Theme)
# ===========================
BG_COLOR = "#141414"          # deep charcoal desktop background
TASKBAR_COLOR = "#1C1C1E"     # floating rounded taskbar
START_MENU_COLOR = "#1F1F21"  # rounded control-center panel
TEXT_COLOR = "#F5F5F5"
BUTTON_COLOR = "#2A2A2C"
HOVER_COLOR = "#37373A"

# HyperOS signature accent (warm orange) + supporting tones
ACCENT_COLOR = "#FF6B35"      # Xiaomi/HyperOS orange accent
ACCENT_SOFT = "#FF6B3533"     # translucent accent, for soft highlights
BORDER_COLOR = "#2E2E30"
GLASS_TINT = "#1C1C1E"

# Window transparency level (1.0 = fully solid, lower = more see-through)
WINDOW_OPACITY = 0.96

# =========================
# HyperOS Shape Language
# =========================
# HyperOS is defined by big, soft, consistent rounded corners.
# These radius values are reused across icons, buttons, and panels
# so the whole OS feels visually unified.
RADIUS_SMALL = 14     # small buttons, chips
RADIUS_MEDIUM = 20    # app icons, taskbar buttons
RADIUS_LARGE = 28     # panels: start menu, app windows, taskbar pill

# Fonts
DEFAULT_FONT = ("Segoe UI", 10)
TITLE_FONT = ("Segoe UI", 18, "bold")

# Boot Settings
BOOT_TIME = 3000  # milliseconds

# Desktop
ICON_WIDTH = 90
ICON_HEIGHT = 80

# Taskbar
TASKBAR_HEIGHT = 56

# Start Menu
START_MENU_WIDTH = 340
START_MENU_HEIGHT = 460

# Wallpaper
WALLPAPER = None  # Example: "assets/wallpaper.png"

# Sounds
BOOT_SOUND = None  # Example: "assets/sounds/boot.wav"