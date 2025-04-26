import json
import logging
import os
import pandas as pd
from dotenv import load_dotenv

from config import LOGS_DIR, DATA_DIR
from src.utils import card_filtering, currency_rate,  stock_prices, top_5_transaction
from src.views import main_page

# import pandas as pd


log_file = os.path.join(LOGS_DIR, 'main.log')
#

logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(log_file, encoding='utf-8', mode='w')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


if __name__== "__main__":
    print(main_page("2021-12-31 15:30:00"))







# # сервис
# transactions_path = os.path.join(DATA_DIR, 'operations.xlsx')
# transactions = pd.read_excel(transactions_path)
# transactions_for_service = reader_data_excel.to_dict(orient='records') # получили список словарей из таблицы
#
# word_to_search = input('Введите строку для поиска') # взяли слово для поиска
# result = simple_search(word_to_search, transactions_for_service) # вызывая уже отдаём. Функция принимает запрос для поиска и транакции в формате списка словарей
# print(result)