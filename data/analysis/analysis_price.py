import json
import matplotlib.pyplot as plt
from collections import Counter

def get_data():
    with open('../users.json', 'r', encoding='utf-8') as file1:
        users = json.load(file1)

    with open('../prices.json', 'r', encoding='utf-8') as file2:
        prices = json.load(file2)
    return users, prices


def get_money_value(text):
    digits = []
    current_number = ""

    for char in text:
        if char.isdigit():
            current_number += char
        elif current_number:
            digits.append(int(current_number))
            current_number = ""

    if current_number:
        digits.append(int(current_number))

    if digits:
        return digits[0]
    else:
        return 0

def make_money_chart():

    users, prices = get_data()
    if not users or not prices:
        return

    directions_info = {}

    types = ['trial', 'kids', 'groups', 'other']

    for type_name in types:
        if type_name in prices:
            if type_name == 'trial':
                directions_info['trial'] = {
                    'title': prices['trial']['name'],
                    'cost': get_money_value(prices['trial']['price']),
                    'students': 0
                }
            else:
                for code, info in prices[type_name].items():
                    directions_info[code] = {
                        'title': info['name'],
                        'cost': get_money_value(info['price']),
                        'students': 0
                    }

    style_mapping = {
        'Baby': 'baby_sonya',
        'Teens': 'teens',
        'Jazz funk': 'jazz_funk',
        'High Heels': 'high_heels',
        'Girly Choreo': 'high_heels_casey',
        'Hip-hop': 'hip_hop',
        'Girly hip-hop': 'hip_hop',
        'Choreo': 'choreo'
    }

    styles_counter = Counter()
    for person in users:
        if 'style' in person:
            styles_counter[person['style']] += 1

    for dance_style, amount in styles_counter.items():
        if dance_style in style_mapping:
            dir_code = style_mapping[dance_style]
            if dir_code in directions_info:
                directions_info[dir_code]['students'] += amount

    chart_labels = []
    money_values = []
    people_counts = []
    chart_colors = []

    colors_list = ['#FFB6C1', '#87CEFA', '#98FB98', '#FFD700', '#FFA07A',
                   '#DA70D6', '#FF6347', '#40E0D0', '#EE82EE', '#9ACD32',
                   '#FFA500', '#00CED1', '#FF69B4', '#7B68EE', '#3CB371']

    all_money = 0
    all_people = 0

    sorted_dirs = sorted(directions_info.items(),
                        key=lambda item: item[1]['students'] * item[1]['cost'],
                        reverse=True)

    for index, (dir_code, info) in enumerate(sorted_dirs):
        people = info['students']
        cost = info['cost']
        title = info['title']
        money = people * cost

        if people > 0:
            all_money += money
            all_people += people

            label_text = f"{title}\n{people} чел. × {cost} руб\nИтого: {money} руб"
            chart_labels.append(label_text)
            money_values.append(money)
            people_counts.append(people)
            chart_colors.append(colors_list[index % len(colors_list)])

    plt.figure(figsize=(11, 8))

    pieces, text_elements, percent_text = plt.pie(money_values, labels=chart_labels, colors=chart_colors,
                                                  autopct=lambda val: f"{val:.1f}%",
                                                  startangle=90, textprops={'fontsize': 8})

    for text in percent_text:
        text.set_size(9)
        text.set_weight('bold')
        text.set_color('white')

    plt.title(f'Выручка по направлениям\nОбщая сумма: {all_money} руб | Всего людей: {all_people}',
              size=13, weight='bold', pad=15)

    plt.axis('equal')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    make_money_chart()