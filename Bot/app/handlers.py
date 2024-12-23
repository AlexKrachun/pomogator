import logging
from aiogram import types
from aiogram.types import Message
from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from aiogram.filters import Command
from Bot.additioanl.message_templates import message_templates, get_changed_context_line
from Bot.app.keyboard import inline_contexts, inline_modes, inline_pay
from Bot.app.openai_api import get_completion, request_get_topic, generate_image

from db.main import db_client

import uuid

from Bot.app.utils.state import *

logger = logging.getLogger(__name__)


router = Router()


class DalleGeneration(StatesGroup):
    promt = State()


@router.message(Command('img'))
async def get_promt(message: types.Message, state: FSMContext):
    await state.set_state(DalleGeneration.promt)
    await message.answer('Введите ваш запрос для генерации изображения:')


@router.message(DalleGeneration.promt)
async def ret_dalle_img(message: types.Message, state: FSMContext):
    await state.update_data(promt=message.text)
    data = await state.get_data()
    # await message.answer(f'Ваш промт: {data}')
    await state.clear()

    dalle_promt = data['promt']

    us_id = message.from_user.id
    if us_id in id_in_processing:
        # logger.warning(f"Пользователь {us_id} пытается отправить сообщение во время обработки.")
        await message.answer(message_templates['ru']['id_in_procces'])
        return

    try:
        id_in_processing.add(us_id)
        processing_message = await message.answer(message_templates['ru']['processing'])

        await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")


        ans = await generate_image(dalle_promt)

        if ans.startswith("http://") or ans.startswith("https://"):
            try:
                await message.answer_photo(ans, caption="Вот ваше сгенерированное изображение!")
                await message.bot.delete_message(
                    chat_id=processing_message.chat.id,
                    message_id=processing_message.message_id
                )
            except Exception as e:
                await message.answer(f"Не удалось отправить изображение: {e}")
        else:
            # Если ответ openai API содержит сообщение об ошибке
            await message.answer(ans)

    except Exception as e:
        logger.exception(f"Ошибка в обработчике ret_dalle_img для пользователя {us_id}: {e}")
        await message.answer("Произошла ошибка при обработке вашего сообщения.")

    finally:
        if us_id in id_in_processing:
            id_in_processing.remove(us_id)
            logger.debug(f"Пользователь {us_id} завершил обработку сообщения.")


@router.message(Command('contexts'))
async def language_cmd(message: types.Message):
    try:
        reply_markup = await inline_contexts(message.from_user.id)
        await message.answer(
            message_templates['ru']['contexts'],
            reply_markup=reply_markup
        )
        logger.debug("Ответ на /contexts успешно отправлен.")
    except Exception as e:
        logger.exception(f"Ошибка в обработчике /contexts: {e}")
        await message.answer("Произошла ошибка при обработке команды /contexts.")


@router.message(Command('pay'))
async def pay_cmd(message: types.Message):
    try:
        await message.answer(
            'Пока тут все for free, мы возьмем от вас деньги в next time.',
            reply_markup=inline_pay
        )
        logger.debug("Ответ на /pay успешно отправлен.")
    except Exception as e:
        logger.exception(f"Ошибка в обработчике /pay: {e}")
        await message.answer("Произошла ошибка при обработке команды /pay.")


@router.message(Command('mode'))
async def mode_cmd(message: types.Message):
    try:
        reply_markup = await inline_modes(
            message.from_user.id,
            # curr_users_models
            db_client.get_user_model_by_tg_id(tg_id=message.from_user.id,),
        )
        await message.answer(
            'Выберите подходящую вам модель gpt.',
            reply_markup=reply_markup
        )
        logger.debug("Ответ на /mode успешно отправлен.")
    except Exception as e:
        logger.exception(f"Ошибка в обработчике /mode: {e}")
        await message.answer("Произошла ошибка при обработке команды /mode.")


@router.message(Command('start'))
async def start_cmd(message: types.Message):
    try:
        # username = message.from_user.username
        # messages[username] = []
        # language = user_languages.get(message.from_user.id, 'ru')
        await message.answer(message_templates['ru']['start'])
        logger.debug("Ответ на /start успешно отправлен.")
    except Exception as e:
        logger.exception(f'Ошибка в обработчике /start: {e}')
        await message.answer("Произошла ошибка при обработке команды /start.")


@router.message(Command('profile'))
async def profile_command(message: Message):
    try:
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
        logger.debug("Ответ на /profile успешно отправлен.")
    except Exception as e:
        logger.exception(f'Ошибка в обработчике /profile: {e}')
        await message.answer("Произошла ошибка при обработке команды /profile.")


@router.message(Command('help'))
async def help_cmd(message: Message):
    try:
        # language = user_languages.get(message.from_user.id, 'ru')
        await message.answer(message_templates['ru']['help'])
        logger.debug("Ответ на /help успешно отправлен.")
    except Exception as e:
        logger.exception(f'Ошибка в обработчике /help: {e}')
        await message.answer("Произошла ошибка при обработке команды /help.")


@router.message(Command('new_context'))
async def new_context(message: Message):
    try:
        # curr_users_context[message.from_user.id] = ''
        chat_id = db_client.create_new_context_by_tg_id(tg_id=message.from_user.id)
        db_client.set_current_context_by_tg_id(tg_id=message.from_user.id, another_context_id=chat_id)
        await message.answer(message_templates['ru']['delete_context'])
        logger.debug("Ответ на /delete_context успешно отправлен.")
    except Exception as e:
        logger.exception(f'Ошибка в обработчике /delete_context: {e}')
        await message.answer("Произошла ошибка при обработке команды /delete_context.")


