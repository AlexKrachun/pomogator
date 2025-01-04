from functools import wraps
from aiogram.types import Message

from Bot.app.utils.state import id_in_processing
from Bot.additioanl.message_templates import message_templates

from db.main import db_client


def processing_guard(handler):
    @wraps(handler)
    async def wrapper(message: Message, *args, **kwargs):
        us_id = message.from_user.id
        if us_id in id_in_processing:
            # await message.answer(message_templates['ru']['id_in_procces'])
            # await message.answer('ПИСЯКАКА, еще старый запрос делается, бро')
            await message.answer('Подожди окончания обработки последнего запроса')

            return
        return await handler(message, *args, **kwargs)

    return wrapper


def block_not_llm_model(handler):
    @wraps(handler)
    async def wrapper(message: Message, *args, **kwargs):
        us_id = message.from_user.id
        curr_model = db_client.get_user_model_by_tg_id(us_id)
        if curr_model in ['dall-e-3', 'face-swap']:
            # await message.answer(message_templates['ru']['id_in_procces'])
            await message.answer('Сначала переключись на текстовую модель в /mode')
            return
        return await handler(message, *args, **kwargs)

    return wrapper


def block_not_dalle_model(handler):
    @wraps(handler)
    async def wrapper(message: Message, *args, **kwargs):
        us_id = message.from_user.id
        curr_model = db_client.get_user_model_by_tg_id(us_id)
        if curr_model not in ['dall-e-3']:
            # await message.answer(message_templates['ru']['id_in_procces'])
            await message.answer('Сначала переключись на dalle в /mode')
            return
        return await handler(message, *args, **kwargs)

    return wrapper



