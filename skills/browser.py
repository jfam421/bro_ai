import webbrowser


WEBSITES = {
    "youtube": "https://youtube.com",
    "ютуб": "https://youtube.com",
    "google": "https://google.com",
    "гугл": "https://google.com",
    "gmail": "https://mail.google.com",
    "chatgpt": "https://chatgpt.com",
}


def handle_browser(text: str):
    if not text.startswith("открой"):
        return None

    for name, url in WEBSITES.items():
        if name in text:
            webbrowser.open(url)
            return f"Открываю {name}."

    return None