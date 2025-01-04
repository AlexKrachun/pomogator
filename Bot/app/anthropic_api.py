from dotenv import load_dotenv
import os
import anthropic
from anthropic.types import MessageParam

load_dotenv()
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')

client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

async def get_claude_text_response(messages_array: list[MessageParam], model_name: str, max_tokens: int = 2048) -> str:
    res = await client.messages.create(
        model=model_name,
        messages=messages_array,
        # max_tokens=max_tokens,
        max_tokens=max_tokens,
    )
    text_answer = res.content[0].text
    return text_answer
