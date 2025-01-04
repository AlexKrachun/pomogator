message_templates = {
    'en': {
        'start': "Hello, I'm bot powered on API GPT-4(ChatGPT). Enter /help",
        'new_topic': 'Starting a new topic!',
        'image_prompt': 'Please add a description of the image after the /image command. For example, /image Neon City.',
        'image_error': 'An error occurred during image generation:',
        'about': 'This bot is powered by OpenAI GPT-4.',
        'help': 'You can interact with this bot using commands like /start, /newtopic, /image, /about, and /help.',
        'language_confirmation': "Language has been set to English.",
        'language_selection': "Available in 3 languages:",
        'processing': "Your request is being processed, please wait.",
        'error': "An error occurred during processing:",
        'delete_context': "New context has been created",

    },
    'ru': {
        'start': "Привет, я бот с нейросетями. Напишите свой запрос или выведите справку /help",
        'new_topic': 'Начинаем новую тему!',
        'image_prompt': 'Пожалуйста, добавьте описание изображения после команды /image. Например, /image Неоновый город.',
        'image_error': 'Произошла ошибка при генерации изображения:',
        'about': 'Этот бот работает на OpenAI GPT-4.',
        'help': '''Вы можете взаимодействовать с этим ботом с помощью команд:
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
        'dall_e_3_handler': '''Введите ваш запрос для генерации изображения:
        Выберите разрешение и степень детализации изображений, которые генерирует DALL•E 3

Разрешение: 1024х1024 | 1024х1792 | 1792х1024
Детализация: обычная | высокая

Запрос с высокой степенью детализации стоит 2 генерации''',
        'face-swap-1': 'Наша программа позволяет легко заменять лица на фотографиях. '
                       'Для этого сначала вам потребуется отправить фотографию: "исходник", '
                       'фото которое вы хотите изменить.',
        'face-swap-2': 'Отправьте фотографию: "замена", '
                       'фото, с которого будет взят материал для замены лица.',

    }
}


def get_changed_context_line(s):
    return f'Ваш контекст сменён на тему: {s}.'
