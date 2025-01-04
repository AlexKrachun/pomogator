from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.main import db_client
import logging


async def inline_contexts(user_id):
    keyboard = InlineKeyboardBuilder()

    current_context_id = db_client.get_current_context_id_by_tg_id(user_id)
    for context in db_client.get_users_contexts_by_tg_id(user_id):
        button_text = context['name'] + (' ✅' if context['id'] == current_context_id else '')
        keyboard.add(InlineKeyboardButton(text=button_text, callback_data=f'context:{str(context["id"])}'))
    return keyboard.adjust(1).as_markup()

# def get_user_model(user_id, curr_users_models):
#     if user_id not in curr_users_models:
#         return 'gpt-4o-mini'

#     return curr_users_models.get(user_id, 'gpt-4o-mini')


ai_models = ['gpt-4o-mini',
             'gpt-4o',
             'o1-mini',
             'o1-preview',
             'claude-3-5-haiku-latest',
             'claude-3-5-sonnet-latest',
             'dall-e-3',
             'face-swap'
             ]

button_names = {
    'gpt-4o-mini': 'gpt-4o-mini',
    'gpt-4o': 'gpt-4o',
    'o1-mini': 'o1-mini',
    'o1-preview': 'o1-preview',
    'claude-3-5-sonnet-latest': 'claude 3.5-sonnet',
    'claude-3-5-haiku-latest': 'claude 3.5-haiku',
    'dall-e-3': 'dall-e-3',
    'face-swap': 'face-swap',
}


async def inline_modes(user_id, model):
    logging.debug(model)
    keyboard = InlineKeyboardBuilder()

    for mode in ai_models:
        curr_mode = button_names[mode]
        if model == mode:
            curr_mode += '✅'

        keyboard.add(InlineKeyboardButton(text=curr_mode, callback_data=f'model:{mode}'))

    # keyboard.add(InlineKeyboardButton(text='o1-preview', url='https://www.youtube.com/watch?v=dQw4w9WgXcQ'))

    return keyboard.adjust(2, 2, 2, 1, 1).as_markup()


quality_settings = ['standard', 'hd']
resolution_settings = ['1024x1024', '1024x1792', '1792x1024']


async def dalle_3_settings(user_id, quality='standard', resolution='1024x1024'):
    keyboard = InlineKeyboardBuilder()

    for qual in quality_settings:
        curr_quality = qual
        if quality == qual:
            curr_quality += '✅'

        keyboard.add(InlineKeyboardButton(text=curr_quality, callback_data=f'quality:{qual}'))

    for resol in resolution_settings:
        curr_resolution = resol
        if resolution == resol:
            curr_resolution += '✅'

        keyboard.add(InlineKeyboardButton(text=curr_resolution, callback_data=f'resolution:{resol}'))

    return keyboard.adjust(2, 3).as_markup()


inline_pay = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Оплатить подписку", url='https://www.youtube.com/watch?v=dQw4w9WgXcQ')]
    ]
)
