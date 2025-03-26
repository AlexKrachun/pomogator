import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
import openai
import asyncio
from Bot.app.consts import max_tokens

load_dotenv()
openai_api_key = os.environ.get('OPENAI_API_KEY')
client = AsyncOpenAI(api_key=openai_api_key)

# limit_tokens = {
#     'gpt-4o-mini': max_tokens,
#     'gpt-4o': max_tokens,
#     'o3-mini': max_tokens,
#     'gpt-4o-search-preview': max_tokens,
#     'o1': max_tokens,
#     'gpt-4.5-preview': max_tokens,
# }

base_for_request = [{"role": "system", "content": "You are a helpful assistant."}]

base_for_topic_request = [{"role": "system",
                           "content": "You make a title for messages in a maximum of several words, write only words,"
                                      " without formulas and nothing else"}]



async def get_common_gpt_complection(messages_array, model):
    # response, response_statistics = await get_completion(messages_array, model)

    # return response, response_statistics
    if model in ['gpt-4o', 'gpt-4o-mini', 'gpt-4o-search-preview', 'gpt-4.5-preview']:
        response, response_statistics = await get_completion(messages_array, model)
    elif model in ['o3-mini', 'o1']:
        response, response_statistics = await get_gpt_thought_through_completion(messages_array, model)

    return response, response_statistics

    # else:
    #     response = 'Ошибка при генерации'
    #     responsed_stat = None
    # return response, responsed_stat


async def get_completion(messages_array, model):
    messages_array = base_for_request + messages_array
    completion = await client.chat.completions.create(
        model=model,
        messages=messages_array,
        max_tokens=max_tokens
    )
    print("\n" * 3, completion, '\n' * 3)
    print(f'Модель - {model}')
    responsed_text = completion.choices[0].message.content
    responsed_stat = {
        'sent_to_input_size_tok': completion.usage.prompt_tokens,
        'answer_size_tok': completion.usage.completion_tokens,
    }
    return responsed_text, responsed_stat


async def get_gpt_thought_through_completion(messages_array, model):
    completion = await client.chat.completions.create(
        model=model,
        messages=messages_array,
    )
    print(f'Модель - {model}')
    responsed_text = completion.choices[0].message.content

    responsed_stat = {
        'sent_to_input_size_tok': completion.usage.prompt_tokens,
        'answer_size_tok': completion.usage.completion_tokens,
    }
    return responsed_text, responsed_stat

async def request_get_topic(message):
    model = 'gpt-4o-mini'
    messages_array = base_for_topic_request + [{"role": "user", "content": message}]
    completion = await client.chat.completions.create(
        model=model,
        messages=messages_array,
        max_tokens=50,
        # max_tokens=limit_tokens[model]
    )
    print(f'Модель - {model}')
    return completion.choices[0].message.content


async def generate_image(prompt, model="dall-e-3", size="1024x1024", quality="standard", n=1):
    try:
        response = await client.images.generate(
            model=model,
            prompt=prompt,
            size=size,
            quality=quality,
            n=n
        )
        return response.data[0].url
    except Exception as e:
        return f"Ошибка при генерации изображения: {e}"





'''
ChatCompletion(id='chatcmpl-BF822hDlmzVu4AfyMaKo8XaodCXjR',
choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='Привет! Как дела? Чем могу помочь?', refusal=None, role='assistant', audio=None, function_call=None, tool_calls=None, annotations=[]))], created=1742945494, model='gpt-4o-mini-2024-07-18', object='chat.completion', service_tier='default', system_fingerprint='fp_27322b4e16', usage=CompletionUsage(completion_tokens=11, prompt_tokens=39, total_tokens=50, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=0, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0)))



 ChatCompletion(id='chatcmpl-9aff96fc-9ebd-45ea-b9b0-0d044ba1628e',
choices=[Choice(finish_reason='stop',
index=0,
logprobs=None,
message=ChatCompletionMessage(content='Привет! Чем могу вам помочь сегодня? ',
refusal=None,
role='assistant',
audio=None,
function_call=None,
tool_calls=None,
annotations=[]))],
created=1742945611,
model='gpt-4o-search-preview-2025-03-11',
object='chat.completion',
service_tier=None,
system_fingerprint='',
usage=CompletionUsage(completion_tokens=10,
prompt_tokens=847,
total_tokens=857,
completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0,
audio_tokens=0,
reasoning_tokens=0,
rejected_prediction_tokens=0),
prompt_tokens_details=PromptTokensDetails(audio_tokens=0,
cached_tokens=0)))
'''
