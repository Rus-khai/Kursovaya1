import datetime
import logging
import os

import pandas as pd
import requests
from dotenv import load_dotenv
from pandas.core.interchange.dataframe_protocol import DataFrame

from config import DATA_DIR, LOGS_DIR

log_file = os.path.join(LOGS_DIR, 'utils.log')
file_path_excel = os.path.join(DATA_DIR, 'operations.xlsx')

load_dotenv('.env')

logger = logging.getLogger('utils')
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


def get_date_time(date_input: str, date_format: str = "%Y-%m-%d %H:%M:%S") -> list[str]:
    """ Функция получает дату, и возвращает список от начала месяца до даты полученная пользователем"""
    logger.info("get_date_time:Перевод DataFrame в формат datetime")
    dt = datetime.datetime.strptime(date_input, date_format)
    start_of_month = dt.replace(day=1)
    result = [start_of_month.strftime("%d.%m.%Y %H:%M:%S"), dt.strftime("%d.%m.%Y %H:%M:%S")]
    logger.info("get_date_time:Вывод список дат")
    return result


def get_filtered_by_date_range(df, period_time: list) -> DataFrame:
    """ Функция принимает DataFrame и период времени,
    и возвращает отфильтрованный DataFrame транзакций в этом интервале времени """

    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    start_date = datetime.datetime.strptime(period_time[0], "%d.%m.%Y %H:%M:%S")
    finish_date = datetime.datetime.strptime(period_time[1], "%d.%m.%Y %H:%M:%S")

    filter_df = df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= finish_date)]
    return filter_df


def filter_by_cards(filter_df: DataFrame) -> list:
    """ Функция принимает отфильтрованный DataFrame по датам, и возвращает список карт"""
    card_list = []

    card_sorted = filter_df[["Номер карты"]]

    for index, row in card_sorted.iterrows():
        if str(row.get('Номер карты')) != 'nan':
            if row.get('Номер карты') not in card_list:
                card_list.append(row.get('Номер карты'))
        else:
            continue
    return card_list


def card_filtering(filter_df: DataFrame, cards: list) -> list[dict]:
    """ Функция принимает DataFrame и список карт, которые есть у пользователя.
        Возвращает список словарей с данными по каждой карте
        - последние 4 цифры номера карты
        - расход по данной карте
        - кешбэк по данной карте. """
    logger.info("card_filtering:Создаётся список номера карт")
    result_dict_list = []
    card_sorted = filter_df[
        [
            "Номер карты",
            "Сумма операции",
            "Кэшбэк"
        ]
    ]
    for card in cards:
        count = 0
        cashback = 0

        for index, row in card_sorted.iterrows():
            if row.get('Номер карты') == card:
                if float(row.get('Сумма операции')) <= 0:
                    count += row.get('Сумма операции')
                if row.get('Кэшбэк'):
                    cashback_data = str(row.get('Кэшбэк'))
                    if cashback_data != 'nan':
                        cashback += int(row.get('Кэшбэк'))

        dict_filter_card = {"last_digits": str(card)[1:],
                            "total_spent": round(count, 2),
                            "cashback": cashback
                            }
        result_dict_list.append(dict_filter_card)
    logger.info("card_filtering:добавление транзакций и результирующий список")
    return result_dict_list


def top_5_transaction(df: DataFrame, direction=True) -> list[dict]:
    """ Функция принимает DataFrame с транзакциями, фильтрует его по сумме операции.
        Возвращает список словарей с пятью наибольшими тратами, содержащими данные:
        -дату операции,
        -сумму операции,
        -категорию операции,
        -описание операции. """
    logger.info("top_5_transaction:Создаётся список")
    result_dict_transaction = []
    transaction = df.to_dict(orient='records')
    logger.info("top_5_transaction:Идёт сортировка от наибольших трат к наименьшему")
    result_sorted = sorted(transaction, key=lambda k: k.get("Сумма операции"), reverse=direction)

    for transaction in result_sorted[:5]:

        dict_transaction = {
            "date": str(transaction.get('Дата операции')),
            "amount": transaction.get('Сумма операции'),
            "category": transaction.get('Категория'),
            "description": transaction.get('Описание')
        }

        result_dict_transaction.append(dict_transaction)
    logger.info("top_5_transaction:добавление транзакций и результирующий список")
    return result_dict_transaction


def currency_rate(data_json):
    """ Функция возвращает список со словарями курса валют имеющихся в файле 'user_settings'
        Для курса валюты используется Exchange Rates Data API: https://apilayer.com/exchangerates_data-api."""
    logger.info("currency_rate:открытие и чтение файла")

    load_dotenv()
    api_key = os.getenv('API_KEY')

    logger.info("currency_rate:Создание результирующего списка")
    result_list = []
    logger.info("currency_rate:Идёт процесс получение данных о курсе рубля")
    if data_json.get('user_currencies'):
        for currency in data_json.get('user_currencies'):
            url = (f'https://api.apilayer.com/exchangerates_data/convert?'
                   f'to=RUB&from={currency}&amount=1')
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


def stock_prices(data_json):
    """Функция возвращает список со словарями цен на акции имеющихся в файле 'user_settings'
        Для получения цен используется Share Price Data API: https://api.marketstack.com."""
    logger.info("stock_prices:открытие и чтение файла")

    load_dotenv()
    api_key = os.getenv('API_KEY_MARKSTACK')
    logger.info("stock_prices:Создание результирующего списка")
    result_list = []
    logger.info("stock_prices:Идёт процесс получение цен")
    if data_json.get('user_stocks'):
        for data in data_json.get('user_stocks'):
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
