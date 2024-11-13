from openai import OpenAI
import os
from dotenv import load_dotenv
import asyncio



# async def answer_with_chatgpt(user_id, chat_id, messages, prompt: str, model='gpt-4o-mini'):

#     load_dotenv()

#     client = OpenAI(
#     api_key=os.environ.get("OPENAI_API_KEY"),
#     )

#     # messages = get_messages(user_id, chat_id)
#     # completion = await client.chat.completions.create(
#     #     model="gpt-4o-mini",
#     #     messages=[
#     #         {"role": "system", "content": "You are a helpful assistant."},
#     #         {
#     #             "role": "user",
#     #             "content": prompt
#     #         }
#     #     ]
#     # )

#     completion = client.chat.completions.create(
#         model=model,
#         messages=messages
#     )
#     print(completion)

#     return completion.choices[0].message.content



async def answer_with_chatgpt(user_id, chat_id, messages, prompt: str, model='gpt-4o-mini'):

    load_dotenv()

    client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    )

    # messages = get_messages(user_id, chat_id)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user","content": prompt}
        ]
    )

    # completion = client.chat.completions.create(
    #     model=model,
    #     messages=messages
    # )
    # print(completion)

    print(completion.choices[0].message.content, "#############")

    return completion.choices[0].message.content

if __name__ == '__main__':
    # messages=[
    #     {"role": "system", "content": "You are a helpful assistant."},
    #     {
    #         "role": "user",
    #         "content": "Write a haiku about recursion in programming."
    #     }
    # ]

    result = asyncio.run(answer_with_chatgpt(-1, -1, [], 'напиши рассказ'))
    print(result)

