from pathlib import Path


START_MENU = [
    Path(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs"),
    Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs",
]


class Indexer:

    def __init__(self):
        self.programs = {}

    def scan(self):
        self.programs.clear()

        for folder in START_MENU:
            if not folder.exists():
                continue

            for file in folder.rglob("*.lnk"):
                name = file.stem.lower().strip()
                self.programs[name] = file

    def search(self, text: str):
        text = text.lower()

        for word in (
            "открой",
            "запусти",
            "запуск",
            "включи",
            "открыть",
            "запустить",
            "please",
        ):
            text = text.replace(word, "")

        text = " ".join(text.split())

        if not text:
            return None

        # 1. Точное совпадение
        if text in self.programs:
            return self.programs[text]

        # 2. Начало названия
        for name, path in self.programs.items():
            if name.startswith(text):
                return path

        # 3. Вхождение
        for name, path in self.programs.items():
            if text in name:
                return path

        # 4. Все слова присутствуют
        words = text.split()

        for name, path in self.programs.items():
            if all(word in name for word in words):
                return path

        return None