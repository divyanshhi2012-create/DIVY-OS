# core/ai.py

class DivyAI:

    def __init__(self, desktop):
        self.desktop = desktop

    def ask_ai(self, prompt):
        """
        Abhi basic response.
        Baad me yahin Gemini API connect karenge.
        """
        return f"You said: {prompt}"

    def execute(self, command):
        """
        Future me OS commands yahan handle karenge.
        """
        command = command.lower().strip()

        if command == "settings":
            if hasattr(self.desktop, "settings"):
                self.desktop.settings.open()

        elif command == "calculator":
            if hasattr(self.desktop, "calculator"):
                self.desktop.calculator.open()

        elif command == "explorer":
            if hasattr(self.desktop, "explorer"):
                self.desktop.explorer.open()

        else:
            return self.ask_ai(command)