from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def index():
    university_info = {
        'name': 'Ульяновский государственный технический университет',
        'short_name': 'УлГТУ',
        'year_founded': 1957,
        'location': 'г. Ульяновск, Россия',
        'rector': 'ВРИО Ямпольский Леонид Семёнович',
        'students_count': 'более 15 000',
        'faculties': [
            {'name': 'Инженерно-строительный факультет', 'icon': '🏗️',
             'description': 'Подготовка строителей и архитекторов'},
            {'name': 'Машиностроительный факультет', 'icon': '⚙️', 'description': 'Механика и машиностроение'},
            {'name': 'Факультет информационных систем и технологий', 'icon': '💻',
             'description': 'IT и программирование'},
            {'name': 'Энергетический факультет', 'icon': '⚡', 'description': 'Энергетика и электротехника'},
            {'name': 'Гуманитарный факультет', 'icon': '📚', 'description': 'Гуманитарные науки'},
            {'name': 'Заочный факультет', 'icon': '📅', 'description': 'Дистанционное обучение'}
        ],
        'achievements': [
            {'number': '65+', 'text': 'лет истории'},
            {'number': '15000+', 'text': 'студентов'},
            {'number': '500+', 'text': 'преподавателей'},
            {'number': '50+', 'text': 'направлений подготовки'}
        ],
        'contacts': {
            'address': '432027, г. Ульяновск, ул. Северный Венец, 32',
            'phone': '+7 (8422) 43-02-03',
            'email': 'rector@ulstu.ru',
            'website': 'https://www.ulstu.ru'
        },
        'current_year': datetime.now().year
    }

    return render_template('index.html', info=university_info)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)