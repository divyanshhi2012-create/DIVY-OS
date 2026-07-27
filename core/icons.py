# ===========================
# DivyOS - Icon Loader
# ===========================
#
# A shared, reusable icon-loading system so every app
# (desktop, notepad, calculator, settings, etc.) can load
# PNG/ICO icons the same safe way, with emoji fallback and
# no risk of icons disappearing due to garbage collection.

from core.utils import resource_path

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class IconLoader:
    """
    Usage:
        icons = IconLoader()
        photo = icons.load("terminal", size=(32, 32))

        if photo:
            label = tk.Label(root, image=photo)
            label.image = photo   # keep a reference too, just in case
        else:
            label = tk.Label(root, text="💻")  # emoji fallback
    """

    def __init__(self):
        # Cache so the same icon isn't loaded from disk twice,
        # and so every loaded image keeps a permanent reference
        # (prevents icons from vanishing).
        self._cache = {}

    def load(self, name, size=(40, 40)):
        """
        Loads assets/icons/<name>.png or .ico, resized to `size`.
        Returns a Tkinter PhotoImage, or None if unavailable
        (caller should fall back to an emoji).
        """
        if not PIL_AVAILABLE:
            return None

        cache_key = (name, size)
        if cache_key in self._cache:
            return self._cache[cache_key]

        candidates = [
            resource_path("assets", "icons", f"{name}.png"),
            resource_path("assets", "icons", f"{name}.ico"),
        ]

        for path in candidates:
            try:
                img = Image.open(path)
            except (FileNotFoundError, OSError):
                continue

            img = img.convert("RGBA")
            img = img.resize(size, Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            self._cache[cache_key] = photo
            return photo

        return None

    def get_or_emoji(self, name, emoji, size=(40, 40)):
        """
        Convenience method: tries to load the image icon,
        and if it's missing, returns the emoji string instead.
        Returns a tuple: (photo_or_none, emoji_string)
        """
        photo = self.load(name, size)
        return photo, emoji


# A single shared instance apps can import directly:
#   from core.icons import icons
#   photo = icons.load("notepad")
icons = IconLoader()