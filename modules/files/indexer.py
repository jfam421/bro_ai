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
        self.folders = []

    def scan(self):
        self.files.clear()
        self.folders.clear()

        for folder in SEARCH_FOLDERS:
            if not folder.exists():
                continue

            try:
                for item in folder.rglob("*"):
                    if item.is_file():
                        self.files.append(item)
                    elif item.is_dir():
                        self.folders.append(item)
            except Exception:
                pass

        print(f"Indexed files: {len(self.files)}")
        print(f"Indexed folders: {len(self.folders)}")

    def _find(self, text: str, items):
        stem = Path(text).stem.lower()
        filename = Path(text).name.lower()

        # Полное имя
        for item in items:
            if item.name.lower() == filename:
                return item

        # Имя без расширения
        for item in items:
            if item.stem.lower() == stem:
                return item

        # Начало имени
        for item in items:
            if item.stem.lower().startswith(stem):
                return item

        # Fuzzy
        if len(stem) >= 4:
            names = [item.stem.lower() for item in items]

            result = process.extractOne(
                stem,
                names,
                scorer=fuzz.WRatio,
                score_cutoff=85,
            )

            if result:
                for item in items:
                    if item.stem.lower() == result[0]:
                        return item

        return None

    def search(self, text: str):
        text = text.lower()

        open_folder = "папку" in text

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

        if open_folder:
            return self._find(text, self.folders)

        result = self._find(text, self.files)

        if result:
            return result

        return self._find(text, self.folders)