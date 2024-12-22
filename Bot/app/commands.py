from aiogram import Bot
from aiogram.types import BotCommand

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Запустить бота"),
        BotCommand(command="/mode", description="Выбрать модель"),
        BotCommand(command="/new_context", description="Перейти на новый контекст"),
        BotCommand(command="/contexts", description="Выбрать контекст"),
        BotCommand(command="/img", description="Сгенерировать изображение"),
        BotCommand(command="/profile", description="Показать профиль"),
        BotCommand(command="/pay", description="Купить подписку"),
        BotCommand(command="/help", description="Показать справку"),

    ]
    await bot.set_my_commands(commands)
