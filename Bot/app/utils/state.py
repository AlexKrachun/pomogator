# state.py
# Глобальные переменные для хранения данных

# Хранение всех контекстов
all_contexts = dict()  # context_id -> JSON

# Соответствие пользователя и списка его контекстов
get_users_contexts = dict()  # user_id -> [context_id_1, context_id_2, ...]

# Текущий контекст пользователя
curr_users_context = dict()  # user_id -> current_context_id

# Выбранные модели для пользователей
curr_users_models = dict()  # user_id -> model_name

# Соответствие контекста и его темы
from_context_id_get_topic = dict()  # context_id -> topic

# Обработка уникальных идентификаторов
id_in_processing = set()
id_not_new_users = set()

# Языковые настройки пользователей
user_languages = {}

# Сообщения для каждого пользователя
messages = dict()
