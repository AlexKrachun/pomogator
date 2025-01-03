from Bot.app.openai_api import *  # Убедитесь, что клиент OpenAI настроен правильно
import asyncio
import aiohttp
import os
import aiohttp
import aiofiles
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
import asyncio


async def save_image(prompt, file_path, model="dall-e-2", size="256x256", n=1):
    """
    Генерирует изображение с помощью OpenAI и сохраняет его на устройство.

    :param prompt: Описание для генерации изображения.
    :param file_path: Путь для сохранения файла.
    :param model: Модель для генерации изображения (по умолчанию "dall-e-2").
    :param size: Размер изображения (по умолчанию "256x256").
    :param n: Количество изображений (по умолчанию 1).
    """
    image_url = await generate_image(prompt, model=model, size=size, n=n)

    if not image_url.startswith("http"):
        print(image_url)  # Вывод ошибки, если генерация не удалась
        return

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                if response.status == 200:
                    async with aiofiles.open(file_path, mode='wb') as f:
                        await f.write(await response.read())
                    print(f"Изображение сохранено в {file_path}")
                else:
                    print(f"Ошибка при загрузке изображения: {response.status}")
    except Exception as e:
        print(f"Ошибка при сохранении изображения: {e}")

# Пример вызова функции
asyncio.run(save_image("A beautiful landscape with mountains and rivers", "output_image.png"))
