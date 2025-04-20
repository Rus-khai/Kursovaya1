import datetime
import os
import logging

from config import LOGS_DIR

log_file = os.path.join(LOGS_DIR, 'views.log')
logger = logging.getLogger('views')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(log_file, encoding='utf-8', mode='w')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def getting_the_current_time():
    """ Функция подучает текущий час времени """
    logger.info("getting_the_current_time:Получение текущего времени")
    current_date_time = datetime.datetime.now()
    return current_date_time


def time_of_the_day():
    """Функция определяет время суток: утро, день, вечер или ночь"""
    logger.info("time_of_the_day:Начался процесс определения времени суток")

    if 4 <= getting_the_current_time().hour <= 11:
        return 'Доброе утро'
    elif 12 <= getting_the_current_time().hour <= 16:
        return 'Добрый день'
    elif 17 <= getting_the_current_time().hour <= 23:
        return 'Добрый вечер'
    elif 0 <= getting_the_current_time().hour <= 3:
        return 'Доброй ночи'