@router.callback_query(F.data.startswith('context:'))
async def handle_context_switch(callback: types.CallbackQuery):
    try:
        context_id = callback.data.removeprefix("context:")
        us_id = callback.from_user.id
        us_name = callback.from_user.username or "неизвестен"
        # topic = from_context_id_get_topic.get(context_id, "Неизвестная тема")
        topic = db_client.get_current_context_by_tg_id(tg_id=us_id).name
        # curr_users_context[us_id] = context_id
        db_client.set_current_context_by_tg_id(tg_id=us_id, another_context_id=context_id)

        await callback.answer()
        await callback.message.answer(get_changed_context_line(topic))

        # context_history = make_context_history(all_contexts, context_id, us_name)
        context_history = db_client.make_context_history(chat_id=context_id)
        logger.info(f'Выведена context_history для пользователя {us_id}')

        try:
            await callback.message.answer(context_history, parse_mode="Markdown")
        except Exception as e:
            await callback.message.answer(context_history)
    except Exception as e:
        logger.exception(f"Ошибка в обработчике handle_context_switch: {e}")
        await callback.answer("Произошла ошибка при переключении контекста.")


@router.callback_query(F.data.startswith('model:'))
async def handle_model_switch(callback: types.CallbackQuery):
    try:
        model_name = callback.data.removeprefix("model:")
        us_id = callback.from_user.id

        if db_client.get_user_model_by_tg_id(us_id) != model_name:

            if model_name in ['gpt-4o-mini', 'gpt-4o']:
                db_client.switch_user_model_by_tg_id(tg_id=us_id, new_model_name=model_name)

            await callback.answer()
            await callback.message.edit_text(
                'Выберите подходящую вам модель gpt.',
                reply_markup=await inline_modes(us_id, db_client.get_user_model_by_tg_id(tg_id=us_id))
            )
            logger.debug(f"Модель для пользователя {us_id} успешно обновлена до {model_name}")
    except Exception as e:
        logger.exception(f"Ошибка в обработчике handle_model_switch: {e}")
        await callback.answer("Произошла ошибка при смене модели.")


@router.message()
async def echo_msg(message: Message):
    logger.info(f"Получено сообщение от пользователя {message.from_user.id}: {message.text}")
    us_id = message.from_user.id
    user_message = message.text

    if us_id in id_in_processing:
        # logger.warning(f"Пользователь {us_id} пытается отправить сообщение во время обработки.")
        await message.answer(message_templates['ru']['id_in_procces'])
        return
    if not user_message:
        # logger.warning(f"Пользователь {us_id} отправил пустое сообщение.")
        return


    try:
        id_in_processing.add(us_id)

        # if us_id not in id_not_new_users:
        # print("n" * 100, db_client.user_is_new_by_tg_id(us_id))
        # print(db_client.get_user_by_tg_id(us_id))
        if db_client.user_is_new_by_tg_id(us_id):

            # id_not_new_users.add(us_id)
            db_client.add_user(name=message.from_user.full_name, tg_id=us_id)  # возможно full_name пустой
            # new_hash = generate_unique_number()

            # get_users_contexts[us_id] = [new_hash]
            # curr_users_context[us_id] = new_hash
            
            dialog_name = await request_get_topic(user_message)
            chat_id = db_client.create_new_context_by_tg_id(tg_id=us_id)
            db_client.update_dialog_neame(chat_id=chat_id, dialog_name=dialog_name)
            db_client.set_current_context_by_tg_id(tg_id=us_id, another_context_id=chat_id)

            # all_contexts[new_hash] = [{"role": "user", "content": user_message}]
            db_client.add_message(chat_id=chat_id, role='user', text=user_message)

        # elif curr_users_context.get(us_id) == '':
        elif db_client.user_has_empty_curr_context_by_tg_id(us_id):
            
            dialog_name = await request_get_topic(user_message)
            
            chat_id = db_client.get_current_context_by_tg_id(tg_id=us_id).id
            
            db_client.update_dialog_neame(chat_id=chat_id, dialog_name=dialog_name)
            
            db_client.add_message(chat_id=chat_id, role='user', text=user_message)

        else:
            # all_contexts[curr_users_context[us_id]].append({"role": "user", "content": user_message})
            curr_context_id = db_client.get_current_context_by_tg_id(us_id).id
            db_client.add_message(chat_id=curr_context_id, role='user', text=user_message)

        curr_context_id = db_client.get_current_context_by_tg_id(us_id).id

        processing_message = await message.answer(message_templates['ru']['processing'])

        await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")

        response = await get_completion(
            db_client.get_full_dialog(curr_context_id)[-10:],
            # get_user_model(us_id, curr_users_models)
            db_client.get_user_model_by_tg_id(us_id)
        )

        logger.info(f"Получен ответ от OpenAI для пользователя {us_id}: {response}")

        try:
            await message.answer(response, parse_mode="Markdown")
        except Exception as e:
            await message.answer(response)
        # all_contexts[curr_context_id].append({"role": "assistant", "content": response})
        db_client.add_message(chat_id=curr_context_id, role='assistant', text=response)

        await message.bot.delete_message(
            chat_id=processing_message.chat.id,
            message_id=processing_message.message_id
        )

    except Exception as e:
        logger.exception(f"Ошибка в обработчике echo_msg для пользователя {us_id}: {e}")
        await message.answer("Произошла ошибка при обработке вашего сообщения.")
    finally:
        if us_id in id_in_processing:
            id_in_processing.remove(us_id)
            logger.debug(f"Пользователь {us_id} завершил обработку сообщения.")
