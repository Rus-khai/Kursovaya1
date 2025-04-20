from unittest import mock
from unittest.mock import patch
from src.utils import currency_rate
from src.utils import read_transaction, cards, top_5_transaction, stock_prices


@mock.patch('pandas.DataFrame.to_dict')
def test_read_transaction(mock_get, json_transactions):
    mock_get.return_value = json_transactions
    result = [
        {
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


def test_get_cards(get_data_1):
    assert cards(get_data_1) == [None, '*5441', '*7197', '*4556']


def test_top_5_transaction(get_data_1):
    result = [
        {
            "date": "10.01.2018 13:00:04",
            "amount": 30000.0,
            "category": "Пополнения",
            "description": "Перевод с карты"
        },
        {
            "date": "10.01.2018 12:59:23",
            "amount": 30000.0,
            "category": "Пополнения",
            "description": "Перевод с карты"
        },
        {
            "date": "05.01.2018 15:28:22",
            "amount": -79.6,
            "category": "Супермаркеты",
            "description": "Пятёрочка"
        },
        {
            "date": "05.01.2018 14:58:38",
            "amount": -120.0,
            "category": "Цветы",
            "description": "Magazin  Prestizh"
        },
        {
            "date": "08.01.2018 14:21:23",
            "amount": -250.0,
            "category": "Связь",
            "description": "МТС"
        }

    ]
    assert top_5_transaction(get_data_1) == result


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
    mock_lict = {
        "pagination": {
            "limit": 100,
            "offset": 0,
            "count": 100,
            "total": 100
        },
        "data": [
            {
                "open": 248.0,
                "high": 249.98,
                "low": 244.91,
                "close": 247.04,
                "volume": 46872348.0,
                "adj_high": 250.0,
                "adj_low": 244.91,
                "adj_close": 247.04,
                "adj_open": 248.0,
                "adj_volume": 47275651.0,
                "split_factor": 1.0,
                "dividend": 0.0,
                "symbol": "AAPL",
                "exchange": "XNAS",
                "date": "2025-02-25T00:00:00+0000"
            }
        ]
    }
    mock_get_1.return_value.json.return_value = mock_lict
    assert stock_prices() == [
        {'stock': 'AAPL', 'price': 247.04},
        {'stock': 'AMZN', 'price': 247.04},
        {'stock': 'GOOGL', 'price': 247.04},
        {'stock': 'MSFT', 'price': 247.04},
        {'stock': 'TSLA', 'price': 247.04}]
