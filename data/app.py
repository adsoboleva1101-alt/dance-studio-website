from flask import Flask, request, render_template, redirect, session, jsonify, g
import json
from datetime import datetime
import os
import sqlite3

app = Flask(__name__)
app.secret_key = 'dance-studio-secret-key'
DATABASE = 'dance_studio.db'

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


def get_db():
    """Получить соединение с базой данных"""
    if 'db' not in g:
        print(f"Подключаемся к базе: {DATABASE}")
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row

        cursor = g.db.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"Таблицы в базе: {[t[0] for t in tables]}")

    return g.db


def close_db(e=None):
    """Закрыть соединение с базой данных"""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    """Инициализировать базу данных - создает таблицу если её нет"""
    with app.app_context():
        db = get_db()

        try:
            cursor = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
            table_exists = cursor.fetchone()

            if not table_exists:
                print("Создаем таблицу users...")

                db.execute('''
                    CREATE TABLE users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        age INTEGER NOT NULL,
                        phone TEXT,
                        registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_login TIMESTAMP,
                        is_active BOOLEAN DEFAULT 1
                    )
                ''')
                db.commit()
                print("✓ Таблица users успешно создана")
            else:
                print("✓ Таблица users уже существует")

                cursor = db.execute("SELECT COUNT(*) FROM users")
                count = cursor.fetchone()[0]
                print(f"✓ Записей в таблице users: {count}")
                cursor = db.execute("PRAGMA table_info(users)")
                columns = [col[1] for col in cursor.fetchall()]

                if 'phone' not in columns:
                    print("Добавляем столбец phone...")
                    db.execute('ALTER TABLE users ADD COLUMN phone TEXT')
                    db.commit()
                    print("Столбец phone добавлен")

        except sqlite3.Error as e:
            print(f"Ошибка при инициализации базы данных: {e}")
            raise


app.teardown_appcontext(close_db)
init_db()


@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')


