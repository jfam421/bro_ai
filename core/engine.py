from core.ai import AI
from core.logger import logger
from core.memory import Memory
from core.router import Router


class Engine:

    def __init__(self):
        self.ai = AI()

        self.router = Router(self.ai)

        self.memory = Memory()

    def process(self, text: str) -> str:
        logger.info(f"USER: {text}")

        result, handled = self.router.route(text)

        if handled:
            logger.info(f"ASSISTANT: {result}")
            return result

        response = self.ai.ask(text)

        answer = response["answer"]

        for fact in response["memory"]:
            self.memory.add(fact)

        logger.info(f"ASSISTANT: {answer}")

        return answer