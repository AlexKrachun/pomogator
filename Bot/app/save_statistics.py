import os
import csv
from datetime import datetime


fieldnames = [
    'user_bd_id', 'user_tg_id', 'succeed', 'date', 'model',
    'cost_for_user_in_fantiks', 'cost_for_us_in_usd',
    'sent_to_input_size_tok', 'answer_size_tok', 'daily_candy',
    'daily_candy_left', 'paid_candy_left', 'answer_time',
]


def save_statistics(statistics: dict):

    statistics['date'] = datetime.now().strftime("%Y-%m-%d %H:%M")

    file_path = 'statistics.csv'
    file_exists = os.path.exists(file_path)

    with open(file_path, 'a', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='\t')

        if not file_exists:
            writer.writeheader()

        # Записываем строку — приведение datetime к строке
        writer.writerow(statistics)


# statistics = {
#     'user_bd_id': 123,
#     'user_tg_id': 999,
#     'succeed': True,
#     'date': datetime.now(),
#     'model': 'gpt-4',
#     'cost_for_user_in_fantiks': 15,
#     'cost_for_us_in_usd': 0.02,
#     'sent_to_input_size_tok': 10,
#     'answer_size_tok': 50,
#     'daily_candy': 10,
#     'daily_candy_left': 10,
#     'paid_candy_left': 10,
#     'answer_time': 10

# }

# save_statistics(statistics)

'''
все хендлеры возвращают
statistics = {
# for required all
    'user_bd_id': int,
    'user_tg_id': int,
    'succeed': bool,  # успешно ли обработался запрос в нейросеть
    'model': str,  # текстовое наименование модели
    'daily_candy': int,   # сколько у челика фантиков в день
    'daily_candy_left': int,  # сколько у челика осталось фантиков на сегодня
    'paid_candy_left': int,  # сколько у челика осталось штучно купленных фантиков
    'answer_time': float, # время обработки запроса в секундах



# whenever possible or None
    'cost_for_user_in_fantiks': int  # сколько фантиков пользователь потратил за запрос
    'cost_for_us_in_usd': float  # сколько мы потратили на запрос $

    'sent_to_input_size_tok': int | None
   # размер отправленного нами в input api запроса (пропмт + история) в токенах
    'answer_size_tok': int | None
  # размер полученного от модели ответа в токенах
}



# Penis
'''
