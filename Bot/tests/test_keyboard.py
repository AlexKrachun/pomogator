import pytest
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Bot.app.keyboard import inline_contexts, inline_modes, get_user_model, inline_pay, chatgpt_models


@pytest.mark.asyncio
async def test_inline_contexts():
    user_id = 123
    from_context_id_get_topic = {
        10: "Topic A",
        11: "Topic B",
        12: "Topic C"
    }
    get_users_contexts = {
        123: [10, 11, 12]
    }

    result = await inline_contexts(user_id, from_context_id_get_topic, get_users_contexts)

    assert isinstance(result, InlineKeyboardMarkup)
    assert len(result.inline_keyboard) == 3
    expected_data = [(10, "Topic A"), (11, "Topic B"), (12, "Topic C")]
    for row, (context_id, topic) in zip(result.inline_keyboard, expected_data):
        button = row[0]
        assert button.text == topic
        assert button.callback_data == f"context:{context_id}"


def test_get_user_model():
    curr_users_models = {
        123: "gpt-4o",
        456: "gpt-4o-mini"
    }

    assert get_user_model(123, curr_users_models) == "gpt-4o"
    assert get_user_model(456, curr_users_models) == "gpt-4o-mini"
    assert get_user_model(789, curr_users_models) == "gpt-4o-mini"


@pytest.mark.asyncio
async def test_inline_modes():
    user_id = 123
    curr_users_models = {
        123: "gpt-4o",
    }

    result = await inline_modes(user_id, curr_users_models)
    assert isinstance(result, InlineKeyboardMarkup)

    expected_buttons = {"gpt-4o-mini", "gpt-4o✅"}

    all_buttons = {button.text for row in result.inline_keyboard for button in row}

    assert all_buttons == expected_buttons, f"Expected buttons {expected_buttons}, but got {all_buttons}"


def test_inline_pay():
    assert isinstance(inline_pay, InlineKeyboardMarkup)
    assert len(inline_pay.inline_keyboard) == 1
    assert len(inline_pay.inline_keyboard[0]) == 1
    button = inline_pay.inline_keyboard[0][0]
    assert isinstance(button, InlineKeyboardButton)
    assert button.text == "Оплатить подписку"
    assert button.url == 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'


@pytest.mark.asyncio
async def test_inline_contexts_simple():
    user_id = 123
    from_context_id_get_topic = {
        10: "Topic A"
    }
    get_users_contexts = {
        123: [10]
    }

    result = await inline_contexts(user_id, from_context_id_get_topic, get_users_contexts)

    assert isinstance(result, InlineKeyboardMarkup)
    assert len(result.inline_keyboard) == 1
    button = result.inline_keyboard[0][0]
    assert button.text == "Topic A"
    assert button.callback_data == "context:10"