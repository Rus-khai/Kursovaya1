from unittest import mock
from unittest.mock import patch

from src.utils import currency_rate
from src.utils import read_transaction

@mock.patch('pandas.DataFrame.to_dict')
def test_read_transaction(mock_get, json_transactions):
    mock_get.return_value = json_transactions
    result = [{
            "Дата операции": "05.01.2018 15:28:22",
            "Дата платежа": "07.01.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -79.6,
            "Валюта операции": "RUB",
            "Сумма платежа": -79.6,
            "Валюта платежа": "RUB",
            "Кэшбэк": None,
            "Категория": "Супермаркеты",
            "MCC": 5411.0,
            "Описание": "Пятёрочка",
            "Бонусы (включая кэшбэк)": 1,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 79.6
        },
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
        }]

    assert read_transaction('2018-01-06 15:28:22') == result






@patch('requests.get')
def test_currency_rate(mock_get_1):
    mock_lict = [
        {'success': True, 'query': {'from': 'USD', 'to': 'RUB', 'amount': 1},
         'info': {'timestamp': 1738744983, 'rate': 98.954297}, 'date': '2025-02-05', 'historical': True,
         'result': 98.954297}
    ]
    mock_get_1.return_value.json.return_value = mock_lict[0]
    assert currency_rate() == [{'currency': 'USD', 'rate': 98.95}, {'currency': 'EUR', 'rate': 98.95}]


@patch('requests.get')
def test_stock_prices(mock_get_1):
    mock_lict = {}