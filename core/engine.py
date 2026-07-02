from core.ai import AI
from core.router import Router


class Engine:
    def __init__(self):
        self.ai = AI()
        self.router = Router()

    def process(self, text):
        result, handled = self.router.route(text)

        if handled:
            return result

        return self.ai.ask(text)