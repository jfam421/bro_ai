import ollama


class AI:
    def __init__(self, model="qwen3:8b"):
        self.model = model

    def ask(self, message: str) -> str:
        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Ты локальный помощник пользователя по имени Бро. "
                        "Отвечай на русском языке. "
                        "Будь кратким, дружелюбным и полезным."
                    )
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        return response["message"]["content"]