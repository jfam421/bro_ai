from pathlib import Path
from ctypes import windll, create_unicode_buffer

from rapidfuzz import process, fuzz


def get_known_folder(csidl: int):
    buf = create_unicode_buffer(260)
    windll.shell32.SHGetFolderPathW(None, csidl, None, 0, buf)
    return Path(buf.value)


# Стандартные папки Windows
DESKTOP = get_known_folder(0x0000)
DOCUMENTS = get_known_folder(0x0005)
PICTURES = get_known_folder(0x0027)
VIDEOS = get_known_folder(0x000E)

DOWNLOADS = Path.home() / "Downloads"
if not DOWNLOADS.exists():
    DOWNLOADS = Path.home() / "OneDrive" / "Downloads"


SEARCH_FOLDERS = [
    DESKTOP,
    DOCUMENTS,
    DOWNLOADS,
    PICTURES,
    VIDEOS,
]


class FileIndexer:

    def __init__(self):
        self.files = []

    def scan(self):
        self.files.clear()

        for folder in SEARCH_FOLDERS:
            if not folder.exists():
                continue

            try:
                for file in folder.rglob("*"):
                    if file.is_file():
                        self.files.append(file)
            except Exception:
                pass

        print(f"Indexed files: {len(self.files)}")

    def search(self, text: str):
        text = text.lower()

        for word in (
            "открой",
            "открыть",
            "файл",
            "документ",
            "картинку",
            "изображение",
            "фотографию",
            "папку",
        ):
            text = text.replace(word, "")

        text = text.strip()

        if not text:
            return None

        stem = Path(text).stem.lower()
        filename = Path(text).name.lower()

        # Полное совпадение имени файла
        for file in self.files:
            if file.name.lower() == filename:
                return file

        # Полное совпадение имени без расширения
        for file in self.files:
            if file.stem.lower() == stem:
                return file

        # Начало имени
        for file in self.files:
            if file.stem.lower().startswith(stem):
                return file

        # Fuzzy только для длинных запросов
        if len(stem) >= 4:
            result = process.extractOne(
                stem,
                [f.stem.lower() for f in self.files],
                scorer=fuzz.WRatio,
                score_cutoff=85,
            )

            if result:
                for file in self.files:
                    if file.stem.lower() == result[0]:
                        return file

        return None