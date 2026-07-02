from core.assistant import Assistant


def main():
    print("=" * 50)
    print("БРО v0.3")
    print("Пиши 'выход' для завершения.")
    print("=" * 50)

    assistant = Assistant()

    while True:
        try:
            user = input("\nТы: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nБро: До встречи!")
            break

        if not user:
            continue

        if user.lower() == "выход":
            print("Бро: До встречи!")
            break

        try:
            answer = assistant.process(user)
            print(f"\nБро: {answer}")

        except Exception as e:
            print(f"\nОшибка: {e}")


if __name__ == "__main__":
    main()