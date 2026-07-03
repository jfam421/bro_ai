from core.ai import AI
from core.logger import logger
from core.memory import Memory
from core.router import Router


class Engine:
    def __init__(self):
        self.ai = AI()
        self.router = Router()
        self.memory = Memory()

    def process(self, text: str) -> str:
        logger.info(f"USER: {text}")

        result, handled = self.router.route(text)

        if handled:
            return result

        response = self.ai.ask(text)

        answer = response["answer"]
        facts = response["memory"]

        for fact in facts:
            self.memory.add(fact)

        logger.info(f"ASSISTANT: {answer}")

        return answer