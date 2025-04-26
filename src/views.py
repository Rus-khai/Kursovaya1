import datetime
import logging
import os
import json
import pandas as pd
from src.utils import time_of_the_day, get_date_time, get_filtered_by_date_range, get_cards, filter_by_cards, card_filtering
from dotenv import load_dotenv
from config import LOGS_DIR, DATA_DIR

log_file = os.path.join(LOGS_DIR, 'views.log')
logger = logging.getLogger('views')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(log_file, encoding='utf-8', mode='w')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

try:
    logger.info("Получение фрейма данных из файла Excel с данными транзакции")
    load_dotenv('.env')
    file_path = os.path.join(DATA_DIR, 'operations.xlsx')
    # user_settings = os.path.join(DATA_DIR, 'user_settings.json')
except Exception as e:
    logger.error(f"Ошибка:{e}")

def main_page(date_input):
    """ Функция для страницы 'Главная'.
        Принимающую на вход строку с датой и временем в формате YYYY-MM-DD HH:MM:SS.
        Возвращает JSON-ответ со следующими данными

        1. Приветствие в формате "???",
        где ??? — «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи» в зависимости от текущего времени.
        2. По каждой карте:
            -последние 4 цифры карты;
            -общая сумма расходов;
            -кешбэк.
        3. Топ-5 транзакций по сумме платежа.
        4. Курс валют, согласно файла user_settings.
        5. Стоимость акций, согласно файла user_settings."""



    logger.info('Установка времени суток для приветствия')
    logger.info('Получения приветствия в зависимости от времени дня')

    data = pd.read_excel(file_path)
    greeting = time_of_the_day()
    time_period = get_date_time(date_input)
    filtered_by_date_range = get_filtered_by_date_range(date_input, time_period)
    cards_filter = filter_by_cards(filtered_by_date_range)
    cards = card_filtering(filtered_by_date_range, cards_filter)







    # logger.info('Идет считывание excel.file и выводит список словарей с транзакциями, отфильтрованный по дате')
    # cards_result = card_filtering(read_transaction(date_input), cards(read_transaction(date_input)))
    # logger.info('Фильтрация Топ-5 транзакций по сумме платежа')
    # top_transactions = top_5_transaction(read_transaction(date_input))
    # logger.info('Мы получаем обменные курсы в соответствии с файлом user_settings')
    # result_currency_rate = currency_rate()
    # logger.info('Мы получаем цену акции в соответствии с файлом user_settings')
    # stock_price = stock_prices()
    result = {
        "greeting": greeting,
        "cards": cards,
    }
    return json.dumps(result, ensure_ascii=False, indent=4)

        # "cards": cards_result,
        # "top_transactions": top_transactions,
        # "currency_rates": result_currency_rate,
        # "stock_prices": stock_price