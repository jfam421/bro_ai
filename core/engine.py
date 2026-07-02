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

        # Запоминаем новые факты
        if self.memory.process(text):
            answer = "Запомнил."
            logger.info(f"BRO: {answer}")
            return answer

        # Отвечаем из памяти
        answer = self.memory.answer(text)
        if answer:
            logger.info(f"BRO: {answer}")
            return answer

        # Проверяем команды
        result, handled = self.router.route(text)
        if handled:
            logger.info(f"BRO: {result}")
            return result

        # Передаём в ИИ
        answer = self.ai.ask(text)

        logger.info(f"BRO: {answer}")

        return answer