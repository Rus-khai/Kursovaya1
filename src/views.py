from src.utils import getting_the_current_time


def views():
    if 4 <= getting_the_current_time().hour <= 11:
        print('Доброе утро')
    elif 12 <= getting_the_current_time().hour <= 16:
        print('Добрый день')
    elif 17 <= getting_the_current_time().hour <= 23:
        print('Добрый вечер')
    elif 0 <= getting_the_current_time().hour <=3:
        print('Доброй ночи')

print(views())