import subprocess


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
        text = text.lower()

        for name, command in PROGRAMS.items():
            if name in text:
                subprocess.Popen(command)
                return f"Открываю {name}."

        return None