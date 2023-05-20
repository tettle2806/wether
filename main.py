# import psycopg2
#
#
# db = psycopg2.connect(
#     database='ls41930',
#     user='postgres',
#     password='2806',
#     host='localhost'
# )
#
# cursor = db.cursor()
#
# username = 'Real Madrid'
# cursor.execute('''
#     INSERT INTO users (username) VALUES (%s)
# ''', (username, ))
# db.commit()
#
# cursor.execute('''
#     SELECT * FROM users
# ''')
#
# users = cursor.fetchall()
# print(users)
#
# db.close()

# Запросы с параметрами
# Запрос на сайт погоды

import requests
from datetime import datetime
import psycopg2

db = psycopg2.connect(
    database='ls41930',
    user='postgres',
    password='2806',
    host='localhost'
)

cursor = db.cursor()

parameters = {
    'appid': '137d62f3c460fac41edca5930e84af7c',
    'units': 'metric',
    'lang': 'ru'
}

while True:
    city = input('Введите город, в котором хотите узнать погоду: ')
    if city == 'stop':
        break
    parameters['q'] = city
    try:
        data = requests.get('https://api.openweathermap.org/data/2.5/weather', params=parameters).json()
        description = data['weather'][0]['description']
        temp = data['main']['temp']
        timezone = data['timezone']
        wind_speed = data['wind']['speed']
        sunrise =  datetime.utcfromtimestamp(data['sys']['sunrise'] + timezone ).strftime('%H:%M:%S')
        sunset =   datetime.utcfromtimestamp(data['sys']['sunset'] + timezone ).strftime('%H:%M:%S')
        print(f'''В городе {city} сейчас {description}
Температура: {temp} °C
Скорость ветра: {wind_speed} м/с
Рассвет: {sunrise}
Закат: {sunset}''')

        cursor.execute('''
            INSERT INTO pogoda (city, description, temperature, wind, sunrise, sunset) VALUES (%s, %s, %s, %s, %s, %s)
        ''', (city, description, temp, wind_speed, sunrise, sunset,))
        db.commit()
        cursor.execute('''
            SELECT * FROM pogoda
        ''')

        pogoda = cursor.fetchall()
        print(pogoda)

        db.close()


    except:
        print('Не верный город. Попробуйте снова')