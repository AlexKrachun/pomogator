from aiogram import BaseMiddleware
from aiogram.types import Message
from db.main import db_client


class UserRegistrationMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        us_id = event.from_user.id

        if db_client.user_is_new_by_tg_id(us_id):
            db_client.add_user(name=event.from_user.full_name, tg_id=us_id, last_used_model='gpt-4o-mini')
            chat_id = db_client.create_new_context_by_tg_id(tg_id=us_id)
            db_client.set_current_context_by_tg_id(tg_id=us_id, context_id=chat_id)
            print("Писюлька пользователь зареган убежище")
            # await event.answer("Пользователь успешно зарегистрирован! Повторите запрос.")
            # return  # Прерываем обработку события

        # Если пользователь зарегистрирован, передаем управление дальше
        return await handler(event, data)