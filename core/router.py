from modules.programs.programs import Launcher
from modules.files.files import Files
from modules.browser.browser import Browser


class Router:

    def __init__(self, ai):
        print(">>> Router initialized")

        self.ai = ai

        self.programs = Launcher()
        self.files = Files()
        self.browser = Browser()

    def route(self, text: str):
        print(f">>> Router received: {text}")

        command = self.ai.analyze_command(text)

        tool = command.get("tool", "chat")

        if tool == "chat":
            return None, False

        if tool == "programs":
            result = self.programs.handle(command)

        elif tool == "files":
            result = self.files.handle(command)

        elif tool == "browser":
            result = self.browser.handle(command)

        else:
            return None, False

        if result is not None:
            return result, True

        return None, False