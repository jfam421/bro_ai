from skills.registry import SKILLS


class Router:
    def route(self, text):
        for skill in SKILLS:
            result = skill.run(text)

            if result is not None:
                return result, True

        return text, False