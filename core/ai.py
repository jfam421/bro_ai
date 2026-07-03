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
        ).read_text(encoding="utf-8")

        self.memory_prompt = Path(
            "prompts/memory.txt"
        ).read_text(encoding="utf-8")

        self.command_prompt = Path(
            "prompts/command.txt"
        ).read_text(encoding="utf-8")

    # -------------------------------------------------
    # Универсальный запрос
    # -------------------------------------------------

    def raw(self, prompt: str) -> str:

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    # -------------------------------------------------
    # Анализ команды
    # -------------------------------------------------

    def analyze_command(self, message: str):

        prompt = self.command_prompt.replace(
            "{message}",
            message
        )

        raw = self.raw(prompt)

        try:
            return json.loads(raw)

        except Exception:
            return {
                "tool": "chat",
                "action": "answer",
                "value": message
            }

    # -------------------------------------------------
    # Анализ памяти
    # -------------------------------------------------

    def analyze_memory(self, message: str):

        prompt = self.memory_prompt.replace(
            "{message}",
            message
        )

        raw = self.raw(prompt)

        try:
            data = json.loads(raw)
            return data.get("memory", [])

        except Exception:
            return []

    # -------------------------------------------------
    # Диалог
    # -------------------------------------------------

    def ask(self, message: str):

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
            answer = data.get("answer", raw)

        except Exception:
            answer = raw

        self.db.add_message(
            "assistant",
            answer
        )

        return {
            "answer": answer
        }