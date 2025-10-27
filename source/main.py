def dance_test():
    """
    Тест для определения подходящего стиля танца
    """
    print("=" * 50)
    print("ТЕСТ: Какой стиль танца тебе подходит?")
    print("=" * 50)

    # Вопрос 1: Возраст
    print("\n1. Сколько тебе лет?")
    print("А) 4-5 лет")
    print("Б) 7-9 лет")
    print("В) 10-13 лет")
    print("Г) 14-15 лет")
    print("Д) 16-17 лет")
    print("Е) 18+ лет")

    age_ans = input("Выбери вариант (А/Б/В/Г/Д/Е): ").upper().strip()

    # Обработка ответа на вопрос 1
    if age_ans == "А":
        return show_res("Baby 4-5", "Тебе идеально подходит группа Baby 4-5!\nТренер: Соня Баловнева")

    elif age_ans == "Б":
        return show_res("Kids 7-9", "Твой стиль — Kids! Танцы для детей 7-9 лет.\nТренер: Даша Шорникова")

    elif age_ans == "В":
        # Для возраста 10-13 лет
        style = full_test()
        final = check_age(style, 12)
        return show_res(final, get_desc(final))

    elif age_ans == "Г":
        # Для возраста 14-15 лет
        style = full_test()
        final = check_age_14_15(style)
        return show_res(final, get_desc(final))

    elif age_ans == "Д":
        # Для возраста 16-17 лет - доступны все взрослые стили
        style = full_test()
        final = check_age_16plus(style, 16)
        return show_res(final, get_desc(final))

    elif age_ans == "Е":
        # Для возраста 18+ лет - доступны все взрослые стили
        style = full_test()
        final = check_age_16plus(style, 18)
        return show_res(final, get_desc(final))

    else:
        print("Пожалуйста, выбери один из предложенных вариантов (А/Б/В/Г/Д/Е)")
        return dance_test()


def full_test():
    """
    Проводит вопросы 2-5 для определения стиля танца
    """
    ans = []

    # Вопрос 2: Музыка
    print("\n2. Какую музыку ты предпочитаешь?")
    print("А) Современные хиты и поп-музыка")
    print("Б) Sensual R&B и медленные композиции")
    print("В) Хип-хоп и биты")
    print("Г) Популярные треки с женственным настроением")
    print("Д) Энергичные поп-композиции")
    print("Е) Электронную музыку с драйвом")

    while True:
        q = input("Выбери вариант (А/Б/В/Г/Д/Е): ").upper().strip()
        if q in ["А", "Б", "В", "Г", "Д", "Е"]:
            ans.append(q)
            break
        else:
            print("Пожалуйста, выбери один из предложенных вариантов")

    # Вопрос 3: Образ
    print("\n3. Какой образ тебе ближе?")
    print("А) Универсальный и современный")
    print("Б) Элегантный и сексуальный")
    print("В) Уличный и свободный")
    print("Г) Милый и кокетливый")
    print("Д) Женственный и грациозный")
    print("Е) Яркий и экспрессивный")

    while True:
        q = input("Выбери вариант (А/Б/В/Г/Д/Е): ").upper().strip()
        if q in ["А", "Б", "В", "Г", "Д", "Е"]:
            ans.append(q)
            break
        else:
            print("Пожалуйста, выбери один из предложенных вариантов")

    # Вопрос 4: Что важно в танце
    print("\n4. Что для тебя важно в танце?")
    print("А) Универсальность и модные движения")
    print("Б) Грация и работа с образами")
    print("В) Энергия и самовыражение")
    print("Г) Легкость и женственность")
    print("Д) Пластичность и изящество")
    print("Е) Эмоциональность и техника")

    while True:
        q = input("Выбери вариант (А/Б/В/Г/Д/Е): ").upper().strip()
        if q in ["А", "Б", "В", "Г", "Д", "Е"]:
            ans.append(q)
            break
        else:
            print("Пожалуйста, выбери один из предложенных вариантов")

    # Вопрос 5: Уровень подготовки
    print("\n5. Какой у тебя уровень подготовки?")
    print("А) Начинающий, но хочу попробовать всё")
    print("Б) Хочу научиться женственной пластике")
    print("В) Нравится уличная культура")
    print("Г) Ищу легкий и приятный стиль")
    print("Д) Хочу развивать женственность в движении")
    print("Е) Готов(а) к энергичным тренировкам")

    while True:
        q = input("Выбери вариант (А/Б/В/Г/Д/Е): ").upper().strip()
        if q in ["А", "Б", "В", "Г", "Д", "Е"]:
            ans.append(q)
            break
        else:
            print("Пожалуйста, выбери один из предложенных вариантов")

    return find_style(ans)


def find_style(ans):
    """
    Определяет стиль танца на основе ответов
    """
    scores = {
        "Choreo": 0,
        "High Heels": 0,
        "Hip-hop": 0,
        "Girly hip-hop": 0,
        "Girly Choreo": 0,
        "Jazz Funk": 0
    }

    # Сопоставление ответов со стилями
    mapping = {
        "А": "Choreo",
        "Б": "High Heels",
        "В": "Hip-hop",
        "Г": "Girly hip-hop",
        "Д": "Girly Choreo",
        "Е": "Jazz Funk"
    }

    # Подсчитываем баллы для каждого стиля
    for a in ans:
        if a in mapping:
            scores[mapping[a]] += 1

    # Находим стиль с максимальным количеством баллов
    max_s = max(scores.values())
    best = [s for s, sc in scores.items() if sc == max_s]

    return best[0]


