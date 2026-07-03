from modules.launcher.launcher import Launcher
from modules.files.files import Files


class Router:
    def __init__(self):
        print(">>> Router initialized")

        self.launcher = Launcher()
        self.files = Files()

    def route(self, text: str):
        print(f">>> Router received: {text}")

        result = self.launcher.open(text)

        if result is not None:
            return result, True

        result = self.files.open(text)

        if result is not None:
            return result, True

        return None, False