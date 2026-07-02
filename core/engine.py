from core.ai import AI
from core.router import Router
from core.logger import logger


class Engine:
    def __init__(self):
        self.ai = AI()
        self.router = Router()

    def process(self, text: str) -> str:
        logger.info(f"USER: {text}")

        result, handled = self.router.route(text)

        if handled:
            logger.info(f"BRO: {result}")
            return result

        answer = self.ai.ask(text)

        logger.info(f"BRO: {answer}")

        return answer