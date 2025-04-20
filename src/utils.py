import datetime
import json
import os
import logging
import pandas as pd
import requests
from config import LOGS_DIR
from dotenv import load_dotenv


from config import DATA_DIR
log_file = os.path.join(LOGS_DIR, 'utils.log')
file_path_excel = os.path.join(DATA_DIR, 'operations.xlsx')
user_settings = os.path.join(DATA_DIR, 'user_settings.json')
load_dotenv('.env')

logger = logging.getLogger('utils')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(log_file, encoding='utf-8', mode='w')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def read_transaction(date_input, file_path=file_path_excel) -> list[dict]:
    """Функция считывает excel.file и выводит список словарей с транзакциями, отфильтрованный по дате"""
    logger.info("read_transaction:Получение фрейма данных из файла Excel с данными транзакции")
    reader_data_excel = pd.read_excel(file_path)
    result_transaction = reader_data_excel.to_dict(orient='records')
    logger.info("read_transaction:Создаётся список транзакций, которые прошли через фильтрацию")
    result_dict = []
    logger.info("read_transaction:Идёт фильтрация")
    for data_dict in result_transaction:
        # Дата из словаря
        date = data_dict.get('Дата операции')
        date_transaction = datetime.datetime.strptime(date, "%d.%m.%Y %H:%M:%S").date()
        # Дата введенная пользователем
        date_object = datetime.datetime.strptime(date_input, "%Y-%m-%d %H:%M:%S").date()
        if (date_object.year == date_transaction.year
                and date_object.month == date_transaction.month
                and date_object.day >= date_transaction.day):
            if data_dict.get('Статус') == 'OK':
                result_dict.append(data_dict)
    logger.info("read_transaction:добавление транзакций и результирующий словарь")
    return result_dict

# print(read_transaction('2021-12-31 16:44:00'))


def cards(filter_list_transaction: list[dict]) -> list:
    """ Функция принимает отфильтрованный список транзакция, и возвращает список номеров карт"""
    logger.info("cards:Создаётся список номера карт")
    cards_list = []
    for transaction in filter_list_transaction:
        if str(transaction.get('Номер карты')) != 'nan':
            if transaction.get('Номер карты') not in cards_list:
                cards_list.append(transaction.get('Номер карты'))
        else:
            continue
    logger.info("cards:добавление номеров карт в список")
    return cards_list


def card_filtering(filter_list_transaction: list[dict], list_cards: list[dict]) -> list[dict]:
    """ Функция принимает DataFrame и список карт, которые есть у пользователя.
        Возвращает список словарей с данными по каждой карте
        - последние 4 цифры номера карты
        - расход по данной карте
        - кешбэк по данной карте. """
    logger.info("card_filtering:Создаётся список номера карт")
    result_dict_list = []
    for card in list_cards:
        count = 0
        cashback = 0
        for transaction in filter_list_transaction:
            if transaction.get('Номер карты') == card:
                if float(transaction.get('Сумма операции')) <= 0:
                    count += transaction.get('Сумма операции')
                if transaction.get('Кэшбэк'):
                    cashback_data = str(transaction.get('Кэшбэк'))
                    if cashback_data != 'nan':
                        cashback += int(transaction.get('Кэшбэк'))

        dict_filter_card = {"last_digits": str(card)[1:],
                            "total_spent": round(count, 2),
                            "cashback": cashback
                            }
        result_dict_list.append(dict_filter_card)
    logger.info("card_filtering:добавление транзакций и результирующий список")
    return result_dict_list
# print(filter(read_transaction_excel(file_path_excel), cards(read_transaction_excel())))


def top_5_transaction(filter_list_transaction: list[dict], direction=True) -> list[dict]:
    """ Функция принимает DataFrame с транзакциями, фильтрует его по сумме операции.
        Возвращает список словарей с пятью наибольшими тратами, содержащими данные:
        -дату операции,
        -сумму операции,
        -категорию операции,
        -описание операции. """
    logger.info("top_5_transaction:Создаётся список")
    result_dict_transaction = []
    logger.info("top_5_transaction:Идёт сортировка от наибольших трат к наименьшему")
    result_sorted = sorted(filter_list_transaction, key=lambda k: k.get("Сумма операции"), reverse=direction)

    for transaction in result_sorted[:5]:

        dict_transaction = {
            "date": transaction.get('Дата операции'),
            "amount": transaction.get('Сумма операции'),
            "category": transaction.get('Категория'),
            "description": transaction.get('Описание')
        }

        result_dict_transaction.append(dict_transaction)
    logger.info("top_5_transaction:добавление транзакций и результирующий список")
    return result_dict_transaction


def currency_rate():
    """ Функция возвращает список со словарями курса валют имеющихся в файле 'user_settings'
        Для курса валюты используется Exchange Rates Data API: https://apilayer.com/exchangerates_data-api."""
    logger.info("currency_rate:открытие и чтение файла")
    with open(user_settings, 'r', encoding="utf-8") as file:
        read_data = json.load(file)

    load_dotenv()
    api_key = os.getenv('API_KEY')
    date_obj = datetime.datetime.now()
    date_now = date_obj.strftime("%Y-%m-%d")

    logger.info("currency_rate:Создание результирующего списка")
    result_list = []
    logger.info("currency_rate:Идёт процесс получение данных о курсе рубля")
    if read_data.get('user_currencies'):
        for currency in read_data.get('user_currencies'):
            url = (f'https://api.apilayer.com/exchangerates_data/convert?'
                   f'to=RUB&from={currency}&amount=1&date={date_now}')
            headers = {"apikey": api_key}

            response = requests.get(url, headers=headers)
            result = round(response.json().get('result'), 2)
            result_dict = {
                'currency': currency,
                'rate': result
            }
            result_list.append(result_dict)
    logger.info("currency_rate:Добавление полученных данных в результирующий словарь")
    return result_list

# print(currency_rate())


def stock_prices():
    """Функция возвращает список со словарями цен на акции имеющихся в файле 'user_settings'
        Для получения цен используется Share Price Data API: https://api.marketstack.com."""
    logger.info("stock_prices:открытие и чтение файла")
    with open(user_settings, 'r', encoding="utf-8") as file:
        read_data = json.load(file)

    load_dotenv()
    api_key = os.getenv('API_KEY_MARKSTACK')
    logger.info("stock_prices:Создание результирующего списка")
    result_list = []
    logger.info("stock_prices:Идёт процесс получение цен")
    if read_data.get('user_stocks'):
        for data in read_data.get('user_stocks'):
            querystring = {"symbols": {data}}
            responses = requests.get(f"https://api.marketstack.com/v1/eod?access_key={api_key}", params=querystring)
            data_dicts = responses.json().get('data')

            for data_dict in data_dicts:
                result = data_dict.get('close')
                break

            result_dict = {
                "stock": data,
                "price": result
            }
            result_list.append(result_dict)
    logger.info("stock_prices:Добавление полученных данных в результирующий словарь")
    return result_list
