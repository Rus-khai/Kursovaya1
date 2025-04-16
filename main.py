import json
import logging
import os
# import pandas as pd

from dotenv import load_dotenv
from config import LOGS_DIR
from src.utils import card_filtering, cards, currency_rate, read_transaction, stock_prices, top_5_transaction
from src.views import time_of_the_day

log_file = os.path.join(LOGS_DIR, 'main.log')
#

logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(log_file, encoding='utf-8', mode='w')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def main_page():
    """ Функция для страницы 'Главная'.
        Принимающую на вход строку с датой и временем в формате YYYY-MM-DD HH:MM:SS.
        Возвращает JSON-ответ со следующими данными:
        1. Приветствие в формате "???",
        где ??? — «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи» в зависимости от текущего времени.
        2. По каждой карте:
            -последние 4 цифры карты;
            -общая сумма расходов;
            -кешбэк.
        3. Топ-5 транзакций по сумме платежа.
        4. Курс валют, согласно файла user_settings.
        5. Стоимость акций, согласно файла user_settings."""

    try:
        logger.info("Получение фрейма данных из файла Excel с данными транзакции")
        load_dotenv('.env')
        # file_path_excel = os.path.join(DATA_DIR, 'operations.xlsx')
        # user_settings = os.path.join(DATA_DIR, 'user_settings.json')
    except Exception as e:
        logger.error(f"Ошибка:{e}")

    logger.info('Установка времени суток для приветствия')
    date_input = input('Введите дату в формате: YYYY-MM-DD HH:MM:SS:')
    logger.info('Получения приветствия в зависимости от времени дня')
    greeting = time_of_the_day()
    logger.info('Идет считывание excel.file и выводит список словарей с транзакциями, отфильтрованный по дате')
    cards_result = card_filtering(read_transaction(date_input), cards(read_transaction(date_input)))
    logger.info('Фильтрация Топ-5 транзакций по сумме платежа')
    top_transactions = top_5_transaction(read_transaction(date_input))
    logger.info('Мы получаем обменные курсы в соответствии с файлом user_settings')
    result_currency_rate = currency_rate()
    logger.info('Мы получаем цену акции в соответствии с файлом user_settings')
    stock_price = stock_prices()
    result = {
        "greeting": greeting,
        "cards": cards_result,
        "top_transactions": top_transactions,
        "currency_rates": result_currency_rate,
        "stock_prices": stock_price
    }
    return json.dumps(result, ensure_ascii=False, indent=4)


print(main_page())
