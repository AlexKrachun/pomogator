from Bot.app.consts import candy
from prices import sub_plan_costs, at_login_user_fantiks_amount

message_templates = {
    'en': {
        'start': "Hello, I'm bot powered on API GPT-4(ChatGPT). Enter /info",
        'new_topic': 'Starting a new topic!',
        'image_prompt': 'Please add a description of the image after the /image command. For example, /image Neon City.',
        'image_error': 'An error occurred during image generation:',
        'about': 'This bot is powered by OpenAI GPT-4.',
        'info': 'You can interact with this bot using commands like /start, /newtopic, /image, /about, and /info.',
        'language_confirmation': "Language has been set to English.",
        'language_selection': "Available in 3 languages:",
        'processing': "Your request is being processed, please wait.",
        'error': "An error occurred during processing:",
        'delete_context': "New context has been created",

    },
    'ru': {
        'start': "Привет, я бот с нейросетями. Напишите запроc.\n\nПочитать про функциолан бота и наши нейросети можно в /info",
        'new_topic': 'Начинаем новую тему!',
        'image_prompt': 'Пожалуйста, добавьте описание изображения после команды /image. Например, /image Неоновый город.',
        'image_error': 'Произошла ошибка при генерации изображения:',
        # 'about': 'Этот бот работает на OpenAI GPT-4.',
        'info':
f'''*Помагатор - это агрегатор нейросетей*
*Команды бота:*
/mode - выбор нейросети
/new\_context - перейти в новый пустой чат с языковой моделью
/contexts - посмотреть список контекстов и переключиться на желаемый
/info - вы как раз тут))
/profile - посмотреть личные данные и баланс
/pay - пополнить баланс


Валюта за которую мы оплачиваем запросы в нейросети: {candy}
На старте вам дается {at_login_user_fantiks_amount} {candy}
Вы можете оформить одну из подписок:
- 100 {candy} в неделю за {sub_plan_costs['month: 100/week']}₽ на 4 недели.
- 300 {candy} в неделю за {sub_plan_costs['month: 300/week']}₽ на 4 недели.
- 1000 {candy} в неделю за {sub_plan_costs['month: 1000/week']}₽ на 4 недели.
остаток {candy} за прошлую неделю не схраняется.


у каждой нейросети своя цена за запрос


*Доступные нейросети:*
Для простых задач. Дешевые, глупые:
    🤖 `gpt-4o-mini`
    🤖 `claude 3.5-haiku`
они обе довольно не плохо работают, но если не помогла одна, как правило может помочь другая

Рабочие лошадки. Не дорогие и умные:
    🤖 `gpt-4o`
    🤖 `o3-mini`
    🤖 `gpt-4o-search-preview`

Для сложных задач. Дорогие и очень умные
    🤖 `claude 3.7-sonnet`
    🤖 `o1`
    🤖 `gpt-4.5-preview`

Для рисования картинок:
    🌃 `dall-e-3` - рисует картинку по текстовому описанию

''',
        'language_confirmation': "Язык был изменен на русский",
        'language_selection': "Доступно на 3 языках:",
        'processing': "Ваш запрос обрабатывается, пожалуйста, подождите",
        'error': "Произошла ошибка во время обработки:",
        'contexts': "Пожалуйста, выберите контекст из списка",
        'delete_context': "Новый контекст начат, напишите запрос",
        'id_in_procces': 'Ваш предыдущий запрос еще обрабатывается',
        'dall_e_3_handler': '''*Введите ваш запрос для генерации изображения:*

*Изменяемые параметры генерации:*

*Разрешение:*
ширина×высота
- 1024×1024
- 1024×1792
- 1792×1024

*Детализация:*
- Обычная
- Высокая
''',
        #         'dall_e_3_handler': '''Выберите разрешение и степень детализации
        # изображений, которые генерирует DALL•E 3
        # _Разрешение_: 1024х1024 | 1024х1792 | 1792х1024
        # _Детализация_: обычная | высокая
        # ''',
        #         'face-swap-1': 'Наша программа позволяет легко заменять лица на фотографиях. '
        #                        'Для этого сначала вам потребуется отправить фотографию: "исходник", '
        #                        'фото которое вы хотите изменить.',
        #         'face-swap-2': 'Отправьте фотографию: "замена", '
        #                        'фото, с которого будет взят материал для замены лица.',
        # 'face-swap-1': 'FaceSwap - замена лица на фото.\n\n'
        #                '*Отправьте исходную фотографию🖼*, которую вы хотите изменить.',
        'face-swap-1': '*Отправьте фотографию🖼*, на которой надо изменить лицо.',
        # 'face-swap-2': '*Отправьте фотографию🖼:* `замена`, с которой будет взято лицо для переноса.',

        'face-swap-3': "Первая фотография успешно обработана!\n*Отправьте фотографию🖼*, "
                       "с которой будет взято лицо для переноса.\n\n"
                       "Если вы хотите сбросить исходную фотографию, "
                       "воспользуйтесь командой /start."
    }
}


def get_changed_context_line(s):
    return f'Ваш контекст сменён на тему: {s}.'
