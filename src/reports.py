import datetime
# import json
# import logging
# import os.path
from typing import Optional

import pandas as pd


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> list[dict]:
    """Функция принимает DataFrame, название категории и опционально дату в формате YYYY-MM-DD.
    Возвращает список словарей с транзакциями по заданной категории за последние три месяца (от переданной даты)"""

    if not date:
        date = datetime.datetime.now()

    transactions_dicts = transactions.to_dict(orient='records')
    result_list = []
    for transaction in transactions_dicts:
        transaction_date = transaction.get('Дата операции')

        date_transaction = datetime.datetime.strptime(transaction_date, "%d.%m.%Y %H:%M:%S").date()
        date_1 = datetime.datetime.strptime(date, "%d.%m.%Y").date()

        if (transaction.get('Категория') == category and transaction.get('Статус') == 'OK'
                and transaction.get('Сумма операции') < 0):

            if date_1.month > 2:
                if (int(date_transaction.year) == int(date_1.year) and int(date_transaction.month) == date_1.month
                        and int(date_transaction.day) <= int(date_1.day)):
                    result_list.append(transaction)
                if int(date_transaction.year) == int(date_1.year) and int(date_transaction.month) == date_1.month - 1:
                    result_list.append(transaction)
                if (int(date_transaction.year) == int(date_1.year) - 1
                        and int(date_transaction.month) == date_1.month - 2):
                    result_list.append(transaction)
                if (int(date_transaction.year) == int(date_1.year) - 1
                        and int(date_transaction.month) == date_1.month - 3
                        and int(date_transaction.day) >= int(date_1.day)):
                    result_list.append(transaction)

            if date_1.month == 2:
                if (int(date_transaction.year) == int(date_1.year) and int(date_transaction.month) == date_1.month
                        and int(date_transaction.day) <= int(date_1.day)):
                    result_list.append(transaction)
                if int(date_transaction.year) == int(date_1.year) and int(date_transaction.month) == date_1.month - 1:
                    result_list.append(transaction)
                if int(date_transaction.year) == int(date_1.year) - 1 and int(date_transaction.month) == 12:
                    result_list.append(transaction)
                if (int(date_transaction.year) == int(date_1.year) - 1 and int(date_transaction.month) == 11
                        and int(date_transaction.day) >= int(date_1.day)):
                    result_list.append(transaction)

            if date_1.month == 1:
                if (int(date_transaction.year) == int(date_1.year) and int(date_transaction.month) == date_1.month
                        and int(date_transaction.day) <= int(date_1.day)):
                    result_list.append(transaction)
                if int(date_transaction.year) == int(date_1.year) - 1 and int(date_transaction.month) == 12:
                    result_list.append(transaction)
                if (int(date_transaction.year) == int(date_1.year) - 1 and int(date_transaction.month) == 11
                        and int(date_transaction.day) >= int(date_1.day)):
                    result_list.append(transaction)
                if (int(date_transaction.year) == int(date_1.year) - 1 and int(date_transaction.month) == 10
                        and int(date_transaction.day) >= int(date_1.day)):
                    result_list.append(transaction)

    return result_list

# if __name__ == '__main__':
#     CURRENT_DIR = os.path.dirname(__file__)
#     DATA_DIR = os.path.join(CURRENT_DIR, '..', 'data')
#     FILE_DIR = os.path.join(DATA_DIR, 'operations.xlsx')
#     a = pd.read_excel(FILE_DIR)
#     print(spending_by_category(a, 'Супермаркеты', '12.02.2021'))
