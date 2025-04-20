import freezegun
from src.views import time_of_the_day


def test_time_of_the_day():
    with freezegun.freeze_time("2025-02-25 06:35:50.032596"):
        assert time_of_the_day() == 'Доброе утро'


def test_time_of_day_try_evening():
    with freezegun.freeze_time("2025-02-25 18:35:50.032596"):
        assert time_of_the_day() == 'Добрый вечер'


def test_time_of_day_try_day():
    with freezegun.freeze_time("2025-02-25 14:35:50.032596"):
        assert time_of_the_day() == 'Добрый день'


def test_time_of_day_try_night():
    with freezegun.freeze_time("2025-02-25 03:35:50.032596"):
        assert time_of_the_day() == 'Доброй ночи'
