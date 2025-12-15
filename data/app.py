from flask import Flask, request, render_template, redirect, session, jsonify
import json
import datetime
import os
import requests

app = Flask(__name__)
app.secret_key = 'dance-studio-secret-key'

# Данные тренеров
COACHES_DATA = [
    {
        'id': 1,
        "name": "Даша Шорникова",
        "specialization": ["choreo", "Kids 7-9"],
        "vk": "https://vk.com/dariashorrrnikova",
        "instagram": "@shornikova_d",
        "story": "Даша - талантливый хореограф с многолетним опытом работы с детьми. Её занятия всегда наполнены энергией и творчеством. Она умеет находить подход к каждому ребёнку, помогая раскрыть их танцевальный потенциал."
    },
    {
        'id': 2,
        "name": "Катя Четина",
        "specialization": ["hip-hop", "Girly hip-hop"],
        "vk": "https://vk.com/chetka17?from=search",
        "instagram": "@chetka17",
        "story": "Катя - настоящая звезда хип-хоп сцены. Её стиль - это уникальное сочетание мощной энергии и женственности. На занятиях она создаёт атмосферу, где каждый может почувствовать себя уверенно и свободно."
    },
    {
        'id': 3,
        "name": "Катя Бударина",
        "specialization": ["High Heels", "Girly choreo"],
        "vk": "https://vk.com/casey7",
        "instagram": "@caseeey7",
        "story": "Катя - эксперт в направлении High Heels. Её уроки - это не просто танцы, а целое искусство движения на каблуках. Она учит не только технике, но и уверенности в себе, грации и женственности."
    },
    {
        'id': 4,
        "name": "Настя Кюннап",
        "specialization": ["Teens 10-14"],
        "vk": "https://vk.com/anastaaaasik?from=search",
        "instagram": "@anastas.ka_",
        "story": "Настя специализируется на работе с подростками. Она понимает психологию этого возраста и создаёт комфортную среду для творческого развития. Её ученики не только учатся танцевать, но и находят себя."
    },
    {
        'id': 5,
        "name": "Настя Семенова",
        "specialization": ["High Heels"],
        "vk": "https://vk.com/naastasyaaa",
        "instagram": "к сожалению нету",
        "story": "Настя - страстный преподаватель High Heels с уникальным подходом к обучению. Она верит, что каждая женщина может чувствовать себя королевой на сцене и в жизни. Её занятия - это трансформация и раскрытие внутренней силы."
    },
    {
        'id': 6,
        "name": "Даша Мигрова",
        "specialization": ["Jazz funk"],
        "vk": "https://vk.com/ddddddddddddddddasha",
        "instagram": "@ddddddddddddasha_",
        "story": "Даша привносит невероятную энергию в свои занятия Jazz funk. Её стиль - это взрывная смесь джаза и фанка. Она вдохновляет учеников экспериментировать и находить свой уникальный стиль в танце."
    },
    {
        'id': 7,
        "name": "Соня Баловнева",
        "specialization": ["Teens 10-14", "baby 4-5"],
        "vk": "https://vk.com/sooooofiaaaaaaa",
        "instagram": "@_so_nka",
        "story": "Соня - универсальный преподаватель, работающий как с малышами, так и с подростками. Её терпение и любовь к детям делают каждое занятие особенным. Она создаёт волшебную атмосферу, где даже самые маленькие танцоры чувствуют себя звездами."
    },
    {
        'id': 8,
        "name": "Ангелина Сумина",
        "specialization": ["High Heels"],
        "vk": "https://vk.com/angelinasumina",
        "instagram": "@angelinasumina",
        "story": "Ангелина - элегантный и техничный преподаватель High Heels. Её уроки - это мастер-класс по грации и уверенности. Она помогает каждой ученице раскрыть свою внутреннюю богиню и танцевать с невероятной страстью."
    },
    {
        'id': 9,
        "name": "Ксения Лунева",
        "specialization": ["High Heels", "Girly choreo"],
        "vk": "https://vk.com/id168724997",
        "instagram": "к сожалению нету",
        "story": "Ксения - разносторонний хореограф, сочетающий в своей работе технику High Heels и женственной хореографии. Её подход основан на индивидуальности каждой ученицы, помогая им найти свой уникальный стиль и выразить себя через танец."
    }
]

