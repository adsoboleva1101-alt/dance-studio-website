import json

data = {
    "high_heels": {
        "Ангелина Сумина": {
            "type": "открытая группа",
            "schedule": {}
        },
        "Ксюша Лунева": {
            "type": "открытая группа",
            "schedule": {
                "вторник, четверг": "21:00 - 22:00",
                "понедельник, среда": "20:30 - 21:30"
            }
        },
        "Катя Бударина": {
            "type": "с нуля",
            "schedule": {}
        },
        "Настя Федоренко": {
            "type": "открытая группа",
            "schedule": {
                "вторник, четверг": "10:00 - 11:00",
                "вторник, четверг": "19:30 - 20:30",
                "понедельник, среда": "20:00 - 21:00"
            }
        }
    },
    "teams": {
        "Paradox": {
            "trainer": "Даша Шорникова",
            "schedule": {
                "вторник, четверг": "20:30 - 21:30"
            }
        },
        "HDK": {
            "trainer": "Катя Четина",
            "schedule": {
                "вторник, четверг": "18:30 - 19:30"
            }
        },
        "4you": {
            "trainer": "Катя Бударина",
            "schedule": {
                "понедельник, среда": "21:00 - 22:00"
            }
        }
    }
}

with open('schedule.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)


def find_schedule(query):
    query = query.lower().strip()
    results = []

    # Поиск в High Heels
    for trainer, info in data["high_heels"].items():
        if query in trainer.lower() or query in info["type"].lower():
            results.append({
                "category": "HIGH HEELS",
                "name": trainer,
                "type": info["type"],
                "schedule": info["schedule"]
            })

    # Поиск в Teams
    for team, info in data["teams"].items():
        if query in team.lower() or query in info["trainer"].lower():
            results.append({
                "category": "TEAM",
                "name": team,
                "trainer": info["trainer"],
                "schedule": info["schedule"]
            })

    return results


def show_all():
    print(f"\n{'=' * 60}")
    print("ПОЛНОЕ РАСПИСАНИЕ")
    print(f"{'=' * 60}")

    print(f"\nHIGH HEELS:")
    for trainer, info in data["high_heels"].items():
        print(f"\n  {trainer} ({info['type']})")
        if info["schedule"]:
            for day, time in info["schedule"].items():
                print(f"    {day}: {time}")
        else:
            print(f"    расписание не указано")

    print(f"\nTEAMS:")
    for team, info in data["teams"].items():
        print(f"\n  {team} - {info['trainer']}")
        for day, time in info["schedule"].items():
            print(f"    {day}: {time}")


def show_by_trainer(trainer_name):
    trainer_name = trainer_name.lower().strip()
    results = []

    for trainer, info in data["high_heels"].items():
        if trainer_name in trainer.lower():
            results.append({
                "category": "HIGH HEELS",
                "name": trainer,
                "type": info["type"],
                "schedule": info["schedule"]
            })

    for team, info in data["teams"].items():
        if trainer_name in info["trainer"].lower():
            results.append({
                "category": "TEAM",
                "name": team,
                "trainer": info["trainer"],
                "schedule": info["schedule"]
            })

    return results


if __name__ == "__main__":
    print("Расписание успешно сохранено")

    while True:
        print(f"\n{'=' * 50}")
        print("ПОИСК РАСПИСАНИЯ")
        print(f"{'=' * 50}")
        print("1 - Найти по названию группы/тренера")
        print("2 - Показать все расписание")
        print("3 - Найти по имени тренера")
        print("4 - Выйти")

        choice = input("\nВыберите действие (1-4): ").strip()

        if choice == "1":
            search = input("\nВведите название группы или имя тренера: ")
            found = find_schedule(search)

            if found:
                print(f"\nНайдено результатов: {len(found)}")
                for item in found:
                    print(f"\nКатегория: {item['category']}")
                    if item['category'] == "HIGH HEELS":
                        print(f"Тренер: {item['name']}")
                        print(f"Тип: {item['type']}")
                    else:
                        print(f"Команда: {item['name']}")
                        print(f"Тренер: {item['trainer']}")

                    if item['schedule']:
                        print("Расписание:")
                        for day, time in item['schedule'].items():
                            print(f"  {day}: {time}")
                    else:
                        print("Расписание: не указано")
                    print(f"{'-' * 40}")
            else:
                print(f"\nПо запросу '{search}' ничего не найдено.")

        elif choice == "2":
            show_all()

        elif choice == "3":
            trainer = input("\nВведите имя тренера: ")
            found = show_by_trainer(trainer)

            if found:
                print(f"\nНайдено групп у тренера: {len(found)}")
                for item in found:
                    print(f"\nКатегория: {item['category']}")
                    if item['category'] == "HIGH HEELS":
                        print(f"Тренер: {item['name']}")
                        print(f"Тип: {item['type']}")
                    else:
                        print(f"Команда: {item['name']}")
                        print(f"Тренер: {item['trainer']}")

                    if item['schedule']:
                        print("Расписание:")
                        for day, time in item['schedule'].items():
                            print(f"  {day}: {time}")
                    else:
                        print("Расписание: не указано")
                    print(f"{'-' * 40}")
            else:
                print(f"\nТренер '{trainer}' не найден.")

        elif choice == "4":
            print("\nДо свидания!")
            break

        else:
            print("\nНеверный выбор.")

        if choice != "4":
            cont = input("\nПродолжить поиск? (да/нет): ").lower()
            if cont != 'да':
                print("\nДо свидания!")
                break