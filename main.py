from core.boot import BootScreen
from core.desktop import Desktop


def start_desktop():
    desktop = Desktop()
    desktop.run()


if __name__ == "__main__":
    boot = BootScreen(start_desktop)
    boot.run()