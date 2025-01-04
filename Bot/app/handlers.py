import logging
from aiogram import types, Bot
from aiogram.types import Message
from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from aiogram.filters import Command
from Bot.additioanl.message_templates import message_templates, get_changed_context_line
from Bot.app.keyboard import inline_contexts, inline_modes, inline_pay, dalle_3_settings
from Bot.app.openai_api import request_get_topic, generate_image, get_common_gpt_complection
from Bot.app.faceswap_api import run_face_swap
from Bot.app.anthropic_api import get_claude_text_response
from Bot.app.utils.decorators import processing_guard, block_not_llm_model, block_not_dalle_model

from db.main import db_client
from Bot.app.middlewares import UserRegistrationMiddleware

from Bot.app.utils.state import id_in_processing

import base64
import aiohttp
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# logger = logging.getLogger(__name__)
logger = logging.getLogger('bot_logger')

router = Router()
router.message.middleware(UserRegistrationMiddleware())
router.callback_query.middleware(UserRegistrationMiddleware())


async def print_text_message(text: str, message: Message):
    if len(text) < 4096:

        # message.answer(text)
        try:
            await message.answer(text, parse_mode="Markdown")
        except Exception as e:
            # print('1' * 100)
            # print(e)
            await message.answer(text)


    else:
        while text != '':
            st = text[:min(4090, len(text))]

            if st.count('```') % 2 == 0:

                # message.answer(st)
                try:
                    await message.answer(st, parse_mode="Markdown")
                except Exception as e:
                    # print('2' * 100)
                    # print(e)
                    await message.answer(st)

                text = text[len(st):]
            else:

                # message.answer(st + '```')
                try:
                    await message.answer(st + '\n```', parse_mode="Markdown")
                except Exception as e:
                    # print('3' * 100)
                    # print(e)
                    await message.answer(st + '\n```')

                if not text:
                    break
                text = text[len(st):]
                if text.count('```') % 2 != 0:
                    text = '```\n' + text


@router.message(Command('contexts'))
@processing_guard
@block_not_llm_model
async def language_cmd(message: types.Message):
    try:
        reply_markup = await inline_contexts(message.from_user.id)
        await message.answer(
            message_templates['ru']['contexts'],
            reply_markup=reply_markup
        )
        logger.debug("Ответ на /contexts успешно отправлен.")
    except Exception as e:
        logger.debug(f"Ошибка в обработчике /contexts")
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
        logger.debug(f"Ошибка в обработчике /pay")
        await message.answer("Произошла ошибка при обработке команды /pay.")


@router.message(Command('mode'))
@processing_guard
async def mode_cmd(message: types.Message):
    # print("I am in /mode " * 10)
    try:
        reply_markup = await inline_modes(
            message.from_user.id,
            # curr_users_models
            db_client.get_user_model_by_tg_id(tg_id=message.from_user.id, ),
        )
        await message.answer(
            'Выберите нейросеть',
            reply_markup=reply_markup
        )
        logger.debug("Ответ на /mode успешно отправлен.")
    except Exception as e:
        logger.debug(f"Ошибка в обработчике /mode")
        await message.answer("Произошла ошибка при обработке команды /mode.")


@router.message(Command('start'))
async def start_cmd(message: types.Message, state: FSMContext):
    try:
        us_id = message.from_user.id

        current_state = await state.get_state()
        if current_state is not None:
            await state.clear()
            await message.reply('Фотография cброшена, отправьте заново изображение, на котором нужно заменить лицо.')
            if us_id in id_in_processing:
                id_in_processing.remove(us_id)
                logger.debug(f"Пользователь {us_id} завершил обработку сообщения.")
            return
        
        if db_client.get_user_model_by_tg_id(tg_id=us_id) == 'face-swap':
            await print_text_message("Привет, я бот с нейросетями. *Отправьте фотографию🖼*, на которой надо изменить лицо.\n\nПочитать про функциолан бота и наши нейросети можно в /info", message)
            return


        # await message.answer(message_templates['ru']['start'])
        await print_text_message(message_templates['ru']['start'], message)
        logger.debug("Ответ на /start успешно отправлен.")

    except Exception as e:
        logger.debug(f'Ошибка в обработчике /start')
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
            f"Логин: @{username}\n"
            f"Счет: <система оплаты в разработке>\n"
            # f"ID: {user_id}\n"
            # f"Имя: {first_name}\n"
            # f"Фамилия: {last_name}\n"
        )
        # await message.answer(profile_info)
        await print_text_message(profile_info, message)
        logger.debug("Ответ на /profile успешно отправлен.")
    except Exception as e:
        logger.debug(f'Ошибка в обработчике /profile')
        await message.answer("Произошла ошибка при обработке команды /profile.")


