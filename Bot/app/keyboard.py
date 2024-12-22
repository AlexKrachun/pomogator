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

    return curr_users_models.get(user_id, 'gpt-4o-mini')


chatgpt_models = ['gpt-4o-mini', 'gpt-4o']
img_generation_models = ['dall-e-2']


async def inline_modes(user_id, curr_users_models):
    print(curr_users_models)
    print(user_id, get_user_model(user_id, curr_users_models))
    keyboard = InlineKeyboardBuilder()

    for mode in chatgpt_models:
        curr_mode = mode
        if get_user_model(user_id, curr_users_models) == mode:
            curr_mode += '✅'

        keyboard.add(InlineKeyboardButton(text=curr_mode, callback_data=f'model:{curr_mode}'))

    keyboard.add(InlineKeyboardButton(text='o1-preview', url='https://www.youtube.com/watch?v=dQw4w9WgXcQ'))
    keyboard.add(InlineKeyboardButton(text='o1-mini', url='https://www.youtube.com/watch?v=dQw4w9WgXcQ'))
    for mode in img_generation_models:
        curr_mode = mode + '✅'

        keyboard.add(InlineKeyboardButton(text=curr_mode, callback_data=f'model:{curr_mode}'))

    return keyboard.adjust(2).as_markup()


inline_pay = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Оплатить подписку", url='https://www.youtube.com/watch?v=dQw4w9WgXcQ')]
    ]
)
