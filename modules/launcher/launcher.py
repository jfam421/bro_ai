import os
import subprocess
import webbrowser
from pathlib import Path

from modules.launcher.indexer import Indexer


PROGRAMS = {
    "блокнот": "notepad.exe",
    "калькулятор": "calc.exe",
    "проводник": "explorer.exe",
    "paint": "mspaint.exe",
    "диспетчер задач": "taskmgr.exe",
}


class Launcher:
    def __init__(self):
        self.indexer = Indexer()
        self.indexer.scan()

    def open(self, text: str):
        original = text.strip()
        text = original.lower().strip()

        prefixes = (
            "открой ",
            "запусти ",
            "включи ",
        )

        for prefix in prefixes:
            if text.startswith(prefix):
                text = text[len(prefix):].strip()
                break

        # Встроенные программы
        if text in PROGRAMS:
            try:
                subprocess.Popen([PROGRAMS[text]])
                return f"Открываю {text}."
            except Exception as e:
                return f"Ошибка: {e}"

        # Программы из меню Пуск
        program = self.indexer.search(text)

        if program:
            try:
                os.startfile(program)
                return f"Открываю {program.stem}."
            except Exception as e:
                return f"Ошибка: {e}"

        # Сайт
        if original.startswith(("http://", "https://")):
            webbrowser.open(original)
            return "Открываю сайт."

        if original.startswith("www."):
            webbrowser.open("https://" + original)
            return "Открываю сайт."

        # Файл или папка
        path = Path(original)

        if path.exists():
            try:
                os.startfile(path)
                return f"Открываю {path.name}."
            except Exception as e:
                return f"Ошибка: {e}"

        return None