@app.route('/profile')
def profile():
    """Личный кабинет - ИСПРАВЛЕННЫЙ ВАРИАНТ"""
    user_id = session.get('user_id')

    if not user_id:
        return redirect('/login')

    try:
        db = get_db()

        cursor = db.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()

        if user:
            user_dict = dict(user)
            return render_template('profile.html', user=user_dict)
        else:
            return redirect('/login')

    except sqlite3.Error as e:
        print(f"Ошибка при загрузке профиля: {e}")
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
        age_choice = data.get('age')
        answers = data.get('answers', [])
        user_id = session.get('user_id')

        # 1. Если возраст 4-5 или 7-9 лет
        if age_choice == "A":
            result = {
                "style": "Baby 4-5",
                "age": "4-5 лет",
                "teacher": "Соня Баловнева",
                "description": "Идеально для малышей!"
            }
        elif age_choice == "B":
            result = {
                "style": "Kids 7-9",
                "age": "7-9 лет",
                "teacher": "Даша Шорникова",
                "description": "Танцы для детей!"
            }
        else:
            # 2. Для возраста 10+ лет анализируем ответы
            question_weights = {
                2: {"А": {"Choreo": 2}, "Б": {"High Heels": 2}, "В": {"Hip-hop": 3},
                    "Г": {"Girly hip-hop": 2}, "Д": {"Girly Choreo": 2}, "Е": {"Jazz Funk": 3}},
                3: {"А": {"Choreo": 3}, "Б": {"High Heels": 3}, "В": {"Hip-hop": 3},
                    "Г": {"Girly hip-hop": 2}, "Д": {"Girly Choreo": 3}, "Е": {"Jazz Funk": 2}},
                4: {"А": {"Choreo": 2}, "Б": {"High Heels": 3}, "В": {"Hip-hop": 3},
                    "Г": {"Girly hip-hop": 2}, "Д": {"Girly Choreo": 3}, "Е": {"Jazz Funk": 3}},
                5: {"А": {"Choreo": 1}, "Б": {"High Heels": 2}, "В": {"Hip-hop": 2},
                    "Г": {"Girly hip-hop": 1}, "Д": {"Girly Choreo": 2}, "Е": {"Jazz Funk": 3}},
                6: {"А": {"Choreo": 2}, "Б": {"High Heels": 3}, "В": {"Hip-hop": 3},
                    "Г": {"Girly hip-hop": 2}, "Д": {"Girly Choreo": 3}, "Е": {"Jazz Funk": 3}},
                7: {"А": {"Choreo": 1}, "Б": {"High Heels": 1}, "В": {"Hip-hop": 2},
                    "Г": {"Girly hip-hop": 1}, "Д": {"Girly Choreo": 1}, "Е": {"Jazz Funk": 2}},
                8: {"А": {"Choreo": 3}, "Б": {"High Heels": 3}, "В": {"Hip-hop": 2},
                    "Г": {"Girly hip-hop": 2}, "Д": {"Girly Choreo": 3}, "Е": {"Jazz Funk": 3}},
                9: {"А": {"Choreo": 1}, "Б": {"High Heels": 2}, "В": {"Hip-hop": 2},
                    "Г": {"Girly hip-hop": 1}, "Д": {"Girly Choreo": 2}, "Е": {"Jazz Funk": 1}},
                10: {"А": {"Choreo": 1}, "Б": {"High Heels": 1}, "В": {"Hip-hop": 2},
                     "Г": {"Girly hip-hop": 1}, "Д": {"Girly Choreo": 1}, "Е": {"Jazz Funk": 2}}
            }

            style_scores = {"Choreo": 0, "High Heels": 0, "Hip-hop": 0,
                           "Girly hip-hop": 0, "Girly Choreo": 0, "Jazz Funk": 0, "Teens 10-13": 0}

            for i, answer in enumerate(answers):
                question_num = i + 2
                if question_num in question_weights and answer in question_weights[question_num]:
                    for style, weight in question_weights[question_num][answer].items():
                        if style in style_scores:
                            style_scores[style] += weight

            recommended_style = max(style_scores, key=style_scores.get)

            # 3. Проверяем возрастные ограничения
            age_mapping = {
                "C": {"text": "10-13 лет", "numeric": 12},
                "D": {"text": "14-15 лет", "numeric": 14},
                "E": {"text": "16-17 лет", "numeric": 16},
                "F": {"text": "18+ лет", "numeric": 18}
            }

            age_info = age_mapping.get(age_choice, {"text": "18+ лет", "numeric": 18})
            user_age = age_info["numeric"]

            min_age_requirements = {
                "Choreo": 14, "Hip-hop": 14, "Girly hip-hop": 14,
                "Jazz Funk": 12, "High Heels": 16, "Girly Choreo": 16
            }

            teachers_by_style = {
                "Choreo": "Даша Шорникова",
                "High Heels": "Катя Бударина, Настя Семенова, Ангелина Сумина, Ксения Лунева",
                "Hip-hop": "Катя Четина",
                "Girly hip-hop": "Катя Четина",
                "Girly Choreo": "Катя Бударина, Ксения Лунева",
                "Jazz Funk": "Даша Мигрова",
                "Teens 10-13": "Настя Кюннап, Соня Баловнева"
            }

            style_descriptions = {
                "Choreo": "Универсальный стиль! Современная хореография.",
                "High Heels": "Чувственные танцы на каблуках!",
                "Hip-hop": "Энергия улиц! Свободный стиль.",
                "Girly hip-hop": "Легкий хип-хоп! Женственный взгляд.",
                "Girly Choreo": "Женственная хореография!",
                "Jazz Funk": "Эмоциональный танец!",
                "Teens 10-13": "Для подростков! Самовыражение."
            }

            final_style = recommended_style
            final_teacher = teachers_by_style.get(recommended_style, "")

            # Проверка возрастных ограничений
            if recommended_style in min_age_requirements:
                min_age = min_age_requirements[recommended_style]
                if user_age < min_age:
                    if age_choice == "C":
                        if recommended_style == "Jazz Funk" and user_age >= 12:
                            pass
                        else:
                            final_style = "Teens 10-13"
                            final_teacher = teachers_by_style["Teens 10-13"]
                    elif age_choice == "D":
                        if recommended_style in ["High Heels", "Girly Choreo"]:
                            final_style = "Choreo"
                            final_teacher = teachers_by_style["Choreo"]

            result = {
                "style": final_style,
                "age": age_info["text"],
                "teacher": final_teacher,
                "description": style_descriptions.get(final_style, "Идеальный стиль!"),
                "questions_count": 10,
                "date": datetime.now().isoformat()
            }

        # Сохраняем результат
        results = load_json_file(RESULTS_FILE)
        results.append(result)
        save_json_file(RESULTS_FILE, results)

        if user_id:
            try:
                db = get_db()
                db.execute('''
                    INSERT INTO test_results (user_id, age_group, dance_style, recommended_trainer)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, result["age"], result["style"], result["teacher"]))
                db.commit()
            except Exception as e:
                print(f"Ошибка сохранения в БД: {e}")

        return jsonify(result)

    except Exception as e:
        print(f"Ошибка в process_test: {e}")
        return jsonify({"error": "Ошибка обработки теста"}), 500

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


@app.route('/check_db')
def check_database():
    """Проверка состояния базы данных"""
    try:
        db = get_db()
        cursor = db.cursor()

        result = "<h1>Проверка базы данных</h1>"
        result += f"<p>Путь к файлу: {os.path.abspath(DATABASE)}</p>"
        result += f"<p>Файл существует: {os.path.exists(DATABASE)}</p>"

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        result += "<h2>Таблицы в базе:</h2><ul>"
        for table in tables:
            result += f"<li>{table[0]}</li>"
        result += "</ul>"

        if any('users' in t for t in tables):
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            result += f"<p>Записей в таблице users: {count}</p>"

            if count > 0:
                cursor.execute("SELECT * FROM users ORDER BY id DESC")
                users = cursor.fetchall()

                result += "<h2>Зарегистрированные пользователи:</h2>"
                result += "<table border='1' style='border-collapse: collapse;'>"
                result += "<tr><th>ID</th><th>Имя</th><th>Email</th><th>Телефон</th><th>Возраст</th></tr>"

                for user in users:
                    result += f"<tr><td>{user[0]}</td><td>{user[1]} {user[2]}</td><td>{user[3]}</td><td>{user[6]}</td><td>{user[5]}</td></tr>"

                result += "</table>"

        return result

    except Exception as e:
        return f"<h1>Ошибка</h1><p>{str(e)}</p>"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            db = get_db()

            # Ищем пользователя
            cursor = db.execute('SELECT * FROM users WHERE email = ?', (email,))
            user = cursor.fetchone()

            if user:
                if user['password'] == password:
                    # Обновляем last_login
                    db.execute('UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?', (user['id'],))
                    db.commit()

                    # ДОБАВЛЕНО: Сохраняем в сессию
                    session['user_id'] = user['id']
                    session['user_name'] = user['first_name']
                    session['user_email'] = user['email']

                    print(f"Пользователь {email} вошел, ID: {user['id']}")
                    return redirect('/')
                else:
                    return render_template('login.html',
                                           error="Неверный пароль",
                                           form_data={'email': email})
            else:
                return render_template('login.html',
                                       error="Пользователь с таким email не найден",
                                       form_data={'email': email})
        except sqlite3.Error as e:
            return render_template('login.html',
                                   error=f"Ошибка базы данных: {str(e)}",
                                   form_data={'email': email})

    message = request.args.get('message')
    return render_template('login.html', message=message)


# Страница регистрации
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        first_name = request.form.get('name')
        last_name = request.form.get('surname')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')
        age = request.form.get('age')

        print(f"Попытка регистрации: {first_name} {last_name}, email: {email}, phone: {phone}, age: {age}")

        # Валидация
        if not all([first_name, last_name, email, password, phone, age]):
            return render_template('registration.html',
                                   error="Все поля обязательны для заполнения",
                                   form_data=request.form)

        if '@' not in email or '.' not in email:
            return render_template('registration.html',
                                   error="Неверный формат email",
                                   form_data=request.form)

        try:
            age_int = int(age)
            if age_int < 0 or age_int > 150:
                return render_template('registration.html',
                                       error="Неверный возраст",
                                       form_data=request.form)
        except ValueError:
            return render_template('registration.html',
                                   error="Возраст должен быть числом",
                                   form_data=request.form)

        try:
            db = get_db()

            cursor = db.execute('SELECT id FROM users WHERE email = ?', (email,))
            if cursor.fetchone():
                return render_template('registration.html',
                                       error="Пользователь с таким email уже существует",
                                       form_data=request.form)

            cursor = db.execute(
                '''INSERT INTO users (first_name, last_name, email, password, age, phone) 
                   VALUES (?, ?, ?, ?, ?, ?)''',
                (first_name, last_name, email, password, age_int, phone)
            )
            db.commit()

            user_id = cursor.lastrowid
            print(f"✓ Пользователь зарегистрирован! ID: {user_id}")

            return redirect('/login?message=Регистрация успешна! Теперь войдите в систему')

        except sqlite3.IntegrityError as e:
            print(f"Ошибка целостности: {e}")
            return render_template('registration.html',
                                   error="Пользователь с таким email уже существует",
                                   form_data=request.form)
        except sqlite3.Error as e:
            print(f"Ошибка SQLite: {e}")
            return render_template('registration.html',
                                   error=f"Ошибка базы данных: {str(e)}",
                                   form_data=request.form)

    return render_template('registration.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    if not os.path.exists(USERS_FILE):
        save_json_file(USERS_FILE, [])
    if not os.path.exists(RESULTS_FILE):
        save_json_file(RESULTS_FILE, [])

    print("Откройте в браузере: http://localhost:5000")
    print("Проверка БД: http://localhost:5000/check_db")
    app.run(debug=True, host='0.0.0.0', port=5000)