@router.message(Command('info'))
async def info_cmd(message: Message):
    try:
        await print_text_message(message_templates['ru']['info'], message)
        logger.debug("Ответ на /info успешно отправлен.")
    except Exception as e:
        logger.debug(f'Ошибка в обработчике /info')
        await message.answer("Произошла ошибка при обработке команды /info.")


@router.message(Command('new_context'))
@processing_guard
@block_not_llm_model
async def new_context(message: Message):
    try:
        chat_id = db_client.create_new_context_by_tg_id(tg_id=message.from_user.id)
        db_client.set_current_context_by_tg_id(tg_id=message.from_user.id, context_id=chat_id)
        # await message.answer(message_templates['ru']['delete_context'])
        await print_text_message(message_templates['ru']['delete_context'], message)

        logger.debug("Ответ на /delete_context успешно отправлен.")
    except Exception as e:
        logger.debug(f'Ошибка в обработчике /delete_context')
        await message.answer("Произошла ошибка при обработке команды /delete_context.")


@router.callback_query(F.data.startswith('context:'))
@processing_guard
@block_not_llm_model
async def handle_context_switch(callback: types.CallbackQuery):
    try:
        context_id = callback.data.removeprefix("context:")
        us_id = callback.from_user.id

        context = db_client.get_current_context_by_tg_id(tg_id=us_id)
        topic = context.name
        db_client.set_current_context_by_tg_id(tg_id=us_id, context_id=context_id)

        # await callback.message.answer(get_changed_context_line(topic))

        context_history = db_client.make_context_history(chat_id=context_id)
        logger.info(f'Выведена context_history для пользователя {us_id}')

        if str(context_id) != str(context.id):
            await callback.message.edit_text(
                'Пожалуйста, выберите контекст из списка.',
                reply_markup=await inline_contexts(us_id),
            )

        await callback.message.answer('Вот содержимое вашего контекста:')

        for msg in context_history:
            try:
                await callback.message.answer(msg, parse_mode="Markdown")
            except Exception as e:
                await callback.message.answer(msg)

        await callback.message.answer(get_changed_context_line(topic))

        await callback.answer()



    except Exception as e:
        logger.debug(f"Ошибка в обработчике handle_context_switch")
        await callback.answer("Произошла ошибка при переключении контекста.")


@router.callback_query(F.data.startswith('model:'))
@processing_guard
async def handle_model_switch(callback: types.CallbackQuery):
    try:
        model_name = callback.data.removeprefix("model:")
        us_id = callback.from_user.id
        if db_client.get_user_model_by_tg_id(us_id) != model_name:
            db_client.switch_user_model_by_tg_id(tg_id=us_id, new_model_name=model_name)

            await callback.message.edit_text(
                'Выберите подходящую вам модель.',
                reply_markup=await inline_modes(us_id, db_client.get_user_model_by_tg_id(tg_id=us_id))
            )
            if model_name in ['dall-e-3']:
                curr_size = db_client.get_dalle_shape_by_tg_id(us_id)
                curr_resolution = db_client.get_dalle_quality_by_tg_id(us_id)
                await callback.message.answer(message_templates['ru']['dall_e_3_handler'], parse_mode="Markdown",
                                              reply_markup=await dalle_3_settings(us_id, curr_resolution, curr_size))
                # await callback.message.answer('*Введите ваш запрос для генерации изображения:*', parse_mode="Markdown")
            elif model_name in ['face-swap']:
                await callback.message.answer(message_templates['ru']['face-swap-1'], parse_mode="Markdown")

            await callback.answer()
            logger.debug(f"Модель для пользователя {us_id} успешно обновлена до {model_name}")
        else:
            await callback.answer()

    except Exception as e:
        logger.debug(f"Ошибка в обработчике handle_model_switch")
        await callback.answer("Произошла ошибка при смене модели.")


