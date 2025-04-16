from src.utils import read_transaction
from unittest.mock import patch

from src.utils import currency_rate, stock_prices


# def test_read_transaction(df_transactions):
#     try_func = read_transaction('2018-01-02 04:07:25', df_transactions)
#     df_list = [
#         {
#             "Дата операции": "01.01.2018 20:27:51",
#             "Дата платежа": "04.01.2018",
#             "Номер карты": "*7197",
#             "Статус": "OK",
#             "Сумма операции": -316.0,
#             "Валюта операции": "RUB",
#             "Сумма платежа": -316.0,
#             "Валюта платежа": "RUB",
#             "Кэшбэк": None,
#             "Категория": "Красота",
#             "MCC": 5977.0,
#             "Описание": "OOO Balid",
#             "Бонусы (включая кэшбэк)": 6,
#             "Округление на инвесткопилку": 0,
#             "Сумма операции с округлением": 316.0
#         },
#         {
#             "Дата операции": "01.01.2018 12:49:53",
#             "Дата платежа": "01.01.2018",
#             "Номер карты": None,
#             "Статус": "OK",
#             "Сумма операции": -3000.0,
#             "Валюта операции": "RUB",
#             "Сумма платежа": -3000.0,
#             "Валюта платежа": "RUB",
#             "Кэшбэк": None,
#             "Категория": "Переводы",
#             "MCC": 2.3,
#             "Описание": "Линзомат ТЦ Юность",
#             "Бонусы (включая кэшбэк)": 0,
#             "Округление на инвесткопилку": 0,
#             "Сумма операции с округлением": 3000.0
#         }
#     ]
#     #result = try_func.to_dict(orient='records')
#     assert df_list == try_func
#
#

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