def check_age(style, age):
    """
    Проверяет возрастные ограничения для возрастов 10-13 лет
    """
    limits = {
        "Choreo": 14,
        "Hip-hop": 14,
        "Girly hip-hop": 14,
        "Jazz Funk": 12,
        "High Heels": 16,
        "Girly Choreo": 16
    }

    if style in limits and age >= limits[style]:
        return style
    elif style in limits and age < limits[style]:
        req_age = limits[style]

        # Для возраста 10-13 лет предлагаем Teens как альтернативу
        alt = "Teens 10-13"

        print(f"\n  Стиль {style} доступен с {req_age}+ лет")
        print(f"Для твоего возраста идеально подойдет: {alt}")

        return alt

    return style


def check_age_14_15(style):
    """
    Проверяет возрастные ограничения для возрастов 14-15 лет
    """
    limits = {
        "Choreo": 14,
        "Hip-hop": 14,
        "Girly hip-hop": 14,
        "Jazz Funk": 12,
        "High Heels": 16,
        "Girly Choreo": 16
    }

    if style in limits:
        if limits[style] <= 14:  # Стили доступные с 14 лет и младше
            return style
        else:
            # Для High Heels и Girly Choreo (16+) предлагаем альтернативу
            req_age = limits[style]
            alt = "Choreo"  # Предлагаем Choreo как универсальный вариант

            print(f"\n  Стиль {style} доступен с {req_age}+ лет")
            print(f"Для твоего возраста идеально подойдет: {alt}")

            return alt

    return style


def check_age_16plus(style, age):
    """
    Проверяет возрастные ограничения для возрастов 16+ лет
    Teens, Baby, Kids НЕ предлагаются!
    """
    limits = {
        "Choreo": 14,
        "Hip-hop": 14,
        "Girly hip-hop": 14,
        "Jazz Funk": 12,
        "High Heels": 16,
        "Girly Choreo": 16
    }

    if style in limits:
        if age >= limits[style]:
            return style
        else:
            # Если стиль недоступен, предлагаем альтернативу из взрослых стилей
            req_age = limits[style]

            # Доступные взрослые стили для альтернативы
            adult_styles = ["Choreo", "Hip-hop", "Girly hip-hop", "Jazz Funk"]
            if age >= 16:
                adult_styles.extend(["High Heels", "Girly Choreo"])

            # Выбираем первый доступный взрослый стиль как альтернативу
            alt = adult_styles[0]

            print(f"\n Стиль {style} доступен с {req_age}+ лет")
            print(f"Для твоего возраста идеально подойдет: {alt}")

            return alt

    return style


def get_desc(style):
    """
    Возвращает описание результата для каждого стиля
    """
    desc = {
        "Baby 4-5": "Тебе идеально подходит группа Baby 4-5!\nТренер: Соня Баловнева",
        "Kids 7-9": "Твой стиль — Kids! Танцы для детей 7-9 лет.\nТренер: Даша Шорникова",
        "Teens 10-13": "Твой стиль — Teens! Современные танцы для подростков 10-13 лет.\nТренеры: Настя Кюннап, Соня Баловнева",
        "Choreo": "Твой стиль — Choreo! Универсальное направление под современную музыку.\nТренер: Даша Шорникova",
        "High Heels": "Твой стиль — High Heels! Элегантный и чувственный танец на каблуках.\nТренеры: Катя Бударина, Настя Семенова, Ангелина Сумина, Ксения Лунева",
        "Hip-hop": "Твой стиль — Hip-hop! Энергичный уличный танец.\nТренер: Катя Четина",
        "Girly hip-hop": "Твой стиль — Girly Hip-hop! Легкий и женственный хип-хоп.\nТренер: Катя Четина",
        "Girly Choreo": "Твой стиль — Girly Choreo! Женственная и грациозная хореография.\nТренеры: Катя Бударина, Ксения Лунева",
        "Jazz Funk": "Твой стиль — Jazz Funk! Энергичный и эмоциональный танец.\nТренер: Даша Мигрова"
    }

    return desc.get(style, "Стиль не определен")


def show_res(style, desc):
    """
    Показывает финальный результат теста
    """
    print("\n" + "=" * 50)
    print("РЕЗУЛЬТАТ ТЕСТА")
    print("=" * 50)
    print(f"{desc}")
    print("=" * 50)

    return style


def main():
    """
    Основная функция для запуска теста
    """
    try:
        print("Добро пожаловать в тест по определению стиля танца!")
        print("Отвечай на вопросы, выбирая буквы А, Б, В и т.д.")

        res = dance_test()

        print("\nПоздравляем с прохождением теста!")
        print("Желаем успехов в танцах!")

        again = input("\nХочешь пройти тест еще раз? (да/нет): ").lower().strip()
        if again in ['да', 'д', 'yes', 'y']:
            print("\n" + "=" * 50)
            main()
        else:
            print("Спасибо за участие! До встречи на танцполе!")

    except KeyboardInterrupt:
        print("\n\nТест прерван. Возвращайся, когда захочешь узнать свой стиль!")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


# Запуск теста
if __name__ == "__main__":
    main()