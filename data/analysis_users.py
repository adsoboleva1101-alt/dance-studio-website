import json
import matplotlib.pyplot as plt
from collections import Counter

# Настройка стиля графиков
plt.style.use('default')
plt.rcParams['font.family'] = 'DejaVu Sans'

# Загрузка данных из файла users.json
def load_users_data(filename='users.json'):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"Загружено {len(data)} записей из {filename}")
    return data

#График 1: Распределение возрастов по стилям
def plot_age_by_style(data):
    if not data:
        return
    style_ages = {}
    for user in data:
        if 'style' in user:
            style = user['style']
            age = int(user['age'])
            if style not in style_ages:
                style_ages[style] = []
            style_ages[style].append(age)

    styles_sorted = sorted(style_ages.keys(), key=lambda x: sum(style_ages[x]) / len(style_ages[x]))

    means = [sum(ages) / len(ages) for ages in style_ages.values()]
    counts = [len(ages) for ages in style_ages.values()]
    plt.figure(figsize=(12, 8))
    colors = ['#D4A5A5', '#9EB7E5', '#A2D5AC', '#E9C46A', '#F4A261', '#E76F51', '#8AC6D1', '#B8B3E9']

    bars = plt.bar(styles_sorted, means, color=colors[:len(styles_sorted)],
                   alpha=0.8, edgecolor='black', linewidth=1.5)

    for i, (bar, mean, count) in enumerate(zip(bars, means, counts)):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                 f'{mean:.1f} лет', ha='center', va='bottom', fontweight='bold', fontsize=11)

        plt.text(bar.get_x() + bar.get_width() / 2, -0.5, f'n={count}',
                 ha='center', va='top', fontsize=9, color='gray')

    plt.title('Средний возраст людей по стилям танцев', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Стиль танцев', fontsize=12)
    plt.ylabel('Средний возраст (лет)', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3, axis='y')
    plt.ylim(0, max(means) + 2)

    plt.tight_layout()
    plt.show()

    print("Статистика по стилям:")
    print("-" * 50)
    for style in styles_sorted:
        ages = style_ages[style]
        avg_age = sum(ages) / len(ages)
        print(f"{style:15} | {len(ages):2} студентов | Средний возраст: {avg_age:5.1f} лет")

# График 2: Популярность направлений танцев
def plot_style_popularity(data):
    if not data:
        return

    styles = []
    for user in data:
        if 'style' in user:
            styles.append(user['style'])
    style_counts = Counter(styles)
    sorted_styles = sorted(style_counts.items(), key=lambda x: x[1], reverse=True)
    styles_names = [item[0] for item in sorted_styles]
    styles_counts = [item[1] for item in sorted_styles]
    plt.figure(figsize=(12, 8))

    colors = ['#D4A5A5', '#9EB7E5', '#A2D5AC', '#E9C46A', '#F4A261', '#E76F51', '#8AC6D1', '#B8B3E9']
    bars = plt.bar(styles_names, styles_counts, color=colors, edgecolor='black', alpha=0.8)

    for bar, count in zip(bars, styles_counts):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                 f'{count}', ha='center', va='bottom', fontweight='bold', fontsize=11)

    plt.title('Популярность направлений танцев', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Стиль танцев', fontsize=12)
    plt.ylabel('Количество студентов', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.show()

    total_students = len(styles)
    print("\n" + "=" * 50)
    print("Популярность направлений:")
    print("-" * 50)
    for style, count in sorted_styles:
        percentage = (count / total_students) * 100
        print(f" {style:15} | {count:2} студентов | {percentage:5.1f}%")


# График 3: Распределение по возрастам
def plot_age_distribution(data):
    if not data:
        return

    ages = [int(user['age']) for user in data if 'age' in user]
    plt.figure(figsize=(12, 6))

    n, bins, patches = plt.hist(ages, bins=range(4, 26), edgecolor='black', alpha=0.7, color='lightblue', rwidth=0.8)

    plt.title('Распределение человек по возрастам', fontsize=16, fontweight='bold')
    plt.xlabel('Возраст (лет)', fontsize=12)
    plt.ylabel('Количество человек', fontsize=12)
    plt.grid(True, alpha=0.3, axis='y')

    for i, count in enumerate(n):
        if count > 0:
            plt.text(bins[i] + 0.5, count + 0.1, int(count),
                     ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plt.show()

    # Статистика по возрастам
    print("\n" + "=" * 50)
    print("Общая статистика по возрастам:")
    print("-" * 50)
    print(f"Всего человек: {len(ages)}")
    avg_age = sum(ages) / len(ages)
    print(f"Средний возраст: {avg_age:.1f} лет")
    sorted_ages = sorted(ages)
    n = len(sorted_ages)
    if n % 2 == 1:
        median_age = sorted_ages[n // 2]
    else:
        median_age = (sorted_ages[n // 2 - 1] + sorted_ages[n // 2]) / 2
    print(f"Медианный возраст: {median_age} лет")
    print(f"Возрастной диапазон: {min(ages)}-{max(ages)} лет")


# График 4: соотношение стилей
def plot_style_pie_chart(data):
    if not data:
        return

    styles = []
    for user in data:
        if 'style' in user:
            styles.append(user['style'])

    style_counts = Counter(styles)
    sorted_styles = sorted(style_counts.items(), key=lambda x: x[1], reverse=True)

    plt.figure(figsize=(10, 8))

    labels = [item[0] for item in sorted_styles]
    sizes = [item[1] for item in sorted_styles]
    pastel_colors = ['#F8C8DC', '#B5EAD7', '#FFDAC1', '#C7CEEA', '#E2F0CB',
                     '#FFB7B2', '#D8BFD8', '#AFEEEE', '#F0E68C', '#FFDAB9']

    colors = pastel_colors[:len(labels)]
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
            startangle=90, shadow=False)
    plt.axis('equal')  # Чтобы диаграмма была круглой
    plt.title('Соотношение стилей танцев\n',
              fontsize=16, fontweight='bold', pad=20)

    plt.tight_layout()
    plt.show()

def main():
    data = load_users_data('users.json')

    if data:
        plot_age_by_style(data)
        plot_style_popularity(data)
        plot_age_distribution(data)
        plot_style_pie_chart(data)

        print(f"Проанализировано записей: {len(data)}")

        styles_count = len(set(user.get('style', '') for user in data if 'style' in user))
        print(f"Количество направлений: {styles_count}")

    else:
        print("Не удалось загрузить данные для анализа")

if __name__ == "__main__":
    main()