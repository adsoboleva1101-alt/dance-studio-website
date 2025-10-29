import json

# Данные о тренерах с добавленными рассказами
coaches_data = [
    {
        "name": "Даша Шорникова",
        "specialization": ["choreo", "Kids 7-9"],
        "vk": "https://vk.com/dariashorrrnikova",
        "instagram": "@shornikova_d",
        "story": "Даша - талантливый хореограф с многолетним опытом работы с детьми. Её занятия всегда наполнены энергией и творчеством. Она умеет находить подход к каждому ребёнку, помогая раскрыть их танцевальный потенциал."
    },
    {
        "name": "Катя Четина",
        "specialization": ["hip-hop", "Girly hip-hop"],
        "vk": "https://vk.com/chetka17?from=search",
        "instagram": "@chetka17",
        "story": "Катя - настоящая звезда хип-хоп сцены. Её стиль - это уникальное сочетание мощной энергии и женственности. На занятиях она создаёт атмосферу, где каждый может почувствовать себя уверенно и свободно."
    },
    {
        "name": "Катя Бударина",
        "specialization": ["High Heels", "Girly choreo"],
        "vk": "https://vk.com/casey7",
        "instagram": "@caseeey7",
        "story": "Катя - эксперт в направлении High Heels. Её уроки - это не просто танцы, а целое искусство движения на каблуках. Она учит не только технике, но и уверенности в себе, грации и женственности."
    },
    {
        "name": "Настя Кюннап",
        "specialization": ["Teens 10-14"],
        "vk": "https://vk.com/anastaaaasik?from=search",
        "instagram": "@anastas.ka_",
        "story": "Настя специализируется на работе с подростками. Она понимает психологию этого возраста и создаёт комфортную среду для творческого развития. Её ученики не только учатся танцевать, но и находят себя."
    },
    {
        "name": "Настя Семенова",
        "specialization": ["High Heels"],
        "vk": "https://vk.com/naastasyaaa",
        "instagram": "к сожалению нету",
        "story": "Настя - страстный преподаватель High Heels с уникальным подходом к обучению. Она верит, что каждая женщина может чувствовать себя королевой на сцене и в жизни. Её занятия - это трансформация и раскрытие внутренней силы."
    },
    {
        "name": "Даша Мигрова",
        "specialization": ["Jazz funk"],
        "vk": "https://vk.com/ddddddddddddddddasha",
        "instagram": "@ddddddddddddasha_",
        "story": "Даша привносит невероятную энергию в свои занятия Jazz funk. Её стиль - это взрывная смесь джаза и фанка. Она вдохновляет учеников экспериментировать и находить свой уникальный стиль в танце."
    },
    {
        "name": "Соня Баловнева",
        "specialization": ["Teens 10-14", "baby 4-5"],
        "vk": "https://vk.com/sooooofiaaaaaaa",
        "instagram": "@_so_nka",
        "story": "Соня - универсальный преподаватель, работающий как с малышами, так и с подростками. Её терпение и любовь к детям делают каждое занятие особенным. Она создаёт волшебную атмосферу, где даже самые маленькие танцоры чувствуют себя звездами."
    },
    {
        "name": "Ангелина Сумина",
        "specialization": ["High Heels"],
        "vk": "https://vk.com/angelinasumina",
        "instagram": "@angelinasumina",
        "story": "Ангелина - элегантный и техничный преподаватель High Heels. Её уроки - это мастер-класс по грации и уверенности. Она помогает каждой ученице раскрыть свою внутреннюю богиню и танцевать с невероятной страстью."
    },
    {
        "name": "Ксения Лунева",
        "specialization": ["High Heels", "Girly choreo"],
        "vk": "https://vk.com/id168724997",
        "instagram": "к сожалению нету",
        "story": "Ксения - разносторонний хореограф, сочетающий в своей работе технику High Heels и женственной хореографии. Её подход основан на индивидуальности каждой ученицы, помогая им найти свой уникальный стиль и выразить себя через танец."
    }
]

# Сохраняем данные в JSON файл
with open('coaches.json', 'w', encoding='utf-8') as file:
    json.dump(coaches_data, file, ensure_ascii=False, indent=2)


# Функция для показа всех тренеров
def show_all_coaches():
    try:
        with open('coaches.json', 'r', encoding='utf-8') as file:
            coaches = json.load(file)

        print(f"\n{'=' * 60}")
        print("ВСЕ ТРЕНЕРЫ ТАНЦЕВАЛЬНОЙ СТУДИИ")
        print(f"{'=' * 60}")

        for coach in coaches:
            print(f"\nТренер: {coach['name']}")
            print(f"Направления: {', '.join(coach['specialization'])}")
            print(f"VK: {coach['vk']}")
            print(f"Instagram: {coach['instagram']}")
            print(f"Рассказ: {coach['story']}")
            print(f"{'-' * 60}")

    except FileNotFoundError:
        print("Файл coaches.json не найден!")


# Функция для поиска тренера по имени
def find_coach_by_name(name):
    try:
        with open('coaches.json', 'r', encoding='utf-8') as file:
            coaches = json.load(file)

        found_coaches = []
        for coach in coaches:
            if name.lower() in coach['name'].lower():
                found_coaches.append(coach)

        return found_coaches
    except FileNotFoundError:
        return []


# Основная программа
if __name__ == "__main__":
    print("Данные успешно сохранены в файл coaches.json")

    # Сначала спрашиваем, хочет ли пользователь найти конкретного тренера
    print("\nХотите найти конкретного тренера? (да/нет)")
    choice = input().lower()

    if choice == 'да':
        name = input("Введите имя тренера: ")
        found_coaches = find_coach_by_name(name)

        if found_coaches:
            print(f"\n{'=' * 60}")
            print(f"НАЙДЕННЫЕ ТРЕНЕРЫ ПО ЗАПРОСУ: '{name}'")
            print(f"{'=' * 60}")

            for coach in found_coaches:
                print(f"\nТренер: {coach['name']}")
                print(f"Направления: {', '.join(coach['specialization'])}")
                print(f"VK: {coach['vk']}")
                print(f"Instagram: {coach['instagram']}")
                print(f"Рассказ: {coach['story']}")
                print(f"{'-' * 60}")
        else:
            print(f"\nТренеры по запросу '{name}' не найдены.")
            print("Показываю всех тренеров:")
            show_all_coaches()

    else:
        # Если пользователь не хочет искать конкретного тренера, показываем всех
        print("\nПоказываю всех тренеров:")
        show_all_coaches()
