import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from Bot.app.handlers import (
    language_cmd,
    pay_cmd,
    mode_cmd,
    start_cmd,
    profile_command,
    help_cmd,
    new_context,
    handle_context_switch,
    handle_model_switch,
    echo_msg,
    generate_unique_number,
    make_context_history,
    get_user_model,
    user_languages,
    id_in_processing,
)
from Bot.additioanl.message_templates import message_templates, get_changed_context_line
from aiogram.types import Message, CallbackQuery, User, Chat
from aiogram import Bot


@pytest.fixture
def mock_message():
    message = MagicMock(spec=Message)
    message.from_user = MagicMock(
        id=123, username="test_user", first_name=None, last_name=None
    )
    message.chat = MagicMock(id=456)
    message.answer = AsyncMock()
    message.bot = MagicMock()
    message.reply_markup = MagicMock()
    return message


@pytest.fixture
def mock_callback_query():
    callback_query = MagicMock(spec=CallbackQuery)
    callback_query.from_user = MagicMock(id=123, username="test_user")
    callback_query.message = MagicMock()
    callback_query.message.answer = AsyncMock()
    callback_query.message.edit_text = AsyncMock()
    callback_query.answer = AsyncMock()
    callback_query.data = "context:1234"
    return callback_query


@pytest.fixture(autouse=True)
def setup_global_data():
    from Bot.app.handlers import (
        user_languages,
        from_context_id_get_topic,
        all_contexts,
        curr_users_context,
        id_in_processing,
    )

    user_languages[123] = "ru"
    from_context_id_get_topic["1234"] = "Тестовая тема"
    all_contexts["1234"] = [
        {"role": "user", "content": "Привет"},
        {"role": "assistant", "content": "Здравствуйте"},
    ]
    curr_users_context[123] = "1234"
    id_in_processing.clear()


@pytest.mark.asyncio
async def test_profile_command_no_name(mock_message):

    await profile_command(mock_message)
    mock_message.answer.assert_called_once_with(
        "👤 Профиль пользователя:\nID: 123\nИмя: не указан\nФамилия: не указан\nЛогин: @test_user"
    )


@pytest.mark.asyncio
async def test_profile_command_with_name(mock_message):

    mock_message.from_user = MagicMock(
        id=123,
        username="test_user",
        first_name="Testfirstname",
        last_name="Testlastname",
    )
    await profile_command(mock_message)
    mock_message.answer.assert_called_once_with(
        "👤 Профиль пользователя:\nID: 123\nИмя: Testfirstname\nФамилия: Testlastname\nЛогин: @test_user"
    )


@pytest.mark.asyncio
async def test_help_cmd_ru(mock_message):
    user_languages[mock_message.from_user.id] = "ru"
    await help_cmd(mock_message)
    mock_message.answer.assert_called_once_with(message_templates["ru"]["help"])


@pytest.mark.asyncio
async def test_help_cmd_en(mock_message):
    user_languages[mock_message.from_user.id] = "en"
    await help_cmd(mock_message)
    mock_message.answer.assert_called_once_with(message_templates["en"]["help"])


@pytest.mark.asyncio
async def test_new_context_cmd_ru(mock_message):
    user_languages[mock_message.from_user.id] = "ru"
    await new_context(mock_message)
    mock_message.answer.assert_called_once_with(
        message_templates["ru"]["delete_context"]
    )


# @pytest.mark.asyncio
# async def test_new_context_cmd_en(mock_message):
#     user_languages[mock_message.from_user.id] = 'en'
#     await new_context(mock_message)
#     mock_message.answer.assert_called_once_with(message_templates['en']['delete_context'])


@pytest.mark.asyncio
async def test_handle_context_switch(mock_callback_query):
    mock_callback_query.data = "context:1234"

    await handle_context_switch(mock_callback_query)
    mock_callback_query.message.answer.assert_called_with(
        "😍test_user:\nПривет\n\n🤖ChatGPT:\nЗдравствуйте\n\nКонтекст переключен"
    )


@pytest.mark.asyncio
async def test_handle_model_switch(mock_callback_query):
    mock_callback_query.data = "model:gpt-3"
    await handle_model_switch(mock_callback_query)
    # mock_callback_query.message.edit_text.assert_called_once_with("Выберите подходящую вам модель gpt. ")
    mock_callback_query.message.edit_text.assert_called_once()


# @pytest.mark.asyncio
# async def test_echo_msg(mock_message):
#     mock_message.text = "Hello"
#     mock_message.photo = None
#     await echo_msg(mock_message)
#     mock_message.answer.assert_called()




# @pytest.mark.asyncio
# async def test_echo_msg_user_already_in_processing():
#     mock_message = AsyncMock(spec=Message)
#     mock_message.from_user.id = 12345
#     mock_message.from_user.username = "test_user"
#     mock_message.text = "Test message"
#     mock_message.answer = AsyncMock()

#     id_in_processing.add(12345)

#     await echo_msg(mock_message)

#     mock_message.answer.assert_called_once_with(message_templates['ru']['id_in_procces'])

#     assert 12345 in id_in_processing

#     id_in_processing.clear()