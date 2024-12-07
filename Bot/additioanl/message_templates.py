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
        'start': "Привет, я бот, работающий на API GPT-4. Напишите свой запрос или выведите справку /help",
        'new_topic': 'Начинаем новую тему!',
        'image_prompt': 'Пожалуйста, добавьте описание изображения после команды /image. Например, /image Неоновый город.',
        'image_error': 'Произошла ошибка при генерации изображения:',
        'about': 'Этот бот работает на OpenAI GPT-4.',
        'help': 'Вы можете взаимодействовать с этим ботом с помощью команд вроде /start, /profile и /help.',
        'language_confirmation': "Язык был изменен на русский.",
        'language_selection': "Доступно на 3 языках:",
        'processing': "Ваш запрос обрабатывается, пожалуйста, подождите.",
        'error': "Произошла ошибка во время обработки:",
        'contexts': "Пожалуйста, выберите контекст из списка.",
        'delete_context': "Контекст очищен.",
        'id_in_procces': 'Ваш предыдущий запрос еще обрабатывается.',
    }
}


def get_changed_context_line(s):
    return f'Ваш контекст сменён на тему: {s}.'
