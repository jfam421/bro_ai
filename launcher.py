from core.assistant import Assistant


def main():
    print("=" * 50)
    print("БРО v0.5")
    print("Пиши 'выход' для завершения.")
    print("=" * 50)

    assistant = Assistant()

    while True:
        try:
            user = input("\nТы: ").strip()

            if not user:
                continue

            if user.lower() == "выход":
                print("Бро: До встречи!")
                break


            answer = assistant.process(user)

            print(f"\nБро: {answer}")

        except (EOFError, KeyboardInterrupt):
            print("\nБро: До встречи!")
            break

        except Exception:
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()