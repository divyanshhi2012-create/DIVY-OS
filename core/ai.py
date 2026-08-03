# ==============================================================================
# DivyOS - DivyAI Intelligent Command & Q&A Engine
# ==============================================================================

import urllib.parse
import webbrowser


class DivyAI:

    def __init__(self, desktop):
        self.desktop = desktop

    def execute(self, command):
        """Processes user voice/text query, executes desktop tasks or searches online."""
        if not command:
            return "Please enter or speak a valid command."

        raw_cmd = command.strip()
        cmd = raw_cmd.lower()

        # ---------------- 1. Desktop System Commands ----------------

        if cmd in ("show desktop", "desktop"):
            if hasattr(self.desktop, "show_desktop"):
                self.desktop.show_desktop()
                return "Showing desktop."

        elif cmd == "lock":
            if hasattr(self.desktop, "lock"):
                self.desktop.lock()
                return "Locking DivyOS."

        elif cmd == "shutdown":
            if hasattr(self.desktop, "shutdown"):
                self.desktop.shutdown()
                return "Shutting down system."

        elif cmd == "restart":
            if hasattr(self.desktop, "restart"):
                self.desktop.restart()
                return "Restarting system."

        elif cmd in ("start", "start menu", "menu"):
            if hasattr(self.desktop, "start_menu"):
                self.desktop.start_menu.toggle()
                return "Opening start menu."

        # ---------------- 2. System Application Launchers ----------------

        elif cmd in ("browser", "open browser"):
            if hasattr(self.desktop, "open_browser"):
                self.desktop.open_browser()
                return "Opening Browser."

        elif cmd in ("settings", "open settings"):
            if hasattr(self.desktop, "open_settings"):
                self.desktop.open_settings()
                return "Opening Settings."

        elif cmd in ("calculator", "open calculator"):
            if hasattr(self.desktop, "open_calculator"):
                self.desktop.open_calculator()
                return "Opening Calculator."

        elif cmd in ("notepad", "open notepad"):
            if hasattr(self.desktop, "open_notepad"):
                self.desktop.open_notepad()
                return "Opening Notepad."

        elif cmd in ("explorer", "open explorer", "files", "computer"):
            if hasattr(self.desktop, "open_explorer"):
                self.desktop.open_explorer()
                return "Opening File Explorer."

        elif cmd in ("terminal", "open terminal"):
            if hasattr(self.desktop, "open_terminal"):
                self.desktop.open_terminal()
                return "Opening Terminal."

        elif cmd in ("appstore", "store", "open store"):
            if hasattr(self.desktop, "open_appstore"):
                self.desktop.open_appstore()
                return "Opening Divy Store."

        # ---------------- 3. Explicit Web Search ----------------

        elif cmd.startswith("search ") or cmd.startswith("google "):
            query = raw_cmd.split(" ", 1)[1] if " " in raw_cmd else raw_cmd
            return self._perform_web_search(query)

        # ---------------- 4. Q&A & Fallback Web AI Search ----------------

        else:
            if "hello" in cmd or "hi" in cmd:
                return "Hello! How can I assist you with DivyOS today?"

            elif "who are you" in cmd or "your name" in cmd:
                return "I am DivyAI, your built-in HyperOS Desktop Assistant."

            return self._perform_web_search(raw_cmd)

    def _perform_web_search(self, query):
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://www.google.com/search?q={encoded_query}"
        webbrowser.open(search_url)
        return f"Searching Google for: '{query}'"