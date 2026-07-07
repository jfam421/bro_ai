from pathlib import Path
import subprocess
import json

from rapidfuzz import process, fuzz


START_MENU = [
    Path(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs"),
    Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs",
]


class Indexer:

    def __init__(self):
        self.programs = {}

    def scan(self):
        self.programs.clear()

        # -------------------------------------------------
        # Обычные ярлыки
        # -------------------------------------------------

        for folder in START_MENU:
            if not folder.exists():
                continue

            try:
                for file in folder.rglob("*.lnk"):
                    name = file.stem.lower().strip()
                    self.programs[name] = file
            except Exception:
                pass

        # -------------------------------------------------
        # Microsoft Store Apps
        # -------------------------------------------------

        try:
            result = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-Command",
                    "[Console]::OutputEncoding=[System.Text.Encoding]::UTF8; Get-StartApps | ConvertTo-Json -Depth 2"
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="ignore",
            )

            if result.returncode == 0 and result.stdout.strip():

                apps = json.loads(result.stdout)

                if isinstance(apps, dict):
                    apps = [apps]

                for app in apps:

                    name = app.get("Name", "").lower().strip()
                    appid = app.get("AppID", "").strip()

                    if name and appid:
                        self.programs[name] = (
                            "shell:AppsFolder\\" + appid
                        )

        except Exception:
            pass

        print(f"Indexed programs: {len(self.programs)}")

    def search(self, text: str):
        text = text.lower()

        for word in (
            "открой",
            "открыть",
            "запусти",
            "запустить",
            "запуск",
            "включи",
            "please",
        ):
            text = text.replace(word, "")

        text = " ".join(text.split())

        if not text:
            return None

        # 1. Полное совпадение
        if text in self.programs:
            return self.programs[text]

        # 2. Совпадение по словам
        query_words = text.split()

        for name, path in self.programs.items():
            name_words = (
                name.replace("-", " ")
                .replace("_", " ")
                .split()
            )

            if all(word in name_words for word in query_words):
                return path

        # 3. Вхождение
        for name, path in self.programs.items():
            if text in name:
                return path

        # 4. Fuzzy Search
        names = list(self.programs.keys())

        result = process.extractOne(
            text,
            names,
            scorer=fuzz.WRatio,
            score_cutoff=85,
        )

        if result:
            return self.programs[result[0]]

        return None