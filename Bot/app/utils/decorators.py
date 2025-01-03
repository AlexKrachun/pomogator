from functools import wraps
from aiogram.types import Message

from Bot.app.utils.state import id_in_processing
from Bot.additioanl.message_templates import message_templates


def processing_guard(handler):
    @wraps(handler)
    async def wrapper(message: Message, *args, **kwargs):
        us_id = message.from_user.id
        if us_id in id_in_processing:
            await message.answer(message_templates['ru']['id_in_procces'])
            return
        return await handler(message, *args, **kwargs)

    return wrapper
