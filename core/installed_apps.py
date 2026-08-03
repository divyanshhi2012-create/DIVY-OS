# ===========================
# DivyOS - Installed Windows Apps
# ===========================
#
# Scans the real Windows Start Menu shortcut folders and builds a
# list of every app actually installed on this PC. Lets DivyOS
# launch them for real using os.startfile().

import os
import sys
import glob


class InstalledApps:

    # These are the two real folders Windows uses for Start Menu
    # shortcuts - one for all users, one for just the current user.
    SHORTCUT_DIRS = [
        os.path.expandvars(r"%ProgramData%\Microsoft\Windows\Start Menu\Programs"),
        os.path.expandvars(r"%AppData%\Microsoft\Windows\Start Menu\Programs"),
    ]

    def __init__(self):
        self._cache = None

    def scan(self, force_refresh=False):
        """
        Returns a list of dicts: [{"name": "Spotify", "path": "C:/.../Spotify.lnk"}, ...]
        Cached after the first scan unless force_refresh=True.
        """
        if self._cache is not None and not force_refresh:
            return self._cache

        if sys.platform != "win32":
            self._cache = []
            return self._cache

        apps = {}

        for base_dir in self.SHORTCUT_DIRS:
            if not os.path.isdir(base_dir):
                continue

            pattern = os.path.join(base_dir, "**", "*.lnk")
            for shortcut_path in glob.glob(pattern, recursive=True):
                name = os.path.splitext(os.path.basename(shortcut_path))[0]

                # Skip Windows' own uninstaller/helper shortcuts clutter
                if name.lower() in ("uninstall", "readme", "help"):
                    continue

                apps[name.lower()] = {
                    "name": name,
                    "path": shortcut_path,
                }

        self._cache = sorted(apps.values(), key=lambda a: a["name"].lower())
        return self._cache

    def launch(self, path):
        """Launches an app using its real Windows shortcut path."""
        try:
            os.startfile(path)
            return True
        except Exception as e:
            print("App Launch Error:", path, e)
            return False

    def search(self, query):
        """Filters the scanned app list by name."""
        query = query.lower().strip()
        return [a for a in self.scan() if query in a["name"].lower()]