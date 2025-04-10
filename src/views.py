import datetime


def getting_the_current_time():
    """ Функция подучает текущий час времени """
    current_date_time = datetime.datetime.now()
    return current_date_time


def time_of_the_day():
    """Функция определяет время суток: утро, день, вечер или ночь"""
    if 4 <= getting_the_current_time().hour <= 11:
        return 'Доброе утро'
    elif 12 <= getting_the_current_time().hour <= 16:
        return 'Добрый день'
    elif 17 <= getting_the_current_time().hour <= 23:
        return 'Добрый вечер'
    elif 0 <= getting_the_current_time().hour <= 3:
        return 'Доброй ночи'

