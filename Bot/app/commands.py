from aiogram import Bot
from aiogram.types import BotCommand

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Перезапустить бота"),
        BotCommand(command="/mode", description="Выбрать нейросеть"),
        BotCommand(command="/new_context", description="Перейти на новый контекст"),
        BotCommand(command="/contexts", description="Выбрать контекст"),
        BotCommand(command="/info", description="Почитать про функциолан бота и наши нейросети"),
        BotCommand(command="/profile", description="Показать профиль"),
        BotCommand(command="/pay", description="Купить подписку"),

    ]
    await bot.set_my_commands(commands)
