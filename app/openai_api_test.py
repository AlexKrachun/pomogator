import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
import asyncio

load_dotenv()
openai_api_key = os.environ.get('OPENAI_API_KEY')
client = AsyncOpenAI(api_key=openai_api_key)

limit_tokens = {
    'gpt-4o': 5000,
    'gpt-4o-mini': 5000,
    'o1-preview': 5000
}


async def get_completion(messages_array, model):
    completion = await client.chat.completions.create(
        model=model,
        messages=messages_array,
        max_tokens=limit_tokens[model]
    )
    print(f'Модель - {model}')
    return completion.choices[0].message.content

