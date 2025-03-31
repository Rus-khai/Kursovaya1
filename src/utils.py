import datetime
import os
from turtle import pd

import pandas as pd

from config import DATA_DIR

file_path_excel = os.path.join(DATA_DIR, 'operations.xlsx')

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
    #print(result_transaction)
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
    cards = []
    for transaction in filter_list_transaction:
        if transaction.get('Номер карты') not in cards:
            cards.append(transaction.get('Номер карты'))
        else:
            continue
    return cards

def filter(filter_list_transaction, list_cards):
    count = 0
    for card in list_cards:
        for transaction in filter_list_transaction:
            if transaction.get('Номер карты') == card:
                if float(transaction.get('Сумма операции')) <= 0:
                    count =+ float(transaction.get('Сумма операции'))

        dict = {"last_digits": card,
                "total_spent": count,
                "cashback": 0
                }
        print(dict)

print(filter(read_transaction_excel(file_path_excel), cards(read_transaction_excel())))
