import datetime
from unittest.mock import patch

import pandas as pd

from src.utils import get_date_time, get_filtered_by_date_range, top_5_transaction, currency_rate, stock_prices


def test_get_date_time():
    assert get_date_time("2021-12-31 16:00:00") == ["01.12.2021 16:00:00", "31.12.2021 16:00:00"]


def test_get_filtered_by_date_range(df_transaction, get_period_time):
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
        }
    ]
    r = get_filtered_by_date_range(df_transaction, get_period_time).reset_index(drop=True).to_dict()
    r_2 = pd.DataFrame(result)
    r_2["Дата операции"] = pd.to_datetime(r_2["Дата операции"], dayfirst=True)
    r_2 = r_2.reset_index(drop=True).to_dict()
    assert r == r_2


def test_top_5_transaction(df_transaction, json_transactions):
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
    assert top_5_transaction(df_transaction) == result


@patch('requests.get')
def test_currency_rate(mock_get_1, read_data):
    mock_lict = [
        {'success': True, 'query': {'from': 'USD', 'to': 'RUB', 'amount': 1},
         'info': {'timestamp': 1738744983, 'rate': 98.954297}, 'date': '2025-02-05', 'historical': True,
         'result': 98.954297}
    ]
    mock_get_1.return_value.json.return_value = mock_lict[0]
    assert currency_rate(read_data) == [{'currency': 'USD', 'rate': 98.95}, {'currency': 'EUR', 'rate': 98.95}]


@patch('requests.get')
def test_stock_prices(mock_get_1, read_data):
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
    assert stock_prices(read_data) == [
        {'stock': 'AAPL', 'price': 247.04},
        {'stock': 'AMZN', 'price': 247.04},
        {'stock': 'GOOGL', 'price': 247.04},
        {'stock': 'MSFT', 'price': 247.04},
        {'stock': 'TSLA', 'price': 247.04}]
