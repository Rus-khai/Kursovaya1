import datetime
import json
import os
import pandas as pd
import requests
from dotenv import load_dotenv


from config import DATA_DIR


load_dotenv('.env')
file_path_excel = os.path.join(DATA_DIR, 'operations.xlsx')
user_settings = os.path.join(DATA_DIR, 'user_settings.json')

def getting_the_current_time():
    """ Функция подучает текущий час времени """
    current_date_time = datetime.datetime.now()
    return current_date_time


def get_input_date_1():

    out_date = input("Введите дату в формате'30.05.2025'")
    print(out_date)
    in_date = str(int(out_date[0:1]) - (int(out_date[0:1]) - 1)) + out_date[2:]
    print(in_date)


def read_transaction_excel(file_path = file_path_excel):
    """Функция считывает excel.file и выводит список словарей с транзакциями, отфильтрованный по дате"""
    reader_data_excel = pd.read_excel(file_path)
    result_transaction = reader_data_excel.to_dict(orient='records')

    result_dict = []
    out_date = input("Введите дату в формате'30.05.2025'")
    for data_dict in result_transaction:
        #Дата из словаря
        date = data_dict.get('Дата операции')
        date_transaction = datetime.datetime.strptime(date, "%d.%m.%Y %H:%M:%S").date()
        #Дата введенная пользователем
        date_object = datetime.datetime.strptime(out_date, "%d.%m.%Y").date()
        if date_object.year == date_transaction.year and date_object.month == date_transaction.month and date_object.day >= date_transaction.day:
            if data_dict.get('Статус') == 'OK':
                result_dict.append(data_dict)

    return result_dict


def cards(filter_list_transaction):
    cards_list = []
    for transaction in filter_list_transaction:
        if str(transaction.get('Номер карты')) != 'nan':
            if transaction.get('Номер карты') not in cards:
                cards_list.append(transaction.get('Номер карты'))
        else:
            continue
    return cards_list


def filter_1(filter_list_transaction, list_cards):

    """ """
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
                "total_spent": round(count,2),
                "cashback": cashback
                }
        result_dict_list.append(dict_filter_card)
    return result_dict_list
#print(filter(read_transaction_excel(file_path_excel), cards(read_transaction_excel())))


def top_5_transaction(filter_list_transaction, direction=True):
    """"""
    result_dict_transaction = []
    result_sorted = sorted(filter_list_transaction, key=lambda k: k.get("Сумма операции"), reverse=direction)

    for  transaction in result_sorted[:5]:
        dict_transaction = {
                "date": transaction.get('Дата операции'),
                "amount": transaction.get('Сумма операции'),
                "category": transaction.get('Категория'),
                "description": transaction.get('Описание')
        }
        result_dict_transaction.append(dict_transaction)
    return result_dict_transaction

# print(top_5_transaction(read_transaction_excel()))

def currency_rate_usd():
    v = "RUB"
    base = "USD"
    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={v}&base={base}"

    payload = {}
    headers = {"apikey": "2JxFXrVuxnS322UdwG6OlktxmkuTcHSs"}

    response = requests.request("GET", url, headers=headers, data=payload)

    # status_code = response.status_code
    result = response.json()
    return result

#print(currency_rate_usd())

def currency_rate_eur():
    v = "RUB"
    base = "EUR"
    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={v}&base={base}"

    payload = {}
    headers = {"apikey": "2JxFXrVuxnS322UdwG6OlktxmkuTcHSs"}

    response = requests.request("GET", url, headers=headers, data=payload)

    # status_code = response.status_code
    result = response.json()
    return result

#print(currency_rate_eur())

def stock_prices():
    """Функция возвращает список со словарями цен на акции имеющихся в файле 'user_settings'
        Для получения цен используется Share Price Data API: https://api.marketstack.com."""


    with open(user_settings,'r', encoding="utf-8") as file:
        read_data = json.load(file)


    load_dotenv()
    api_key = os.getenv('API_KEY_MARKSTACK')

    result_list = []
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
    return result_list

# print(stock_prices())
