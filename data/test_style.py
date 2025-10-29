import json
import datetime
import os

# Файл для результатов
RESULTS_FILE = "results.json"


def main():
    """
    Главная функция
    """
    print("=" * 40)
    print("ТЕСТ: Твой стиль танца")
    print("=" * 40)

    # Запускаем тест
    result = run_test()

    # Показываем результат
    show_result(result)

    # Сохраняем результат (статистика скрыта от пользователя)
    save_result(result)


def run_test():
    """
    Запускает тест
    """
    # Вопрос 1: Возраст
    print("\n1. Сколько тебе лет?")
    print("А) 4-5")
    print("Б) 7-9")
    print("В) 10-13")
    print("Г) 14-15")
    print("Д) 16-17")
    print("Е) 18+")

    age = input("Твой выбор: ").upper()

    # Для детей сразу возвращаем результат
    if age == "А":
        return {"style": "Baby 4-5", "age": "4-5", "teacher": "Соня Баловнева"}
    elif age == "Б":
        return {"style": "Kids 7-9", "age": "7-9", "teacher": "Даша Шорникова"}

    # Для остальных задаем вопросы
    answers = []

    # Вопросы 2-5
    questions = [
        "\n2. Какая музыка?\nА) Поп\nБ) R&B\nВ) Хип-хоп\nГ) Женственная\nД) Энергичная\nЕ) Электроника",
        "\n3. Какой образ?\nА) Современный\nБ) Элегантный\nВ) Уличный\nГ) Милый\nД) Женственный\nЕ) Яркий",
        "\n4. Что важно?\nА) Модно\nБ) Грация\nВ) Энергия\nГ) Легкость\nД) Пластика\nЕ) Эмоции",
        "\n5. Уровень?\nА) Начинающий\nБ) Хочу пластику\nВ) Уличные стили\nГ) Легкий стиль\nД) Женственность\nЕ) Готов к нагрузкам"
    ]

    for q in questions:
        print(q)
        while True:
            ans = input("Твой выбор: ").upper()
            if ans in ["А", "Б", "В", "Г", "Д", "Е"]:
                answers.append(ans)
                break
            else:
                print("Выбери А-Е")

    # Определяем стиль
    style = find_style(answers)

    # Проверяем возраст
    final = check_age(style, age)

    return {
        "style": final["style"],
        "age": get_age_text(age),
        "teacher": final["teacher"]
    }


def find_style(answers):
    """
    Находит стиль по ответам
    """
    # Баллы стилей
    scores = {
        "Choreo": 0,
        "High Heels": 0,
        "Hip-hop": 0,
        "Girly hip-hop": 0,
        "Girly Choreo": 0,
        "Jazz Funk": 0
    }

    # Ответ -> стиль
    style_map = {
        "А": "Choreo",
        "Б": "High Heels",
        "В": "Hip-hop",
        "Г": "Girly hip-hop",
        "Д": "Girly Choreo",
        "Е": "Jazz Funk"
    }

    # Считаем баллы
    for ans in answers:
        if ans in style_map:
            scores[style_map[ans]] += 1

    # Лучший стиль
    return max(scores, key=scores.get)


def get_age_text(age_choice):
    """
    Возраст текстом
    """
    ages = {
        "А": "4-5 лет",
        "Б": "7-9 лет",
        "В": "10-13 лет",
        "Г": "14-15 лет",
        "Д": "16-17 лет",
        "Е": "18+ лет"
    }
    return ages.get(age_choice, "Не указано")


def check_age(style, age_choice):
    """
    Проверяет возрастные ограничения
    """
    # Минимальный возраст
    min_age = {
        "Choreo": 14,
        "Hip-hop": 14,
        "Girly hip-hop": 14,
        "Jazz Funk": 12,
        "High Heels": 16,
        "Girly Choreo": 16
    }

    # Возраст числом
    age_num = {"А": 4, "Б": 7, "В": 10, "Г": 14, "Д": 16, "Е": 18}
    age = age_num.get(age_choice, 0)

    # Тренеры
    teachers = {
        "Baby 4-5": "Соня Баловнева",
        "Kids 7-9": "Даша Шорникова",
        "Teens 10-13": "Настя Кюннап, Соня Баловнева",
        "Choreo": "Даша Шорникова",
        "High Heels": "Катя Бударина, Настя Семенова, Ангелина Сумина, Ксения Лунева",
        "Hip-hop": "Катя Четина",
        "Girly hip-hop": "Катя Четина",
        "Girly Choreo": "Катя Бударина, Ксения Лунева",
        "Jazz Funk": "Даша Мигрова"
    }

    # Если возраст подходит
    if style in min_age and age >= min_age[style]:
        return {"style": style, "teacher": teachers.get(style, "Тренер")}

    # Если не подходит - альтернатива
    if age_choice == "В":  # 10-13
        if style == "Jazz Funk" and age >= 12:
            return {"style": "Jazz Funk", "teacher": teachers["Jazz Funk"]}
        else:
            return {"style": "Teens 10-13", "teacher": teachers["Teens 10-13"]}

    elif age_choice == "Г":  # 14-15
        if style in ["High Heels", "Girly Choreo"]:
            print(f"\nСтиль {style} с 16+ лет")
            print("Для тебя: Choreo")
            return {"style": "Choreo", "teacher": teachers["Choreo"]}
        else:
            return {"style": style, "teacher": teachers.get(style, "Тренер")}

    else:  # 16+
        return {"style": style, "teacher": teachers.get(style, "Тренер")}


def show_result(data):
    """
    Показывает результат
    """
    style = data["style"]
    teacher = data["teacher"]

    # Описания
    info = {
        "Baby 4-5": "Идеально для малышей!",
        "Kids 7-9": "Танцы для детей!",
        "Teens 10-13": "Для подростков!",
        "Choreo": "Универсальный стиль!",
        "High Heels": "Чувственные танцы!",
        "Hip-hop": "Энергия улиц!",
        "Girly hip-hop": "Легкий хип-хоп!",
        "Girly Choreo": "Женственная хореография!",
        "Jazz Funk": "Эмоциональный танец!"
    }

    print("\n" + "=" * 40)
    print("ТВОЙ РЕЗУЛЬТАТ")
    print("=" * 40)
    print(f"Стиль: {style}")
    print(f"Описание: {info.get(style, 'Твой стиль!')}")
    print(f"Тренер: {teacher}")
    print("=" * 40)


def save_result(data):
    """
    Сохраняет результат (статистика скрыта)
    """
    data["date"] = datetime.datetime.now().isoformat()

    try:
        # Читаем старые
        if os.path.exists(RESULTS_FILE):
            with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
                all_data = json.load(f)
        else:
            all_data = []

        # Добавляем новые
        all_data.append(data)

        # Сохраняем
        with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)

    except:
        # Ошибка скрыта от пользователя
        pass


# Запуск
if __name__ == "__main__":
    main()
