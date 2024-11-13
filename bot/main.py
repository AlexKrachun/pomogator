import logging
import time
import asyncio  # Импортируем asyncio для запуска асинхронной функции
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand

from aiogram.filters import Command
import openai
from config import bot_token, api_key
from message_templates import message_templates

# from ..backend.gpt_api import answer_with_chatgpt

logging.basicConfig(level=logging.INFO)

bot = Bot(token=bot_token)
dp = Dispatcher()

openai.api_key = api_key


##################3



from openai import OpenAI
import os
from dotenv import load_dotenv



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


####################










messages = {}
user_languages = {}  # Track user's current language

# Language selection keyboard
language_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="English🇬🇧", callback_data='en'),
            InlineKeyboardButton(text="Русский🇷🇺", callback_data='ru')
        ]
    ]
)

# Регистрация команд
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Запустить бота"),
        BotCommand(command="/help", description="Показать справку"),
        BotCommand(command="/profile", description="Показать профиль"),
    ]
    await bot.set_my_commands(commands)
'''        BotCommand(command="/language", description="Показать профиль")
'''



@dp.message(Command('language'))
async def language_cmd(message: types.Message):
    await message.answer(
        message_templates['ru']['language_selection'],
        reply_markup=language_keyboard
    )



@dp.message(Command('start'))
async def start_cmd(message: types.Message):
    try:
        username = message.from_user.username
        messages[username] = []
        language = user_languages.get(message.from_user.id, 'ru')
        await message.answer(message_templates[language]['start'])
    except Exception as e:
        logging.error(f'Error in start_cmd: {e}')



@dp.message(Command('profile'))
async def profile_command(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or "не указан"
    first_name = message.from_user.first_name or "не указан"
    last_name = message.from_user.last_name or "не указан"

    profile_info = (
        f"👤 Профиль пользователя:\n"
        f"ID: {user_id}\n"
        f"Имя: {first_name}\n"
        f"Фамилия: {last_name}\n"
        f"Логин: @{username}"
    )
    await message.answer(profile_info)


@dp.message(Command('help'))
async def help_cmd(message: types.Message):
    language = user_languages.get(message.from_user.id, 'ru')
    await message.answer(message_templates[language]['help'])


@dp.message(Command('about'))
async def about_cmd(message: types.Message):
    language = user_languages.get(message.from_user.id, 'ru')
    await message.answer(message_templates[language]['about'])


@dp.message()
async def echo_msg(message: types.Message):
    try:
        user_message = message.text
        # print(type(user_message))
        # print(user_message)
        userid = message.from_user.username
        print(userid)

        language = user_languages.get(message.from_user.id, 'ru')
        processing_message = await message.answer(message_templates[language]['processing'])
        await bot.send_chat_action(chat_id=message.chat.id, action="typing")

        print("-----------------------------------")
        gpt_answer = await answer_with_chatgpt(user_id=-1, chat_id=-1, messages=[], prompt=user_message, model='gpt-4o-mini')
        print("+++++++++++++++++++++++++++++++++")

        
        await bot.delete_message(chat_id=processing_message.chat.id, message_id=processing_message.message_id)
        while gpt_answer != '':
            await message.answer(gpt_answer[:min(4000, len(gpt_answer))])
            gpt_answer = gpt_answer[min(4000, len(gpt_answer)):]


    except:
        pass




if __name__ == '__main__':
    async def main():
        await set_commands(bot)
        await dp.start_polling(bot)  # Добавляем await перед вызовом start_polling

    asyncio.run(main())  # Запускаем основную функцию