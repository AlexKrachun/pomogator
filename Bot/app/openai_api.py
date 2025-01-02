import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
import openai
import asyncio

load_dotenv()
openai_api_key = os.environ.get('OPENAI_API_KEY')
client = AsyncOpenAI(api_key=openai_api_key)

limit_tokens = {
    'gpt-4o': 5000,
    'gpt-4o-mini': 5000,
    'o1-preview': 5000
}

base_for_request = [{"role": "system", "content": "You are a helpful assistant."}]

base_for_topic_request = [{"role": "system",
                           "content": "You make a title for messages in a maximum of several words, write only words,"
                                      " without formulas and nothing else"}]


async def get_completion(messages_array, model):
    messages_array = base_for_request + messages_array
    completion = await client.chat.completions.create(
        model=model,
        messages=messages_array,
        max_tokens=limit_tokens[model]
    )
    print(f'Модель - {model}')
    return completion.choices[0].message.content


async def request_get_topic(message):
    model = 'gpt-4o-mini'
    messages_array = base_for_topic_request + [{"role": "user", "content": message}]
    completion = await client.chat.completions.create(
        model=model,
        messages=messages_array,
        max_tokens=limit_tokens[model]
    )
    print(f'Модель - {model}')
    return completion.choices[0].message.content


async def generate_image(prompt, model="dall-e-3", size="1024x1024", quality="standard", n=1):
    try:
        response = await client.images.generate(
            model=model,
            prompt=prompt,
            size=size,
            quality="standard",
            n=n
        )
        return response.data[0].url
    except Exception as e:
        return f"Ошибка при генерации изображения: {e}"
