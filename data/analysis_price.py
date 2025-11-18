import json
import matplotlib.pyplot as plt
from collections import Counter
import re


def load_data():
    """Загружает данные из двух JSON файлов"""
    try:
        with open('users.json', 'r', encoding='utf-8') as f:
            users_data = json.load(f)

        with open('prices.json', 'r', encoding='utf-8') as f:
            prices_data = json.load(f)

        print(f"Загружено {len(users_data)} студентов и данные о ценах")
        return users_data, prices_data

    except FileNotFoundError as e:
        print(f"Файл не найден: {e}")
        return None, None
    except json.JSONDecodeError:
        print("Ошибка чтения JSON файла")
        return None, None

# функция извлекает числовое значение цены из строки
def extract_price(price_str):
    match = re.search(r'(\d+)', price_str)
    return int(match.group(1)) if match else 0

# Создание круговой диаграммы
def create_comprehensive_revenue_chart():

    users_data, prices_data = load_data()
    if not users_data or not prices_data:
        return

    direction_data = {}

    categories = ['trial', 'kids', 'groups', 'other']

    for category in categories:
        if category in prices_data:
            if category == 'trial':
                # Пробное занятие - отдельная запись
                direction_data['trial'] = {
                    'name': prices_data['trial']['name'],
                    'price': extract_price(prices_data['trial']['price']),
                    'count': 0
                }
            else:
                # kids, groups, other - словари с направлениями
                for key, value in prices_data[category].items():
                    direction_data[key] = {
                        'name': value['name'],
                        'price': extract_price(value['price']),
                        'count': 0
                    }

    style_to_direction = {
        'Baby': 'baby_sonya',
        'Teens': 'teens',
        'Jazz funk': 'jazz_funk',
        'High Heels': 'high_heels',
        'Girly Choreo': 'high_heels_casey',
        'Hip-hop': 'hip_hop',
        'Girly hip-hop': 'hip_hop',
        'Choreo': 'choreo'
    }

    styles_count = Counter()
    for user in users_data:
        if 'style' in user:
            styles_count[user['style']] += 1

    for style, count in styles_count.items():
        if style in style_to_direction:
            direction_key = style_to_direction[style]
            if direction_key in direction_data:
                direction_data[direction_key]['count'] += count

    labels = []
    revenues = []
    student_counts = []
    colors = []

    color_palette = ['#FFB6C1', '#87CEFA', '#98FB98', '#FFD700', '#FFA07A',
                     '#DA70D6', '#FF6347', '#40E0D0', '#EE82EE', '#9ACD32',
                     '#FFA500', '#00CED1', '#FF69B4', '#7B68EE', '#3CB371']

    total_revenue = 0
    total_students = 0

    sorted_directions = sorted(direction_data.items(),
                               key=lambda x: x[1]['count'] * x[1]['price'],
                               reverse=True)

    for i, (direction_key, data) in enumerate(sorted_directions):
        count = data['count']
        price = data['price']
        name = data['name']
        revenue = count * price

        if count > 0:  # Показываем только направления со студентами
            total_revenue += revenue
            total_students += count

            # Формируем подпись
            short_name = name
            if len(name) > 30:
                short_name = name[:27] + "..."

            label = f"{short_name}\n{count} чел. × {price} руб\n= {revenue} руб"
            labels.append(label)
            revenues.append(revenue)
            student_counts.append(count)
            colors.append(color_palette[i % len(color_palette)])

    plt.figure(figsize=(12, 9))

    wedges, texts, autotexts = plt.pie(revenues, labels=labels, colors=colors,
                                       autopct=lambda pct: f"{pct:.1f}%",
                                       startangle=90, textprops={'fontsize': 7})

    for autotext in autotexts:
        autotext.set_fontsize(8)
        autotext.set_fontweight('bold')
        autotext.set_color('white')

    plt.title(f'Выручка по направлениям\nВсего: {total_revenue} руб | Человек: {total_students}',
              fontsize=14, fontweight='bold', pad=20)

    plt.axis('equal')
    plt.tight_layout()
    plt.show()

    # Выводим полную статистику
    print("\n" + "-" * 50)
    print("Полная статистика по всем направлениям:")
    print("=" * 80)

    print(f"\nОБЩАЯ СТАТИСТИКА:")
    print(f"Всего человек: {total_students}")
    print(f"Общая выручка: {total_revenue} руб")
    print(f"Количество активных направлений: {len(revenues)}")

    print(f"\nДетали по направлениям:")
    print("-" * 50)

    for direction_key, data in sorted_directions:
        if data['count'] > 0:
            count = data['count']
            price = data['price']
            name = data['name']
            revenue = count * price
            percentage = (revenue / total_revenue) * 100

            print(f"\n{name}:")
            print(f"Человек: {count}")
            print(f"Цена: {price} руб")
            print(f"Выручка: {revenue} руб ({percentage:.1f}%)")

if __name__ == "__main__":
    create_comprehensive_revenue_chart()