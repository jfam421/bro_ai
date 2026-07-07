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

        lower = text.lower().strip()

        # -------------------------------------------------
        # Быстрый запуск программ
        # -------------------------------------------------

        if lower.startswith(("открой ", "запусти ", "запустить ")):
            command = {
                "tool": "programs",
                "action": "open",
                "value": text,
            }

            result = self.programs.handle(command)

            if result is not None:
                return result, True

        # -------------------------------------------------
        # Быстрый поиск файлов
        # -------------------------------------------------

        if (
            "файл" in lower
            or "папк" in lower
            or "документ" in lower
            or "картинк" in lower
            or "изображен" in lower
            or "рабочий стол" in lower
            or "загрузки" in lower
            or "downloads" in lower
            or "documents" in lower
        ):
            command = {
                "tool": "files",
                "action": "open",
                "value": text,
            }

            result = self.files.handle(command)

            if result is not None:
                return result, True

        # -------------------------------------------------
        # Быстрый поиск в интернете
        # -------------------------------------------------

        if lower.startswith(("найди ", "поищи ", "загугли ")):
            command = {
                "tool": "browser",
                "action": "search",
                "value": text,
            }

            result = self.browser.handle(command)

            if result is not None:
                return result, True

        # -------------------------------------------------
        # AI
        # -------------------------------------------------

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