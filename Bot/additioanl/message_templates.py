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
        'start': "Привет, я бот с нейросетями. Напишите свой запрос или выведите справку /info",
        'new_topic': 'Начинаем новую тему!',
        'image_prompt': 'Пожалуйста, добавьте описание изображения после команды /image. Например, /image Неоновый город.',
        'image_error': 'Произошла ошибка при генерации изображения:',
        # 'about': 'Этот бот работает на OpenAI GPT-4.',
        'info': '''Вы можете взаимодействовать с этим ботом с помощью команд:
         /profile - посмотреть личные данные в рамках бота
         /new_context - переключиться на новый контекст
         /mode - выбрать подходящую модель gpt
         /contexts - увидеть список ваших контекстов
         /img - сгенерировать изображение с помощью DALLE-2
         ''',
        'language_confirmation': "Язык был изменен на русский.",
        'language_selection': "Доступно на 3 языках:",
        'processing': "Ваш запрос обрабатывается, пожалуйста, подождите.",
        'error': "Произошла ошибка во время обработки:",
        'contexts': "Пожалуйста, выберите контекст из списка.",
        'delete_context': "Контекст очищен.",
        'id_in_procces': 'Ваш предыдущий запрос еще обрабатывается.',
        'dall_e_3_handler': '''*Введите ваш запрос для генерации изображения:*

Настройки разрешения и степень детализации
изображений, которые генерирует DALL•E 3
_Разрешение_: 1024х1024 | 1024х1792 | 1792х1024
_Детализация_: обычная | высокая
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
        'face-swap-1': '*Отправьте исходную фотографию🖼*, которую вы хотите изменить.',
        # 'face-swap-2': '*Отправьте фотографию🖼:* `замена`, с которой будет взято лицо для переноса.',

        'face-swap-3': "Первая фотография успешно обработана!\n*Отправьте фотографию🖼*, "
                       "с которой будет взято лицо для переноса.\n\n"
                       "Если вы хотите сбросить исходную фотографию, "
                       "воспользуйтесь командой /start."
    }
}


def get_changed_context_line(s):
    return f'Ваш контекст сменён на тему: {s}.'
