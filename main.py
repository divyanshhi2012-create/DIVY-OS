# ==============================================================================
# DivyOS - Main Launcher Engine
# ==============================================================================

from core.boot import BootScreen
from core.desktop import Desktop


def start_desktop():
    desktop = Desktop()
    desktop.run()


if __name__ == "__main__":
    boot = BootScreen(start_desktop)
    boot.run()


# ==============================================================================
# Vercel Deployment Entrypoint Handler (Fixes Vercel Build Error)
# ==============================================================================
def app(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/plain")])
    return [b"DivyOS Desktop Engine Source Repository"]