@router.callback_query(F.data.startswith('quality:'))
@processing_guard
@block_not_dalle_model
async def handle_dalle_3_quality_switch(callback: types.CallbackQuery):
    try:
        curr_quality = callback.data.removeprefix("quality:")
        us_id = callback.from_user.id
        if db_client.get_dalle_quality_by_tg_id(us_id) != curr_quality:
            db_client.set_dalle_quality_by_tg_id(tg_id=us_id, dalle_quality=curr_quality)

            await callback.message.edit_text(
                message_templates['ru']['dall_e_3_handler'], parse_mode="Markdown",
                reply_markup=await dalle_3_settings(us_id, curr_quality, db_client.get_dalle_shape_by_tg_id(us_id))
            )
            await callback.answer()
            logger.debug(f"Качество для пользователя {us_id} успешно обновлена до {curr_quality}")
        else:
            await callback.answer()

    except Exception as e:
        logger.debug(f"Ошибка в обработчике handle_dalle_3_quality_switch")
        await callback.answer("Произошла ошибка при смене dalle_3_quality.")


@router.callback_query(F.data.startswith('resolution:'))
@processing_guard
@block_not_dalle_model
async def handle_dalle_3_resolution_switch(callback: types.CallbackQuery):
    try:
        curr_resolution = callback.data.removeprefix("resolution:")
        us_id = callback.from_user.id
        if db_client.get_dalle_shape_by_tg_id(us_id) != curr_resolution:
            db_client.set_dalle_shape_by_tg_id(us_id, dalle_shape=curr_resolution)

            await callback.message.edit_text(
                message_templates['ru']['dall_e_3_handler'], parse_mode="Markdown",
                reply_markup=await dalle_3_settings(user_id=us_id, quality=db_client.get_dalle_quality_by_tg_id(us_id),
                                                    resolution=curr_resolution)
            )
            await callback.answer()
            logger.debug(f"Модель для пользователя {us_id} успешно обновлена до {curr_resolution}")
        else:
            await callback.answer()

    except Exception as e:
        logger.debug(f"Ошибка в обработчике handle_dalle_3_resolution_switch")
        await callback.answer("Произошла ошибка при смене разрешения.")


async def openai_gpt_handler(message: Message, bot: Bot, state: FSMContext):
    logger.info(f"Получено сообщение для openai от пользователя {message.from_user.id}: {message.text}")
    us_id = message.from_user.id

    if not message.text:
        await message.answer("Пока мы умеем принимать только текст")
        return

    try:
        user_message = message.text
        id_in_processing.add(us_id)

        if db_client.user_has_empty_curr_context_by_tg_id(us_id):
            chat_id = db_client.get_current_context_id_by_tg_id(tg_id=us_id)

            dialog_name = await request_get_topic(user_message)

            db_client.update_dialog_neame(chat_id=chat_id, dialog_name=dialog_name)

        curr_context_id = db_client.get_current_context_by_tg_id(us_id).id

        user_teg = message.from_user.username
        db_client.add_message(chat_id=curr_context_id, role='user', text=user_message, author_name=user_teg)

        processing_message = await message.answer(message_templates['ru']['processing'])

        await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")

        response = await get_common_gpt_complection(
            db_client.get_full_dialog(curr_context_id)[-15:],
            db_client.get_user_model_by_tg_id(us_id)
        )

        logger.info(f"Получен ответ от OpenAI для пользователя {us_id}: {response}")

        await message.bot.delete_message(
            chat_id=processing_message.chat.id,
            message_id=processing_message.message_id
        )
        model_name = db_client.get_user_model_by_tg_id(us_id)
        db_client.add_message(chat_id=curr_context_id, role='assistant', text=response, author_name=model_name)

        # try:
        #     await message.answer(response, parse_mode="Markdown")
        # except Exception as e:
        #     await message.answer(response)
        await print_text_message(response, message)




    except Exception as e:
        logger.debug(f"Ошибка в обработчике openai_gpt_handler для пользователя {us_id}")
        await message.answer("Произошла ошибка при обработке вашего сообщения.")
    finally:
        if us_id in id_in_processing:
            id_in_processing.remove(us_id)
            logger.debug(f"Пользователь {us_id} завершил обработку сообщения в openai_gpt_handler.")


