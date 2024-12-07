import os
import logging
from aiogram import types
from aiogram.types import Message
from aiogram import Router, F
from openai import AsyncOpenAI

from dotenv import load_dotenv

from aiogram.filters import Command
from additioanl.message_templates import message_templates, get_changed_context_line
from app.keyboard import inline_contexts, inline_modes, inline_pay, chatgpt_models
from app.openai_api_test import get_completion, request_get_topic

import uuid


def generate_unique_number():
    return str(uuid.uuid4())


def get_user_model(user_id, curr_users_models):
    if user_id not in curr_users_models:
        return 'gpt-4o-mini'

    return curr_users_models[user_id]


def make_context_history(all_contexts_dict, context_id, us_name):
    context_history = ''
    for d in all_contexts_dict[context_id]:
        if d['role'] == 'user':
            context_history += '😍' + us_name + ':'
        elif d['role'] == 'assistant':
            context_history += '🤖ChatGPT:'
        context_history += '\n'
        context_history += d['content']
        context_history += '\n'
        context_history += '\n'

    context_history += 'Контекст переключен'

    return context_history


user_languages = {}
messages = dict()
all_contexts = dict()  # context_id -> JSON
get_users_contexts = dict()  # user -> [id_1,id_2,id_3,id_4]
curr_users_context = dict()  # user -> curr_id
curr_users_models = dict()
from_context_id_get_topic = dict()  # context_id -> topic
router = Router()


id_in_processing = set()
id_not_new_users = set()


@router.message(Command('contexts'))
async def language_cmd(message: types.Message):
    await message.answer(
        message_templates['ru']['contexts'],
        reply_markup=await inline_contexts(message.from_user.id, from_context_id_get_topic, get_users_contexts)
    )


@router.message(Command('pay'))
async def pay_cmd(message: types.Message):
    await message.answer('Пока тут все for free, мы возьмем от вас деньги в next time.', reply_markup=inline_pay)


@router.message(Command('mode'))
async def mode_cmd(message: types.Message):
    await message.answer('Выберите подходящую вам модель gpt.',
                         reply_markup=await inline_modes(message.from_user.id, curr_users_models))


@router.message(Command('start'))
async def start_cmd(message: types.Message):
    try:
        username = message.from_user.username
        messages[username] = []
        language = user_languages.get(message.from_user.id, 'ru')
        await message.answer(message_templates[language]['start'])
    except Exception as e:
        logging.error(f'Error in start_cmd: {e}')


@router.message(Command('profile'))
async def profile_command(message: Message):
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


@router.message(Command('help'))
async def help_cmd(message: Message):
    language = user_languages.get(message.from_user.id, 'ru')
    await message.answer(message_templates[language]['help'])


@router.message(Command('about'))
async def about_cmd(message: Message):
    language = user_languages.get(message.from_user.id, 'ru')
    await message.answer(message_templates[language]['about'])


@router.message(Command('delete_context'))
async def about_cmd(message: Message):
    curr_users_context[message.from_user.id] = ''
    await message.answer(message_templates['ru']['delete_context'])


@router.callback_query(F.data.startswith('context:'))
async def handle_context_switch(callback: types.CallbackQuery):
    print(callback.data)
    context_id = callback.data.removeprefix("context:")

    us_id = callback.from_user.id
    us_name = callback.from_user.username
    topic = from_context_id_get_topic[context_id]
    curr_users_context[us_id] = context_id

    await callback.answer()
    await callback.message.answer(get_changed_context_line(topic))

    context_history = make_context_history(all_contexts, context_id, us_name)
    await callback.message.answer(context_history)


@router.callback_query(F.data.startswith('model:'))
async def handle_model_switch(callback: types.CallbackQuery):
    model_name = callback.data.removeprefix("model:")
    us_id = callback.from_user.id
    print(model_name, us_id)

    # Сохраняем выбранную модель для пользователя
    curr_users_models[us_id] = model_name

    await callback.answer()
    await callback.message.edit_text('Выберите подходящую вам модель gpt. ',
                                     reply_markup=await inline_modes(us_id, curr_users_models))


# @router.message()
@router.message(F.content_type.in_({'text', 'photo'}))
async def echo_msg(message):
    us_id = message.from_user.id
    user_message = message.text
    print(message.photo)

    if us_id in id_in_processing:
        await message.answer(message_templates['ru']['id_in_procces'])
        return 0
    if not user_message:
        return 0

    try:
        id_in_processing.add(us_id)
        print(message.from_user.username, " - ", user_message, message.from_user.id)

        if us_id not in id_not_new_users:
            id_not_new_users.add(us_id)
            new_hash = generate_unique_number()
            get_users_contexts[us_id] = [new_hash]
            curr_users_context[us_id] = new_hash
            all_contexts[new_hash] = [{"role": "user", "content": message.text}]
            from_context_id_get_topic[new_hash] = await request_get_topic(message.text)

        elif curr_users_context[us_id] == '':
            new_hash = generate_unique_number()
            get_users_contexts[us_id].append(new_hash)
            curr_users_context[us_id] = new_hash
            all_contexts[new_hash] = [{"role": "user", "content": message.text}]

            from_context_id_get_topic[new_hash] = await request_get_topic(message.text)
        else:
            all_contexts[curr_users_context[us_id]].append({"role": "user", "content": message.text})

        curr_context_id = curr_users_context[us_id]


        processing_message = await message.answer(message_templates['ru']['processing'])
        await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
        # response = "ЗАГЛУШКА"
        response = await get_completion(all_contexts[curr_context_id][-10:],
                                        get_user_model(us_id, curr_users_models))
        await message.answer(response)

        all_contexts[curr_context_id].append({"role": "assistant", "content": response})

        await message.bot.delete_message(chat_id=processing_message.chat.id, message_id=processing_message.message_id)

        id_in_processing.remove(us_id)
    finally:
        if us_id in id_in_processing:
            id_in_processing.remove(us_id)