# Данные расписания
SCHEDULE_DATA = {
    "high_heels": {
        "Ангелина Сумина": {
            "type": "открытая группа",
            "schedule": {
                "вторник, четверг": "21:00 - 22:00"
            }
        },
        "Ксюша Лунева": {
            "type": "открытая группа",
            "schedule": {
                "понедельник, среда": "20:30 - 21:30"
            }
        },
        "Катя Бударина": {
            "type": "с нуля",
            "schedule": {
                "вторник, четверг": "10:00 - 11:00",
                "понедельник, среда": "20:00 - 21:00"
            }
        },
        "Настя Семенова": {
            "type": "открытая группа",
            "schedule": {
                "вторник, четверг": "19:30 - 20:30"
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
    },
    "hip-hop": {
        "Катя Четина": {
            "type": "открытая группа",
            "schedule": {
                "вторник, четверг": "17:00 - 18:00"
            }
        }
    },
    "girly_hip_hop": {
        "Катя Четина": {
            "type": "открытая группа",
            "schedule": {
                "вторник, четверг": "20:00 - 21:00"
            }
        }
    },
    "choreo": {
        "Даша Шорникова": {
            "type": "открытая группа",
            "schedule": {
                "вторник, четверг": "18:00 - 19:00"
            }
        }
    },
    "girly_choreo": {
        "Катя Бударина": {
            "type": "открытая группа",
            "schedule": {
                "понедельник, среда": "19:00 - 20:00"
            }
        },
        "Ксюша Лунева": {
            "type": "открытая группа",
            "schedule": {
                "понедельник, среда": "19:30 - 20:30"
            }
        }
    }
}

# Данные цен
PRICES_DATA = {
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
        "hip_hop": {
            "name": "HIP-HOP / GIRLY HIP-HOP by Chetka",
            "price": "3000 руб"
        },
        "choreo": {
            "name": "CHOREO by Dasha Shor",
            "price": "3200 руб"
        },
        "high_heels_casey": {
            "name": "HIGH HEELS / GIRLY CHOREO by Casey",
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

USERS_FILE = "users.json"
RESULTS_FILE = "results.json"


def load_json_file(filename):
    """Загрузка данных из JSON файла"""
    try:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Ошибка загрузки файла {filename}: {e}")
        return []


def save_json_file(filename, data):
    """Сохранение данных в JSON файла"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Ошибка сохранения файла {filename}: {e}")
        return False


@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')


@app.route('/profile')
def profile():
    """Личный кабинет"""
    user_id = session.get('user_id')

    if not user_id:
        return redirect('/login')

    users = load_json_file(USERS_FILE)

    for user in users:
        if user['id'] == user_id:
            return render_template('profile.html', user=user)

    return redirect('/login')


@app.route('/test')
def test():
    """Страница теста стиля"""
    return render_template('test.html')


@app.route('/api/test', methods=['POST'])
def process_test():
    """Обработка теста стиля"""
    try:
        data = request.json
        age = data.get('age')
        answers = data.get('answers', [])

        # Определение стиля на основе возраста и ответов
        if age == "A":
            result = {"style": "Baby 4-5", "age": "4-5 лет", "teacher": "Соня Баловнева"}
        elif age == "B":
            result = {"style": "Kids 7-9", "age": "7-9 лет", "teacher": "Даша Шорникова"}
        else:
            # Для взрослых определяем стиль по ответам
            style_map = {
                "A": "Choreo",
                "B": "High Heels",
                "C": "Hip-hop",
                "D": "Girly hip-hop",
                "E": "Girly Choreo",
                "F": "Jazz Funk"
            }

            if answers:
                style = style_map.get(answers[0], "Choreo")
            else:
                style = "Choreo"

            # Проверка возрастных ограничений
            if (style in ["High Heels", "Girly Choreo"]) and age in ["C", "D"]:
                style = "Choreo"

            # Определение тренера
            teachers = {
                "Choreo": "Даша Шорникова",
                "High Heels": "Катя Бударина, Настя Семенова, Ангелина Сумина, Ксения Лунева",
                "Hip-hop": "Катя Четина",
                "Girly hip-hop": "Катя Четина",
                "Girly Choreo": "Катя Бударина, Ксения Лунева",
                "Jazz Funk": "Даша Мигрова"
            }

            age_texts = {
                "C": "10-13 лет",
                "D": "14-15 лет",
                "E": "16-17 лет",
                "F": "18+ лет"
            }

            result = {
                "style": style,
                "age": age_texts.get(age, "18+ лет"),
                "teacher": teachers.get(style, "Даша Шорникова")
            }

        # Сохранение результата
        result["date"] = datetime.datetime.now().isoformat()
        results = load_json_file(RESULTS_FILE)
        results.append(result)
        save_json_file(RESULTS_FILE, results)

        return jsonify(result)

    except Exception as e:
        print(f"Ошибка в process_test: {e}")
        return jsonify({"error": "Произошла ошибка"}), 500


@app.route('/schedule')
def schedule():
    """Страница расписания"""
    user_name = session.get('user_name')
    return render_template('schedule.html', schedule_data=SCHEDULE_DATA, user_name=user_name)


@app.route('/coaches')
def coaches():
    """Страница тренеров"""
    user_name = session.get('user_name')
    return render_template('coaches.html', coaches_data=COACHES_DATA, user_name=user_name)


@app.route('/dances')
def dances():
    """ Функция для отображения страницы "О танцах" """
    return render_template('dances.html')


@app.route('/prices')
def prices():
    """Страница цен"""
    user_name = session.get('user_name')
    return render_template('prices.html', prices_data=PRICES_DATA, user_name=user_name)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    """Страница регистрации"""
    if request.method == 'POST':
        user_data = {
            'id': f"user_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'age': request.form.get('age'),
            'registration_date': datetime.datetime.now().isoformat(),
            'status': 'active'
        }

        users = load_json_file(USERS_FILE)

        if any(user.get('email') == user_data['email'] for user in users):
            return render_template('registration.html',
                                 error="Пользователь с таким email уже существует",
                                 form_data=request.form)

        users.append(user_data)
        if save_json_file(USERS_FILE, users):
            return redirect('/')
        else:
            return render_template('registration.html', error="Ошибка регистрации")

    return render_template('registration.html')


if __name__ == '__main__':
    if not os.path.exists(USERS_FILE):
        save_json_file(USERS_FILE, [])
    if not os.path.exists(RESULTS_FILE):
        save_json_file(RESULTS_FILE, [])

    print("Запуск сайта танцевальной студии...")
    print("Откройте в браузере: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)