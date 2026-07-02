from modules.launcher.launcher import Launcher


class Router:
    def __init__(self):
        self.launcher = Launcher()

    def route(self, text: str):
        result = self.launcher.open(text)

        if result is not None:
            return result, True

        return None, False