from pathlib import Path
import json

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

    def ask(self, message: str) -> dict:
        self.db.add_message("user", message)

        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            }
        ]

        memories = self.db.get_memory()

        if memories:
            messages.append(
                {
                    "role": "system",
                    "content":
                        "Долговременная память:\n"
                        + "\n".join(
                            f"- {fact}"
                            for fact in memories
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

        raw = response["message"]["content"]

        try:
            data = json.loads(raw)

            answer = data.get("answer", "")
            memory = data.get("memory", [])

        except Exception:
            answer = raw
            memory = []

        self.db.add_message(
            "assistant",
            answer
        )

        return {
            "answer": answer,
            "memory": memory
        }