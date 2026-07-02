import os
import subprocess
import webbrowser
from pathlib import Path


PROGRAMS = {
    "блокнот": "notepad",
    "калькулятор": "calc",
    "проводник": "explorer",
    "paint": "mspaint",
    "диспетчер задач": "taskmgr",
    "командная строка": "cmd",
    "powershell": "powershell",
    "vs code": "code",
    "vscode": "code",
}


class Launcher:

    def open(self, text: str):
        text = text.lower().strip()

        # ---------- программы ----------
        for name, command in PROGRAMS.items():
            if name in text:
                subprocess.Popen(command)
                return f"Открываю {name}."

        # ---------- сайты ----------
        if text.startswith("https://") or text.startswith("http://"):
            webbrowser.open(text)
            return "Открываю сайт."

        if text.startswith("www."):
            webbrowser.open(f"https://{text}")
            return "Открываю сайт."

        # ---------- файл или папка ----------
        path = Path(text)

        if path.exists():
            os.startfile(path)
            return f"Открываю {path.name}."

        return None