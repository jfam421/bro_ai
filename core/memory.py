import re

from core.database import Database


class Memory:
    def __init__(self):
        self.db = Database()

    def process(self, text: str) -> bool:
        text = text.strip()

        patterns = [
            (r"меня зовут (.+)", "name"),
            (r"мне (\d+) лет", "age"),
            (r"мой город (.+)", "city"),
            (r"я живу в (.+)", "city"),
            (r"я учусь в (.+)", "university"),
        ]

        lower = text.lower()

        for pattern, key in patterns:
            match = re.search(pattern, lower)

            if match:
                value = match.group(1).strip().title()
                self.db.set_fact(key, value)
                return True

        return False

    def answer(self, text: str):
        text = text.lower()

        if "как меня зовут" in text:
            name = self.db.get_fact("name")
            if name:
                return f"Тебя зовут {name}."

        if "сколько мне лет" in text:
            age = self.db.get_fact("age")
            if age:
                return f"Тебе {age} лет."

        if "в каком городе я живу" in text:
            city = self.db.get_fact("city")
            if city:
                return f"Ты живёшь в городе {city}."

        if "где я учусь" in text:
            university = self.db.get_fact("university")
            if university:
                return f"Ты учишься в {university}."

        return None