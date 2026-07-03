import webbrowser
from urllib.parse import quote_plus


class Browser:

    def handle(self, command: dict):

        if command.get("tool") != "browser":
            return None

        action = command.get("action")
        value = command.get("value", "").strip()

        if not value:
            return None

        # Поиск
        if action == "search":

            url = (
                "https://www.google.com/search?q="
                + quote_plus(value)
            )

            webbrowser.open(url)

            return f'Ищу "{value}".'

        # Открытие ссылки
        if action != "open":
            return None

        if value.startswith(("http://", "https://")):
            webbrowser.open(value)
            return "Открываю сайт."

        if value.startswith("www."):
            webbrowser.open("https://" + value)
            return "Открываю сайт."

        if "." in value and " " not in value:
            webbrowser.open("https://" + value)
            return "Открываю сайт."

        # Не угадываем за пользователя.
        url = (
            "https://www.google.com/search?q="
            + quote_plus(value)
        )

        webbrowser.open(url)

        return f'Ищу "{value}".'