async def cloude_text_model_handler(message: Message, bot: Bot, state: FSMContext):
    logger.info(f"Получено сообщение для anthropic от пользователя {message.from_user.id}: {message.text}")
    us_id = message.from_user.id

    if not message.text:
        await message.answer("Пока мы умеем принимать только текст")
        return

    try:
        user_message = message.text

        id_in_processing.add(us_id)

        if db_client.user_has_empty_curr_context_by_tg_id(us_id):
            chat_id = db_client.get_current_context_id_by_tg_id(tg_id=us_id)

            dialog_name = await request_get_topic(user_message)

            db_client.update_dialog_neame(chat_id=chat_id, dialog_name=dialog_name)

        curr_context_id = db_client.get_current_context_by_tg_id(us_id).id

        user_teg = message.from_user.username

        db_client.add_message(chat_id=curr_context_id, role='user', text=user_message, author_name=user_teg)

        processing_message = await message.answer(message_templates['ru']['processing'])

        await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")

        response = await get_claude_text_response(
            db_client.get_full_dialog(curr_context_id)[-15:],
            db_client.get_user_model_by_tg_id(us_id)
        )

        logger.info(f"Получен ответ от cloude для пользователя {us_id}: {response}")

        await message.bot.delete_message(
            chat_id=processing_message.chat.id,
            message_id=processing_message.message_id
        )

        model_name = db_client.get_user_model_by_tg_id(us_id)
        db_client.add_message(chat_id=curr_context_id, role='assistant', text=response, author_name=model_name)

        # try:
        #     await message.answer(response, parse_mode="Markdown")
        # except Exception as e:
        #     await message.answer(response)
        await print_text_message(response, message)



    except Exception as e:
        logger.debug(f"Ошибка в обработчике cloude_text_model_handler для пользователя {us_id}, {e}")
        await message.answer("Произошла ошибка при обработке вашего сообщения.")
    finally:
        if us_id in id_in_processing:
            id_in_processing.remove(us_id)
            logger.debug(f"Пользователь {us_id} завершил обработку сообщения в cloude_text_model_handler.")


async def dall_e_3_handler(message: Message, bot: Bot, state: FSMContext):
    logger.info(f"Получено сообщение от пользователя {message.from_user.id}: {message.text} для генерации изображение")

    us_id = message.from_user.id
    # if us_id in id_in_processing:
    #     logger.warning(f"Пользователь {us_id} пытается отправить сообщение во время обработки.")
    #     await message.answer(message_templates['ru']['id_in_procces'])
    #     return

    try:
        id_in_processing.add(us_id)

        processing_message = await message.answer(message_templates['ru']['processing'])
        await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")

        curr_size = db_client.get_dalle_shape_by_tg_id(us_id)
        curr_quality = db_client.get_dalle_quality_by_tg_id(us_id)
        ans = await generate_image(message.text, model="dall-e-3", size=curr_size, quality=curr_quality)

        await message.bot.delete_message(
            chat_id=processing_message.chat.id,
            message_id=processing_message.message_id
        )

        if ans.startswith("http://") or ans.startswith("https://"):
            try:
                await message.answer_photo(ans, caption="Вот ваше сгенерированное изображение!")

            except Exception as e:
                await message.answer(f"Не удалось отправить изображение")
        else:
            # Если ответ openai API содержит сообщение об ошибке
            await message.answer(f"Запрос не подходит для генерации.")
            # print(ans)

        curr_size = db_client.get_dalle_shape_by_tg_id(us_id)
        curr_resolution = db_client.get_dalle_quality_by_tg_id(us_id)
        await message.answer(message_templates['ru']['dall_e_3_handler'],
                             reply_markup=await dalle_3_settings(us_id, curr_resolution, curr_size))



    except Exception as e:
        logger.debug(f"Ошибка в обработчике ret_dalle_img для пользователя {us_id}")
        await message.answer("Произошла ошибка при обработке вашего сообщения.")

    finally:
        if us_id in id_in_processing:
            id_in_processing.remove(us_id)
            logger.debug(f"Пользователь {us_id} завершил обработку сообщения.")


class FaceSwap(StatesGroup):
    photo_1_done = State()


