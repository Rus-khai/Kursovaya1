import json
import os
from unittest import mock

from config import DATA_DIR
from src.services import simple_search

file_path = os.path.join(DATA_DIR, 'operations_test.xlsx')


@mock.patch('pandas.DataFrame.to_dict')
def test_simple_search(mock_get, json_transactions):
    mock_get.return_value = json_transactions
    result = [
        {
            "Дата операции": "05.01.2018 14:58:38",
            "Дата платежа": "07.01.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -120.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -120.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": None,
            "Категория": "Цветы",
            "MCC": 5992.0,
            "Описание": "Magazin  Prestizh",
            "Бонусы (включая кэшбэк)": 2,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 120.0
        }
    ]

    assert simple_search('Цветы') == json.dumps(result, ensure_ascii=False, indent=4)
