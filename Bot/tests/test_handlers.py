import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from aiogram import types
from aiogram.fsm.context import FSMContext
from Bot.app.handlers import (
    start_cmd,
    profile_command,
    help_cmd,
    pay_cmd,
    mode_cmd,
    new_context,
    ret_dalle_img,
    handle_context_switch,
    handle_model_switch,
    echo_msg,
)

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Bot.additioanl.message_templates import message_templates
# from Bot.app.utils.state import id_in_processing


@pytest.fixture
def mock_message():
    message = MagicMock(spec=types.Message)
    message.from_user = MagicMock(id=123, username="test_user", first_name="Test", last_name="User")
    message.chat = MagicMock(id=456)
    message.text = "Test message"
    message.answer = AsyncMock()
    message.answer_photo = AsyncMock()
    message.bot = AsyncMock()
    return message

@pytest.fixture
def mock_callback_query():
    callback_query = MagicMock(spec=types.CallbackQuery)
    callback_query.from_user = MagicMock(id=123, username="test_user")
    callback_query.data = "context:1234"
    callback_query.answer = AsyncMock()
    callback_query.message = MagicMock()
    callback_query.message.edit_text = AsyncMock()
    callback_query.message.answer = AsyncMock()
    return callback_query

@pytest.fixture
def mock_state():
    state = AsyncMock(spec=FSMContext)
    state.get_data = AsyncMock(return_value={"promt": "Test prompt"})
    state.update_data = AsyncMock()
    state.clear = AsyncMock()
    return state

@pytest.mark.asyncio
async def test_start_cmd(mock_message):
    await start_cmd(mock_message)
    mock_message.answer.assert_called_once_with(message_templates['ru']['start'])

@pytest.mark.asyncio
async def test_profile_command(mock_message):
    await profile_command(mock_message)
    expected_profile = (
        "👤 Профиль пользователя:\n"
        "ID: 123\n"
        "Имя: Test\n"
        "Фамилия: User\n"
        "Логин: @test_user"
    )
    mock_message.answer.assert_called_once_with(expected_profile)

@pytest.mark.asyncio
async def test_help_cmd(mock_message):
    with patch('Bot.app.handlers.message_templates', {"ru": {"help": "Помощь"}}):
        await help_cmd(mock_message)
        mock_message.answer.assert_called_once_with("Помощь")

@pytest.mark.asyncio
async def test_pay_cmd(mock_message):
    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Оплатить подписку", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")]
        ]
    )
    with patch('Bot.app.keyboard.inline_pay', new=inline_keyboard):
        await pay_cmd(mock_message)
        mock_message.answer.assert_called_once_with(
            'Пока тут все for free, мы возьмем от вас деньги в next time.',
            reply_markup=inline_keyboard
        )

@pytest.mark.asyncio
async def test_mode_cmd(mock_message):
    with patch('Bot.app.handlers.inline_modes', new=AsyncMock(return_value="inline_markup")):
        with patch('Bot.app.handlers.db_client') as mock_db:
            mock_db.get_user_model_by_tg_id.return_value = "gpt-4o"
            await mode_cmd(mock_message)
            mock_message.answer.assert_called_once_with(
                'Выберите подходящую вам модель gpt.',
                reply_markup="inline_markup"
            )

@pytest.mark.asyncio
async def test_new_context(mock_message):
    with patch('Bot.app.handlers.db_client') as mock_db:
        mock_db.create_new_context_by_tg_id.return_value = "new_context_id"
        await new_context(mock_message)
        mock_db.set_current_context_by_tg_id.assert_called_once_with(tg_id=123, another_context_id="new_context_id")
        mock_message.answer.assert_called_once_with(message_templates['ru']['delete_context'])
        
        
@pytest.mark.asyncio
async def test_ret_dalle_img(mock_message, mock_state):
    with patch('Bot.app.handlers.generate_image', new=AsyncMock(return_value="https://example.com/image.png")):
        await ret_dalle_img(mock_message, mock_state)
        mock_message.answer_photo.assert_called_once_with(
            "https://example.com/image.png", caption="Вот ваше сгенерированное изображение!"
        )

@pytest.mark.asyncio
async def test_handle_context_switch(mock_callback_query):
    with patch('Bot.app.handlers.db_client') as mock_db:
        mock_db.get_current_context_by_tg_id.return_value = MagicMock(name="Test Context")
        mock_db.make_context_history.return_value = "История контекста"
        await handle_context_switch(mock_callback_query)
        mock_callback_query.message.answer.assert_any_call("История контекста", parse_mode="Markdown")

@pytest.mark.asyncio
async def test_handle_model_switch(mock_callback_query):
    with patch('Bot.app.handlers.db_client') as mock_db:
        mock_db.get_user_model_by_tg_id.return_value = "gpt-4o-mini"
        await handle_model_switch(mock_callback_query)
        mock_callback_query.message.edit_text.assert_called_once()

@pytest.mark.asyncio
async def test_echo_msg(mock_message):
    with patch('Bot.app.handlers.db_client') as mock_db:
        mock_db.user_is_new_by_tg_id.return_value = False
        mock_db.get_current_context_by_tg_id.return_value = MagicMock(id=1234)
        mock_db.get_full_dialog.return_value = []
        mock_db.get_user_model_by_tg_id.return_value = "gpt-4o-mini"
        with patch('Bot.app.handlers.get_completion', new=AsyncMock(return_value="Test completion")):
            await echo_msg(mock_message)
            mock_message.answer.assert_any_call("Test completion", parse_mode="Markdown")
