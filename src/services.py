import json
import os

import pandas as pd
from dotenv import load_dotenv

from config import DATA_DIR


def simple_search():
    """
    функция принимает список словарей с данными о банковских операциях и строку поиска,
    а возвращает список словарей, у которых в описании есть данная строка
    """
    load_dotenv('.env')
    file_path = os.path.join(DATA_DIR, 'operations.xlsx')
    str_search = str(input("Введите строку для поиска:"))
    reader_data_excel = pd.read_excel(file_path)
    result_transaction = reader_data_excel.to_dict(orient='records')
    result_list_transaction = []

    try:
        for transaction in result_transaction:
            if (str(transaction.get('Описание')).lower() == str_search.lower()
                    or str(transaction.get('Категория')).lower() == str_search.lower()):
                result_list_transaction.append(transaction)
    except Exception as e:
        result_list_transaction = f'Ошибка {e}'
    finally:
        if result_list_transaction:
            print(result_list_transaction)
            final = json.dumps(result_list_transaction, ensure_ascii=False, indent=4)
            return final
        return 'Операции не найдены'
