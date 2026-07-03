import os

from modules.files.indexer import FileIndexer


class Files:

    def __init__(self):
        self.indexer = FileIndexer()
        self.indexer.scan()

    def open(self, text: str):
        path = self.indexer.search(text)

        if path is None:
            return None

        try:
            os.startfile(path)
            return f"Открываю {path.name}."
        except Exception as e:
            return f"Ошибка: {e}"