from core.engine import Engine


class Assistant:
    def __init__(self):
        self.engine = Engine()

    def process(self, message: str) -> str:
        return self.engine.process(message)