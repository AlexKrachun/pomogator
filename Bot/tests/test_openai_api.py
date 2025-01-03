import pytest
from unittest.mock import AsyncMock, patch
from Bot.app.openai_api import get_completion, request_get_topic, limit_tokens, base_for_request, base_for_topic_request
from Bot.app.openai_api import generate_image


@pytest.mark.asyncio
@patch('Bot.app.openai_api.client.chat.completions.create', new_callable=AsyncMock)
async def test_get_completion(mock_create):
    mock_create.return_value = AsyncMock()
    mock_create.return_value.choices = [
        AsyncMock(message=AsyncMock(content="тестовый ответ от openai api"))
    ]

    messages_array = [{"role": "user", "content": "Hello"}]
    model = 'gpt-4o'
    result = await get_completion(messages_array, model)

    mock_create.assert_called_once_with(
        model=model,
        messages=base_for_request + messages_array,
        max_tokens=limit_tokens[model]
    )

    assert result == "тестовый ответ от openai api"


@pytest.mark.asyncio
@patch('Bot.app.openai_api.client.chat.completions.create', new_callable=AsyncMock)
async def test_request_get_topic(mock_create):
    mock_create.return_value = AsyncMock()
    mock_create.return_value.choices = [
        AsyncMock(message=AsyncMock(content="Тестовая тема для диалога"))
    ]

    message = "тестовое сообщение"
    model = 'gpt-4o-mini'
    result = await request_get_topic(message)

    mock_create.assert_called_once_with(
        model=model,
        messages=base_for_topic_request + [{"role": "user", "content": message}],
        max_tokens=limit_tokens[model]
    )

    assert result == "Тестовая тема для диалога"


@pytest.mark.asyncio
@patch('Bot.app.openai_api.client.images.generate', new_callable=AsyncMock)
async def test_generate_image(mock_generate):
    mock_generate.return_value = AsyncMock()
    mock_generate.return_value.data = [
        AsyncMock(url="http://wiki.cs.hse.ru/")
    ]

    prompt = "изображение котенка с закатом на фоне"

    result = await generate_image(prompt)

    mock_generate.assert_called_once_with(
        model="dall-e-2",
        prompt=prompt,
        size="256x256",
        n=1
    )
    assert result == "http://wiki.cs.hse.ru/"


@pytest.mark.asyncio
@patch('Bot.app.openai_api.client.images.generate', new_callable=AsyncMock)
async def test_generate_image_error(mock_generate):
    mock_generate.side_effect = Exception("Ошибка API")

    prompt = "изображение котенка с закатом на фоне"

    result = await generate_image(prompt)

    mock_generate.assert_called_once_with(
        model="dall-e-2",
        prompt=prompt,
        size="256x256",
        n=1
    )

    assert result == "Ошибка при генерации изображения: Ошибка API"
