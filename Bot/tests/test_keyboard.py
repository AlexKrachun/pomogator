import pytest
from unittest.mock import patch, MagicMock
from Bot.app.keyboard import inline_contexts, inline_modes



@pytest.mark.asyncio
@patch('Bot.app.keyboard.db_client', new_callable=MagicMock)
async def test_inline_contexts(mock_db_client):
    user_id = 123
    mock_db_client.get_users_contexts_by_tg_id.return_value = [
        {"id": 10, "name": "Topic A"},
        {"id": 11, "name": "Topic B"},
        {"id": 12, "name": "Topic C"}
    ]

    result = await inline_contexts(user_id)

    assert len(result.inline_keyboard) == 3
    for button, expected in zip(result.inline_keyboard, ["Topic A", "Topic B", "Topic C"]):
        assert button[0].text == expected
        assert button[0].callback_data.startswith("context:")



@pytest.mark.asyncio
async def test_inline_modes():
    user_id = 123
    model = "gpt-4o"

    result = await inline_modes(user_id, model)

    expected_buttons = {'gpt-4o-mini',
                        'gpt-4o ✅',
                        'o1-mini',
                        'o1-preview',
                        'claude 3.5-sonnet',
                        'claude 3.5-haiku',
                        'dall-e-3',
                        'face-swap',
                        }

    all_buttons = {button.text for row in result.inline_keyboard for button in row}
    assert all_buttons == expected_buttons
