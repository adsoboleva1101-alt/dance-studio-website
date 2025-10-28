import webbrowser


def get_form_url(style):
    """
    Возвращает единую URL форму Google Forms для всех стилей
    """
    # Единая форма для всех направлений
    return "https://forms.gle/8C7SuB2hjFiWF79f7"


def offer_registration(style):
    """
    Предлагает записаться на пробное занятие
    """
    print("\nХочешь попробовать этот стиль на практике?")
    print("Запишись на пробное занятие!")

    form_url = get_form_url(style)

    print(f"\nТвой стиль: {style}")
    print(f"Ссылка для записи: {form_url}")

    while True:
        choice = input("\nВыбери действие:\n"
                       "1 - Открыть форму записи\n"
                       "2 - Продолжить\n"
                       "Твой выбор (1/2): ").strip()

        if choice == "1":
            webbrowser.open(form_url)
            print("Форма открывается в браузере...")
            print("Не забудь указать в форме, что выбрал стиль: " + style)
            break
        elif choice == "2":
            print("Можешь записаться позже по ссылке выше")
            print("Не забудь указать в форме стиль: " + style)
            break
        else:
            print("Пожалуйста, выбери 1 или 2")


def show_res(style, desc):
    """
    Показывает финальный результат теста с возможностью записи
    """
    print("\n" + "=" * 50)
    print("РЕЗУЛЬТАТ ТЕСТА")
    print("=" * 50)
    print(f"{desc}")
    print("=" * 50)

    # Предлагаем записаться на занятие
    offer_registration(style)

    return style