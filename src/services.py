import json
import logging
import os

from dotenv import load_dotenv

from config import LOGS_DIR


def simple_search(str_search, transactions):
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
    logger.info("Создание результирующего списка")
    result_list_transaction = []
    logger.info("Идёт поиск по введенным данным")
    try:
        for transaction in transactions:
            if (str_search.lower() in str(transaction.get('Описание', '')).lower()
                    or str_search.lower() in str(transaction.get('Категория', '')).lower()):
                result_list_transaction.append(transaction)
    except Exception as e:
        result_list_transaction = f'Ошибка {e}'
    finally:
        if result_list_transaction:
            final = json.dumps(result_list_transaction, ensure_ascii=False, indent=4)
            return final
        return 'Операции не найдены'
