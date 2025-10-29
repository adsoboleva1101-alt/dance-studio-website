import json

data = {
    "trial": {
        "name": "ПРОБНОЕ ЗАНЯТИЕ",
        "price": "200 руб",
        "conditions": "Для открытых групп - 200 руб *при покупке абонемента в день пробного занятия - бесплатно"
    },
    "kids": {
        "baby_sonya": {
            "name": "BABY by Sonya",
            "price": "2500 руб"
        },
        "kids_dasha": {
            "name": "KIDS by Dasha",
            "price": "2600 руб"
        }
    },
    "groups": {
        "teens": {
            "name": "TEENS by Nastya / by Sonya",
            "price": "2500 руб"
        },
        "jazz_funk": {
            "name": "JAZZ FUNK by Dasha",
            "price": "2500 руб"
        },
        "high_heels": {
            "name": "HIGH HEELS by Angelina / by Ksu / by Nastya",
            "price": "3000 руб"
        },
        "heelusion": {
            "name": "HEELUSION",
            "price": "3000 руб"
        },
        "hip_hop": {
            "name": "HIP-HOP / GIRLY HIP-HOP by Chetka",
            "price": "3000 руб"
        },
        "hdk": {
            "name": "HDK",
            "price": "3000 руб"
        },
        "choreo": {
            "name": "CHOREO by Dasha Shor",
            "price": "3200 руб"
        },
        "paradox": {
            "name": "PARADOX",
            "price": "3200 руб"
        },
        "high_heels_casey": {
            "name": "HIGH HEELS / GIRLY CHOREO by Casey",
            "price": "4000 руб"
        },
        "foryou": {
            "name": "4YOU",
            "price": "4000 руб"
        }
    },
    "other": {
        "single": {
            "name": "Разовое занятие / аренда",
            "price": "600 руб"
        },
        "student": {
            "name": "Скидка студентам",
            "price": "500 руб"
        }
    }
}

with open('prices.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)


def find_price(service_name):
    service_name = service_name.lower().strip()
    results = []

    for category, services in data.items():
        if category == "trial":
            if service_name in services["name"].lower():
                results.append({
                    "category": "Пробное занятие",
                    "name": services["name"],
                    "price": services["price"],
                    "conditions": services.get("conditions", "")
                })

        elif category == "kids":
            for key, info in services.items():
                if service_name in info["name"].lower():
                    results.append({
                        "category": "Детские группы",
                        "name": info["name"],
                        "price": info["price"]
                    })

        elif category == "groups":
            for key, info in services.items():
                if service_name in info["name"].lower():
                    results.append({
                        "category": "Группы",
                        "name": info["name"],
                        "price": info["price"]
                    })

        elif category == "other":
            for key, info in services.items():
                if service_name in info["name"].lower():
                    results.append({
                        "category": "Условия",
                        "name": info["name"],
                        "price": info["price"]
                    })

    return results


def show_all():
    print(f"\n{'=' * 70}")
    print("ВСЕ УСЛУГИ И ЦЕНЫ")
    print(f"{'=' * 70}")

    for category, services in data.items():
        if category == "trial":
            print(f"\n{services['name']}:")
            print(f"   Цена: {services['price']}")
            print(f"   Условия: {services['conditions']}")

        elif category == "kids":
            print(f"\nДЕТСКИЕ ГРУППЫ:")
            for key, info in services.items():
                print(f"   • {info['name']}: {info['price']}")

        elif category == "groups":
            print(f"\nГРУППЫ:")
            for key, info in services.items():
                print(f"   • {info['name']}: {info['price']}")

        elif category == "other":
            print(f"\nУСЛОВИЯ:")
            for key, info in services.items():
                print(f"   • {info['name']}: {info['price']}")


if __name__ == "__main__":
    print("Данные о ценах успешно сохранены")

    while True:
        print(f"\n{'=' * 50}")
        print("ПОИСК ЦЕН НА УСЛУГИ")
        print(f"{'=' * 50}")
        print("1 - Найти цену услуги")
        print("2 - Показать все услуги")
        print("3 - Выйти")

        choice = input("\nВыберите действие (1-3): ").strip()

        if choice == "1":
            service = input("\nВведите название услуги: ")
            found = find_price(service)

            if found:
                print(f"\nНайдено услуг: {len(found)}")
                for item in found:
                    print(f"\nКатегория: {item['category']}")
                    print(f"Услуга: {item['name']}")
                    print(f"Цена: {item['price']}")
                    if item.get('conditions'):
                        print(f"Условия: {item['conditions']}")
                    print(f"{'-' * 40}")
            else:
                print(f"\nУслуги по запросу '{service}' не найдены.")

        elif choice == "2":
            show_all()

        elif choice == "3":
            print("\nДо свидания!")
            break

        else:
            print("\nНеверный выбор.")

        if choice != "3":
            cont = input("\nПродолжить поиск? (да/нет): ").lower()
            if cont != 'да':
                print("\nДо свидания!")
                break
