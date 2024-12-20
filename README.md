| **Функция**                                    | **Статус** |
|------------------------------------------------|------------|
| Выбор нейросети - среди моделей OpenAI         | ✅         |
| Отображение профиля                            | ✅         |
| Создать новый чат                              | ✅         |
| Получить памятку об устройстве бота            | ✅         |
| Отправить текстовый промпт                     | ✅         |
| Получить текстовый ответ на промпт             | ✅         |



#                     Telegram Bot                         #

## Обзор проекта
Этот проект представляет собой Telegram-бота, реализованного с 
использованием библиотеки Aiogram и API OpenAI GPT.

**❗Важно:** В проекте также есть папка `backend`, которая содержит код для создания сайта с использованием FastAPI. Однако эта часть проекта **не связана** с проектом по курсу "Deep Python". Итоговый проект представляет собой именно Telegram-бот, а сайт является отдельной частью, не относящейся к задачам курса.


------------------------------------------------------------
## 1. Структура проекта
Проект разбит по модулям:

- additioanl/
  - message_templates.py: Шаблоны сообщений бота на русском и английском.

- app/
  - commands.py: Реализует команды бота (/start, /help, /mode и др.).
  - handlers.py: Обработка сообщений и обратных вызовов.
  - keyboard.py: Генерация интерактивных клавиатур.
  - openai_api.py: Работа с OpenAI API (генерация текстов, тем сообщений).

- tests/
  - Тесты для проверки модулей commands, keyboard, handlers и взаимодействия с API.

- main.py:
  - Точка входа в приложение, где настраиваются бот и диспетчер.

------------------------------------------------------------
## 2. Основной функционал
- Поддержка нескольких языков: русский и английский.
- Команды:
  - /start — Запуск бота.
  - /help — Справка по боту.
  - /mode — Выбор модели GPT.
  - /contexts — Выбор контекста.
  - /delete_context — Очистка текущего контекста.
  - /profile — Профиль пользователя.
  - /pay — Кнопка для оплаты.
- Интерактивные клавиатуры:
  - Inline-клавиатуры для выбора моделей и контекстов.
- Интеграция с OpenAI API:
  - Генерация ответов на сообщения.
  - Определение тем для переключения контекстов.

------------------------------------------------------------
## 3. Тестирование
Проект включает модули для тестирования:
- test_commands.py:
  - Проверка настройки и работы команд.
- test_keyboard.py:
  - Проверка генерации inline-клавиатур.
- test_handlers.py:
  - Проверка обработки сообщения пользователей и событий callback.
- test_openai_api.py:
  - Тестирование взаимодействия с OpenAI API.

Для тестирования используются pytest и unittest.mock.

------------------------------------------------------------
## 4. Как запустить проект

1. Установите `.env` в свой проект.
2. Установите `requirements.txt`.
3. Запустите `main.py`:


------------------------------------------------------------
#         Функциональные задачи          #

1. **Интегрировать использование базы данных** для хранения информации о пользователях, их настройках и контекстах переписки.
