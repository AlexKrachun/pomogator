from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

from aiogram.utils.keyboard import InlineKeyboardBuilder


async def inline_contexts(user_id, from_context_id_get_topic, get_users_contexts):
    keyboard = InlineKeyboardBuilder()
    for context_id in get_users_contexts[user_id]:
        keyboard.add(InlineKeyboardButton(text=from_context_id_get_topic[context_id],
                                          callback_data=f'context:{str(context_id)}'))
    return keyboard.adjust(1).as_markup()


def get_user_model(user_id, curr_users_models):
    if user_id not in curr_users_models:
        return 'gpt-4o-mini'

    # return curr_users_models[user_id]
    return curr_users_models.get(user_id, 'gpt-4o-mini')


chatgpt_models = ['gpt-4o', 'gpt-4o-mini']


async def inline_modes(user_id, curr_users_models):
    own_chatgpt_models = []
    print(curr_users_models)
    print(user_id, get_user_model(user_id, curr_users_models))
    for mode in chatgpt_models:
        if get_user_model(user_id, curr_users_models) == mode:
            own_chatgpt_models.append(mode + '✅')
        else:
            own_chatgpt_models.append(mode)

    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text=own_chatgpt_models[1], callback_data=f'model:{chatgpt_models[1]}'))
    keyboard.add(InlineKeyboardButton(text=own_chatgpt_models[0], callback_data=f'model:{chatgpt_models[0]}'))
    keyboard.add(InlineKeyboardButton(text='o1-preview', url='https://www.youtube.com/watch?v=dQw4w9WgXcQ'))
    keyboard.add(InlineKeyboardButton(text='o1-mini', url='https://www.youtube.com/watch?v=dQw4w9WgXcQ'))

    return keyboard.adjust(2).as_markup()


# mode_keyboard = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [InlineKeyboardButton(text="GPT-4o mini", callback_data=f'model:{chatgpt_models[1]}'),
#          InlineKeyboardButton(text="GPT-4o", callback_data=f'model:{chatgpt_models[0]}')],
#         [InlineKeyboardButton(text="o1-mini", url='https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
#          InlineKeyboardButton(text="o1-preview", url='https://www.youtube.com/watch?v=dQw4w9WgXcQ')],
#     ]
# )

inline_pay = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Оплатить подписку", url='https://www.youtube.com/watch?v=dQw4w9WgXcQ')]
    ]
)
