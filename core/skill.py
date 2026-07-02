class Skill:
    def __init__(self, name, handler):
        self.name = name
        self.handler = handler

    def run(self, text):
        return self.handler(text)