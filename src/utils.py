import json
import datetime


def date_transactions():
    end_date = datetime.datetime.now()
    start_date = end_date.replace(day=1)
    return f'{start_date.strftime('%d.%m.%Y')} - {end_date.strftime('%d.%m.%Y')}'


def greeting():
    """Функция выводит приветствие, в зависимости от времени суток"""
    date_now = datetime.datetime.now()
    if date_now.hour >= 0 and date_now.hour <= 5:
        greet = 'Доброй ночи'
    elif date_now.hour >= 6 and date_now.hour <= 11:
        greet = 'Доброе утро'
    elif date_now.hour >= 12 and date_now.hour <= 18:
        greet = 'Добрый день'
    elif date_now.hour >= 19 and date_now.hour <= 23:
        greet = 'Добрый вечер'
    return greet







if __name__ == "__main__":
    print(greeting())

