import pytest
from unittest.mock import AsyncMock
from aiogram import Bot
from aiogram.types import BotCommand
from Bot.app.commands import set_commands

@pytest.mark.asyncio
async def test_set_commands():

    mock_bot = AsyncMock(spec=Bot)


    await set_commands(mock_bot)

    expected_commands = [
        BotCommand(command="/start", description="Запустить бота"),
        BotCommand(command="/mode", description="Выбрать модель"),
        BotCommand(command="/delete_context", description="Удалить контекст"),
        BotCommand(command="/contexts", description="Выбрать контекст"),
        BotCommand(command="/profile", description="Показать профиль"),
        BotCommand(command="/pay", description="Купить подписку"),
        BotCommand(command="/help", description="Показать справку"),
    ]

    mock_bot.set_my_commands.assert_called_once_with(expected_commands)