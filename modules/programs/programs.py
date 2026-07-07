import os

from modules.programs.indexer import Indexer


class Launcher:

    def __init__(self):
        self.indexer = Indexer()
        self.indexer.scan()

    def handle(self, command: dict):

        if command.get("tool") != "programs":
            return None

        if command.get("action") != "open":
            return None

        value = command.get("value", "").strip()

        if not value:
            return None

        program = self.indexer.search(value)

        if program is None:
            return None

        try:
            os.startfile(program)

            if isinstance(program, str):
                name = value
            else:
                name = program.stem

            return f"Открываю {name}."

        except Exception as e:
            return f"Ошибка: {e}"