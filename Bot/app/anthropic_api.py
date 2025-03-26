from dotenv import load_dotenv
import os
import anthropic
from anthropic.types import MessageParam
from Bot.app.consts import max_tokens

load_dotenv()
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')

client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

async def get_claude_text_response(messages_array: list[MessageParam], model_name: str) -> str:
    res = await client.messages.create(
        model=model_name,
        messages=messages_array,
        max_tokens=max_tokens,
    )
    text_answer = res.content[0].text
    responsed_stat = {
        'sent_to_input_size_tok': res.usage.input_tokens,
        'answer_size_tok': res.usage.output_tokens,
    }
    return text_answer, responsed_stat

'''
res:

Message(id='msg_01B4xkTpFLdyL9yFn6MgTjS9',
content=[TextBlock(text='Я не могу подготовить подробный медицинский доклад в таком стиле. Если вас интересует научная информация о строении и функциях репродуктивной системы, я могу предложить корректную медицинскую консультацию или посоветовать профессиональные источники.', type='text')],
model='claude-3-5-haiku-20241022',
role='assistant',
stop_reason='end_turn',
stop_sequence=None,
type='message',
usage=Usage(cache_creation_input_tokens=0, cache_read_input_tokens=0, input_tokens=605, output_tokens=88))

'''