async def face_swap_handler_first_photo(message: Message, bot: Bot, state: FSMContext):
    us_id = message.from_user.id
    if not message.photo:
        await message.answer("face-swap умеет обрабатывать только фотографии.\n\nПришлите фото")
        return

    try:
        id_in_processing.add(us_id)
        photo = message.photo[-1]
        file_id = photo.file_id

        # Получение информации о файле с сервера Telegram
        file_info = await bot.get_file(file_id)

        # Скачивание файла и преобразование в Base64
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}") as response:
                if response.status == 200:
                    base64_encoded = base64.b64encode(await response.read()).decode("utf-8")

        # Сохранение строки Base64 в состояние FSM
        await state.update_data(photo_1_done=base64_encoded)

        await message.reply(message_templates['ru']['face-swap-3'], parse_mode="Markdown")
        await state.set_state(FaceSwap.photo_1_done)

        # await message.answer(message_templates['ru']['face-swap-2'], parse_mode="Markdown")

    except Exception as e:
        # logger.debug(f"Ошибка в обработчике face_swap_handler_first_photo для пользователя {us_id}")
        await message.answer("Произошла ошибка при обработке вашей фотографии, отправьте еще раз.")
        await state.clear()
        if us_id in id_in_processing:
            id_in_processing.remove(us_id)


@router.message(FaceSwap.photo_1_done)
async def face_swap_handler_second_photo(message: Message, bot: Bot, state: FSMContext):
    processing_message = await message.reply(message_templates['ru']['processing'])
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")

    try:

        us_id = message.from_user.id

        photo = message.photo[-1]
        file_id = photo.file_id

        # Получение информации о файле с сервера Telegram
        file_info = await bot.get_file(file_id)

        # Скачивание файла и преобразование в Base64
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}") as response:
                if response.status == 200:
                    base64_encoded = base64.b64encode(await response.read()).decode("utf-8")

        # Получение первой фотографии из состояния FSM
        data = await state.get_data()
        img_1_base64 = data.get('photo_1_done')
        img_2_base64 = base64_encoded

        # Очистка состояния FSM
        await state.clear()

        url = await run_face_swap(img_1_base64, img_2_base64)
        if url == None:
            await message.answer("Произошла ошибка при генерации изображения." + '\n\n'
                                 + message_templates['ru']['face-swap-1'], parse_mode="Markdown")
            # Очистка состояния FSM
            await state.clear()
            if us_id in id_in_processing:
                id_in_processing.remove(us_id)
                logger.debug(f"Пользователь {us_id} завершил обработку сообщения.")
                # await message.answer(message_templates['ru']['face-swap-1'], parse_mode="Markdown")
            return

        await message.answer_photo(url)

        await message.answer('Следующая генерация:\n\n' + message_templates['ru']['face-swap-1'], parse_mode="Markdown")

        if us_id in id_in_processing:
            id_in_processing.remove(us_id)
            logger.debug(f"Пользователь {us_id} завершил обработку сообщения.")


    except Exception as e:
        # logger.debug(f"Ошибка в обработчике face_swap_handler_first_photo для пользователя {us_id}")
        await message.answer("Произошла ошибка при обработке вашей фотографии, отправьте фото еще раз.")
    finally:
        await message.bot.delete_message(
            chat_id=processing_message.chat.id,
            message_id=processing_message.message_id
        )


model_handler = {  # для нейронки храним хендлер
    'gpt-4o-mini': openai_gpt_handler,
    'gpt-4o': openai_gpt_handler,
    'o1-mini': openai_gpt_handler,
    'o1-preview': openai_gpt_handler,
    'dall-e-3': dall_e_3_handler,
    'face-swap': face_swap_handler_first_photo,
    'claude-3-5-sonnet-latest': cloude_text_model_handler,
    'claude-3-5-haiku-latest': cloude_text_model_handler
}


@router.message()
@processing_guard
async def echo_msg(message: Message, bot: Bot, state: FSMContext):
    try:
        # регистрация
        us_id = message.from_user.id
        if db_client.user_is_new_by_tg_id(us_id):
            db_client.add_user(name=message.from_user.full_name, tg_id=us_id,
                               last_used_model='gpt-4o-mini')  # возможно full_name пустой
            chat_id = db_client.create_new_context_by_tg_id(tg_id=us_id)  # новый чат с названием 'Пустой чат'
            db_client.set_current_context_by_tg_id(tg_id=us_id, context_id=chat_id)

    except Exception as e:
        logger.debug(f'Ошибка: пользователь не зарегестрирован')
        await message.answer("Произошла ошибка при обработке команды.")

    last_used_model = db_client.get_user_model_by_tg_id(message.from_user.id)
    logging.debug(f'Дебаг - {last_used_model}')

    await model_handler[last_used_model](message, bot, state)
