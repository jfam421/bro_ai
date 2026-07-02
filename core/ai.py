from pathlib import Path

import ollama

from core.database import Database


class AI:
    def __init__(self, model="qwen3:8b"):
        self.model = model
        self.db = Database()

        self.system_prompt = Path(
            "prompts/system.txt"
        ).read_text(
            encoding="utf-8"
        )

    def ask(self, message: str) -> str:
        self.db.add_message("user", message)

        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            }
        ]

        facts = self.db.get_all_facts()

        if facts:
            messages.append(
                {
                    "role": "system",
                    "content": "Факты о пользователе:\n"
                    + "\n".join(
                        f"{k}: {v}" for k, v in facts.items()
                    )
                }
            )

        for role, text in self.db.get_history():
            messages.append(
                {
                    "role": role,
                    "content": text
                }
            )

        response = ollama.chat(
            model=self.model,
            messages=messages
        )

        answer = response["message"]["content"]

        self.db.add_message(
            "assistant",
            answer
        )

        return answer