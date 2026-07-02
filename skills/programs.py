import subprocess


PROGRAMS = {
    "блокнот": "notepad",
    "калькулятор": "calc",
    "проводник": "explorer",
    "paint": "mspaint",
    "паинт": "mspaint",
    "терминал": "cmd",
    "командная строка": "cmd",
}


def handle_programs(text: str):
    if not text.startswith("открой") and not text.startswith("запусти"):
        return None

    for name, command in PROGRAMS.items():
        if name in text:
            subprocess.Popen(command)
            return f"Открываю {name}."

    return None