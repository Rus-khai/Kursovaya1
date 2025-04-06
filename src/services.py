import re


def search_description(list_transaction_dict, str_search):
    """
    функция принимает список словарей с данными о банковских операциях и строку поиска,
    а возвращает список словарей, у которых в описании есть данная строка
    """
    result_list_transaction = []
    pattern = re.compile(str_search)
    try:
        for transaction in list_transaction_dict:
            result = re.search(pattern, transaction.get('description').lower())
            if result:
                result_list_transaction.append(transaction)
    except Exception as e:
        result_list_transaction = f'Ошибка {e}'
    finally:
        if result_list_transaction:
            return result_list_transaction
        return 'Операции не найдены'