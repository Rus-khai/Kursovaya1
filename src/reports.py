import datetime
import logging
import os.path
from functools import wraps
from typing import Optional
from config import LOGS_DIR, PATH_REPORT
import pandas as pd

log_file = os.path.join(LOGS_DIR, 'reports.log')

logger = logging.getLogger('reports')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(log_file, encoding='utf-8', mode='w')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def report_to_file(file_name: str = "default_report.xlsx"):
    """ Декоратор позволяющий записывать отчеты в файл формата *xlsx.
    Файл по умолчанию - default_report.xlsx
    Все отчеты сохраняются в директории reports/"""
    def inner(func):
        @wraps
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            patch_to_report = os.path.join(PATH_REPORT, file_name)
            result.to_excel(patch_to_report, index=False)
            logger.info(f"Отчет записан в файл: {patch_to_report}")
            return result
        return wrapper
    return inner

def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> list[dict]:
    """Функция принимает DataFrame, название категории и опционально дату в формате YYYY-MM-DD.
    Возвращает список словарей с транзакциями по заданной категории за последние три месяца (от переданной даты)"""
    logger.info("Идёт проверка, введена ли дата, если нет, то будет назначена текущая дата.")
    if not date:
        date = datetime.datetime.now()

    transactions_dicts = transactions.to_dict(orient='records')

    logger.info("Создаётся список расходов за последние три месяца (с даты отправки)")
    result_list = []
    for transaction in transactions_dicts:
        transaction_date = transaction.get('Дата операции')

        date_transaction = datetime.datetime.strptime(transaction_date, "%d.%m.%Y %H:%M:%S").date()
        date_1 = datetime.datetime.strptime(date, "%Y-%m-%d").date()

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
    logger.info("Программа завершает работу и выдает результат")

    return result_list


# if __name__ == '__main__':
#     CURRENT_DIR = os.path.dirname(__file__)
#     DATA_DIR = os.path.join(CURRENT_DIR, '..', 'data')
#     FILE_DIR = os.path.join(DATA_DIR, 'operations.xlsx')
#     a = pd.read_excel(FILE_DIR)
#     print(spending_by_category(a, 'Супермаркеты', '2021-02-12'))
