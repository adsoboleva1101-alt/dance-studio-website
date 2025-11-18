import json
import matplotlib.pyplot as plt

def load_schedule_data(filename='schedule.json'):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"Загружено расписание из {filename}")
    return data

def schedule_chart(data):
    if not data:
        return
    trainers_schedule = {}

    if 'high_heels' in data:
        for trainer, info in data['high_heels'].items():
            if info['schedule']:
                trainers_schedule[trainer] = info['schedule']

    if 'teams' in data:
        for team, info in data['teams'].items():
            trainer = info['trainer']
            if info['schedule']:
                if trainer in trainers_schedule:
                    trainers_schedule[trainer].update(info['schedule'])
                else:
                    trainers_schedule[trainer] = info['schedule']

    days_ru = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
    day_to_num = {day: i for i, day in enumerate(days_ru)}

    trainers = list(trainers_schedule.keys())

    fig, ax = plt.subplots(figsize=(14, 8))

    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3', '#54A0FF']

    # Рисуем прямоугольники с расписанием
    for i, (trainer, schedule) in enumerate(trainers_schedule.items()):
        color = colors[i % len(colors)]

        for day_str, time_range in schedule.items():
            days = [d.strip() for d in day_str.split(',')]

            for day in days:
                if day in day_to_num:
                    day_num = day_to_num[day]

                    if ' - ' in time_range:
                        start, end = time_range.split(' - ')
                        start_h, start_m = map(int, start.split(':'))
                        end_h, end_m = map(int, end.split(':'))

                        # Преобразуем время в координаты
                        start_time = start_h + start_m / 60
                        end_time = end_h + end_m / 60
                        duration = end_time - start_time

                        # Рисуем прямоугольник
                        rect = plt.Rectangle((day_num, start_time), 1, duration,
                                             facecolor=color, alpha=0.7,
                                             edgecolor='white', linewidth=2)
                        ax.add_patch(rect)

                        ax.text(day_num + 0.5, start_time + duration / 2,
                                f"{start}\n-\n{end}",
                                ha='center', va='center',
                                fontsize=9, fontweight='bold',
                                color='white')

    ax.set_xlim(0, 7)
    ax.set_ylim(16, 23)

    ax.set_xticks([i + 0.5 for i in range(7)])
    ax.set_xticklabels(['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'], fontsize=12)
    ax.set_xlabel('Дни недели', fontsize=12, fontweight='bold')

    ax.set_yticks(range(16, 24))
    ax.set_yticklabels([f'{h}:00' for h in range(16, 24)], fontsize=11)
    ax.set_ylabel('Время', fontsize=12, fontweight='bold')

    ax.grid(True, alpha=0.3, linestyle='--')

    ax.set_title('Расписание тренеров', fontsize=16, fontweight='bold', pad=20)

    from matplotlib.patches import Patch

    legend_elements = [Patch(facecolor=colors[i], alpha=0.7, label=trainer)
                       for i, trainer in enumerate(trainers)]
    ax.legend(handles=legend_elements, bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    plt.show()


def main():
    data = load_schedule_data('schedule.json')

    if data:
        schedule_chart(data)
    else:
        print("Не удалось загрузить данные расписания")


if __name__ == "__main__":
    main()
