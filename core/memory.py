from core.database import Database


class Memory:
    def __init__(self):
        self.db = Database()

    # Пока оставляем совместимость
    def process(self, text: str) -> bool:
        return False

    def add(self, fact: str):
        self.db.add_memory(fact)

    def get_all(self):
        return self.db.get_memory()

    def clear(self):
        self.db.clear_memory()