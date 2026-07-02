import ollama

from core.database import Database


SYSTEM_PROMPT = """
Ты локальный ИИ-помощник по имени Бро.

Правила:

- Всегда отвечай на русском языке.
- Будь кратким.
- Если пользователь обращается "брат", "бро", "братан" — отвечай дружелюбно.
- Не упоминай, что ты языковая модель.
- Если не знаешь ответ — честно скажи об этом.
"""


class AI:
    def __init__(self, model="qwen3:8b"):
        self.model = model
        self.db = Database()

    def ask(self, message: str) -> str:
        self.db.add("user", message)

        history = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

        for role, text in self.db.last():
            history.append(
                {
                    "role": role,
                    "content": text
                }
            )

        response = ollama.chat(
            model=self.model,
            messages=history
        )

        answer = response["message"]["content"]

        self.db.add("assistant", answer)

        return answer