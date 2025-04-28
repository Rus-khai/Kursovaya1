import datetime
import logging
import os.path
from functools import wraps
from typing import Optional

import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame

from config import LOGS_DIR, PATH_REPORT

log_file = os.path.join(LOGS_DIR, 'reports.log')

logger = logging.getLogger('reports')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(log_file, encoding='utf-8', mode='w')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def report_to_file(file_name: str = "default_report.xlsx"):
    """ Декоратор позволяющий записывать отчеты в файл формата *xlsx.
    Файл по умолчанию - default_report.xlsx
    Все отчеты сохраняются в директории reports/"""
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            path_to_report = os.path.join(PATH_REPORT, file_name)
            result.to_excel(path_to_report, index=False)
            logger.info(f"Отчет записан в файл: {path_to_report}")
            return result
        return wrapper
    return inner


@report_to_file()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> DataFrame:
    """Функция принимает DataFrame, название категории и опционально дату в формате YYYY-MM-DD.
    Возвращает список словарей с транзакциями по заданной категории за последние три месяца (от переданной даты)"""
    logger.info("Идёт проверка, введена ли дата, если нет, то будет назначена текущая дата.")
    if not date:
        end_date = datetime.datetime.now()
    else:
        end_date = datetime.datetime.strptime(date, "%Y-%m-%d")
    start_date = end_date - pd.DateOffset(months=3)

    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format='%d.%m.%Y %H:%M:%S')
    filtered_df_to_date = transactions[(transactions['Дата операции'] >= start_date)
                                       & (transactions['Дата операции'] <= end_date)]
    filter_df_to_category = filtered_df_to_date[filtered_df_to_date["Категория"] == category].copy()
    return filter_df_to_category
