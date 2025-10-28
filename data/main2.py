import json
import datetime
import os

# Файл для хранения пользователей
USERS_FILE = "users.json"


def register_user():
    """
    Регистрация нового пользователя
    """
    print("\n" + "=" * 40)
    print("РЕГИСТРАЦИЯ НА САЙТЕ")
    print("=" * 40)

    # Собираем данные пользователя
    user_data = {}

    user_data['id'] = generate_user_id()
    user_data['name'] = input("Имя: ").strip()
    user_data['email'] = input("Email: ").strip()
    user_data['phone'] = input("Телефон: ").strip()
    user_data['age'] = input("Возраст: ").strip()

    # Добавляем дату регистрации
    user_data['registration_date'] = datetime.datetime.now().isoformat()
    user_data['status'] = "active"

    # Сохраняем пользователя
    if save_user(user_data):
        print("\nРегистрация успешна!")
        print(f"Добро пожаловать, {user_data['name']}!")
        return user_data
    else:
        print("\nОшибка регистрации")
        return None


def generate_user_id():
    """
    Генерирует уникальный ID пользователя
    """
    return f"user_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"


def save_user(user_data):
    """
    Сохраняет пользователя в JSON файл
    """
    try:
        # Читаем существующих пользователей
        users = get_all_users()

        # Проверяем email на уникальность
        for user in users:
            if user.get('email') == user_data['email']:
                print("Пользователь с таким email уже существует")
                return False

        # Добавляем нового пользователя
        users.append(user_data)

        # Сохраняем в файл
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=2)

        return True

    except Exception as e:
        print(f"Ошибка сохранения: {e}")
        return False


def get_all_users():
    """
    Возвращает список всех пользователей
    """
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except:
        return []


def show_all_users():
    """
    Показывает всех зарегистрированных пользователей (только для админа)
    """
    users = get_all_users()

    print("\n" + "=" * 50)
    print("ВСЕ ЗАРЕГИСТРИРОВАННЫЕ ПОЛЬЗОВАТЕЛИ")
    print("=" * 50)

    if not users:
        print("Пользователей пока нет")
        return

    for i, user in enumerate(users, 1):
        print(f"\n--- Пользователь {i} ---")
        print(f"ID: {user.get('id', 'Не указан')}")
        print(f"Имя: {user.get('name', 'Не указано')}")
        print(f"Email: {user.get('email', 'Не указан')}")
        print(f"Телефон: {user.get('phone', 'Не указан')}")
        print(f"Возраст: {user.get('age', 'Не указан')}")
        print(f"Дата регистрации: {user.get('registration_date', 'Не указана')}")


def search_user():
    """
    Поиск пользователя по имени или email (только для админа)
    """
    search_term = input("\nВведите имя или email для поиска: ").strip().lower()
    users = get_all_users()

    found_users = []
    for user in users:
        if (search_term in user.get('name', '').lower() or
                search_term in user.get('email', '').lower()):
            found_users.append(user)

    if found_users:
        print(f"\nНайдено пользователей: {len(found_users)}")
        for user in found_users:
            print(f"{user['name']} | {user['email']} | {user.get('phone', 'Не указан')}")
    else:
        print("Пользователи не найдены")


def show_admin_stats():
    """
    Показывает статистику только для администратора
    """
    users = get_all_users()

    stats = {
        'total_users': len(users),
        'by_age': {}
    }

    for user in users:
        age = user.get('age', 'Не указан')
        stats['by_age'][age] = stats['by_age'].get(age, 0) + 1

    print(f"\nСТАТИСТИКА:")
    print(f"Всего пользователей: {stats['total_users']}")
    print("По возрасту:")
    for age, count in stats['by_age'].items():
        print(f"  {age}: {count}")


def admin_menu():
    """
    Скрытое меню администратора с паролем
    """
    password = input("\nВведите пароль администратора: ")
    if password != "admin123":  # Простой пароль, можно изменить
        print("Неверный пароль")
        return

    while True:
        print("\n" + "=" * 40)
        print("АДМИНИСТРАТОР")
        print("=" * 40)
        print("1 - Статистика")
        print("2 - Все пользователи")
        print("3 - Поиск пользователя")
        print("4 - Назад")

        choice = input("\nВыберите действие (1-4): ").strip()

        if choice == "1":
            show_admin_stats()
        elif choice == "2":
            show_all_users()
        elif choice == "3":
            search_user()
        elif choice == "4":
            break
        else:
            print("Неверный выбор")


def main_menu():
    """
    Главное меню системы для обычных пользователей
    """
    while True:
        print("\n" + "=" * 40)
        print("СИСТЕМА РЕГИСТРАЦИИ")
        print("=" * 40)
        print("1 - Зарегистрироваться")
        print("2 - Выйти")

        choice = input("\nВыберите действие (1-2): ").strip()

        if choice == "1":
            register_user()
        elif choice == "2":
            print("👋 До свидания!")
            break
        else:
            print("Неверный выбор")


# Запуск системы
if __name__ == "__main__":
    main_menu()