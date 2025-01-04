# import logging.config
# import os
# import logging
# import asyncio
# from aiogram import Bot, Dispatcher
# import sys

# from Bot.app.handlers import router
# from Bot.app.commands import set_commands
# from dotenv import load_dotenv

# from logging.handlers import RotatingFileHandler

# load_dotenv()
# bot_token = os.environ.get('BOT_TOKEN')


# logging.basicConfig(
#     level=logging.DEBUG,
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#     handlers=[
#         RotatingFileHandler(
#             "bot_log.log",
#             maxBytes=5 * 1024 * 1024,  # 5 МБ
#             backupCount=5,
#             encoding='utf-8'
#         ),
#         logging.StreamHandler(sys.stdout)
#     ]
# )

# logging.getLogger("httpx").setLevel(logging.WARNING)
# logging.getLogger("aiogram").setLevel(logging.WARNING)

# # logger = logging.getLogger(__name__)
# logger = logging.getLogger('bot_logger')



# if __name__ == '__main__':
#     async def main():
#         logging.error('аааааа, дебажу логер')
#         logging.info("Запуск бота...")
#         if not bot_token:
#             logging.error("Переменная окружения BOT_TOKEN не найдена.")
#             raise ValueError("Переменная окружения BOT_TOKEN не найдена.")

#         bot = None
#         try:
#             logging.info("Инициализация бота.")
#             bot = Bot(token=bot_token)

#             logging.info("Создание диспетчера.")
#             dp = Dispatcher()

#             logging.info("Подключение роутера.")
#             dp.include_router(router)

#             logging.info("Установка команд бота.")
#             await set_commands(bot)

#             logging.info("Начало polling.")
#             await dp.start_polling(bot)


#         except Exception as e:
#             logging.exception(f"Необработанное исключение: {e}")
#         finally:
#             if bot:
#                 try:
#                     logging.info("Завершение работы бота.")
#                     await bot.close()
#                 except Exception as e:
#                     logging.exception(f"Ошибка при закрытии бота: {e}")


#     try:
#         asyncio.run(main())
#     except Exception as e:
#         logging.exception(f"Не удалось запустить бота: {e}")



import os
import logging
import asyncio
from aiogram import Bot, Dispatcher
import sys
from Bot.app.handlers import router
from Bot.app.commands import set_commands
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

load_dotenv()
bot_token = os.environ.get('BOT_TOKEN')


def setup_logger():
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    logger = logging.getLogger('bot_logger')
    logger.setLevel(logging.INFO)

    if logger.handlers:
        logger.handlers.clear()

    file_handler = RotatingFileHandler(
        "bot_log.log",
        maxBytes=5 * 1024 * 1024,  # 5 МБ
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("aiogram").setLevel(logging.WARNING)

    return logger

logger = setup_logger()

if __name__ == '__main__':
    async def main():
        logger.info("Запуск бота...")
        if not bot_token:
            logger.error("Переменная окружения BOT_TOKEN не найдена.")
            raise ValueError("Переменная окружения BOT_TOKEN не найдена.")

        bot = None
        try:
            logger.info("Инициализация бота.")
            bot = Bot(token=bot_token)

            logger.info("Создание диспетчера.")
            dp = Dispatcher()

            logger.info("Подключение роутера.")
            dp.include_router(router)

            logger.info("Установка команд бота.")
            await set_commands(bot)

            logger.info("Начало polling.")
            await dp.start_polling(bot)

        except Exception as e:
            logger.exception(f"Необработанное исключение: {e}")
        finally:
            if bot:
                try:
                    logger.info("Завершение работы бота.")
                    await bot.close()
                except Exception as e:
                    logger.exception(f"Ошибка при закрытии бота: {e}")

    try:
        asyncio.run(main())
    except Exception as e:
        logger.exception(f"Не удалось запустить бота: {e}")