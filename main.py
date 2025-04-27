import logging
import os

import pandas as pd

from config import DATA_DIR, LOGS_DIR
from src.reports import spending_by_category
from src.services import simple_search
from src.views import main_page

file_path = os.path.join(DATA_DIR, 'operations.xlsx')

log_file = os.path.join(LOGS_DIR, 'main.log')


logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(log_file, encoding='utf-8', mode='w')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


if __name__ == "__main__":

    logger.info("Идёт проверка модуля views.py")
    print(main_page("2021-12-31 15:30:00"))

    logger.info("Идёт проверка модуля services.py")
    transactions_path = os.path.join(DATA_DIR, 'operations.xlsx')
    transactions = pd.read_excel(transactions_path)
    transactions_for_service = transactions.to_dict(orient='records')

    word_to_search = input('Введите строку для поиска')  # взяли слово для поиска
    result = simple_search(word_to_search, transactions_for_service)  # Функция принимает запрос для поиска
    # и транзакции в формате списка словарей
    print(result)

    logger.info("Идёт проверка модуля reports.py")
    data = pd.read_excel(file_path)
    print(spending_by_category(data, "Супермаркеты", "2021-12-31"))
