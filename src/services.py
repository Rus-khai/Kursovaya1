import json
import os
import pandas as pd
import logging
from dotenv import load_dotenv
from config import DATA_DIR, LOGS_DIR


def simple_search(str_search):
    """ Функция принимает список словарей с данными о банковских операциях и строку поиска,
    а возвращает список словарей, у которых в описании есть данная строка. """

    log_file = os.path.join(LOGS_DIR, 'services.log')

    logger = logging.getLogger('services')
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(log_file, encoding='utf-8', mode='w')
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    load_dotenv('.env')
    file_path = os.path.join(DATA_DIR, 'operations.xlsx')
    logger.info("Получение строки для поиска")

    logger.info("Открытие файла")
    reader_data_excel = pd.read_excel(file_path)
    result_transaction = reader_data_excel.to_dict(orient='records')
    logger.info("Создание результирующего списка")
    result_list_transaction = []
    logger.info("Идёт поиск по введенным данным")
    try:
        for transaction in result_transaction:
            if (str(transaction.get('Описание')).lower() == str_search.lower()
                    or str(transaction.get('Категория')).lower() == str_search.lower()):
                result_list_transaction.append(transaction)
    except Exception as e:
        result_list_transaction = f'Ошибка {e}'
    finally:
        if result_list_transaction:
            # print(result_list_transaction)
            final = json.dumps(result_list_transaction, ensure_ascii=False, indent=4)
            return final
        return 'Операции не найдены'


# print(simple_search())
