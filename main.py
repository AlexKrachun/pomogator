import os
import logging
import asyncio
from aiogram import Bot, Dispatcher

from Bot.app.handlers import router
from Bot.app.commands import set_commands
from dotenv import load_dotenv

load_dotenv()
bot_token = os.environ.get('BOT_TOKEN')

if __name__ == '__main__':
    async def main():
        logging.basicConfig(level=logging.INFO)
        bot = Bot(token=bot_token)
        dp = Dispatcher()
        dp.include_router(router)
        await set_commands(bot)
        await dp.start_polling(bot)

    asyncio.run(main())  # Запускаем основную функцию
