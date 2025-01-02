import logging
from aiogram import types, Bot
from aiogram.types import Message
from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from aiogram.filters import Command
from Bot.additioanl.message_templates import message_templates, get_changed_context_line
from Bot.app.keyboard import inline_contexts, inline_modes, inline_pay, dalle_3_settings
from Bot.app.openai_api import get_completion, request_get_topic, generate_image, get_common_gpt_complection
from Bot.app.faceswap_api import run_face_swap

from db.main import db_client

from Bot.app.utils.state import id_in_processing


from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN')


logger = logging.getLogger(__name__)

router = Router()


# class FaceSwap(StatesGroup):
#      = State()

# class DalleGeneration(StatesGroup):
#     promt = State()
#
#
# @router.message(Command('img'))
# async def get_promt(message: types.Message, state: FSMContext):
#     await state.set_state(DalleGeneration.promt)
#     await message.answer('Введите ваш запрос для генерации изображения:')

#
# @router.message(DalleGeneration.promt)
# async def ret_dalle_img(message: types.Message, state: FSMContext):
#     await state.update_data(promt=message.text)
#     data = await state.get_data()
#     # await message.answer(f'Ваш промт: {data}')
#     await state.clear()
#
#     dalle_promt = data['promt']
#     if dalle_promt == '/start':
#         await message.answer(message_templates['ru']['start'])
#         return None


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
            db_client.get_user_model_by_tg_id(tg_id=message.from_user.id, ),
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
        # регистрация
        us_id = message.from_user.id
        if db_client.user_is_new_by_tg_id(us_id):
            db_client.add_user(name=message.from_user.full_name, tg_id=us_id,
                               last_used_model='gpt-4o-mini')  # возможно full_name пустой
            chat_id = db_client.create_new_context_by_tg_id(tg_id=us_id)  # новый чат с названием 'Пустой чат'
            db_client.set_current_context_by_tg_id(tg_id=us_id, context_id=chat_id)

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
        await message.answer(message_templates['ru']['help'])
        logger.debug("Ответ на /help успешно отправлен.")
    except Exception as e:
        logger.exception(f'Ошибка в обработчике /help: {e}')
        await message.answer("Произошла ошибка при обработке команды /help.")


@router.message(Command('new_context'))
async def new_context(message: Message):
    try:
        chat_id = db_client.create_new_context_by_tg_id(tg_id=message.from_user.id)
        db_client.set_current_context_by_tg_id(tg_id=message.from_user.id, context_id=chat_id)
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

        topic = db_client.get_current_context_by_tg_id(tg_id=us_id).name
        db_client.set_current_context_by_tg_id(tg_id=us_id, context_id=context_id)

        await callback.answer()
        await callback.message.answer(get_changed_context_line(topic))

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
            db_client.switch_user_model_by_tg_id(tg_id=us_id, new_model_name=model_name)

            await callback.message.edit_text(
                'Выберите подходящую вам модель.',
                reply_markup=await inline_modes(us_id, db_client.get_user_model_by_tg_id(tg_id=us_id))
            )
            if model_name in ['dall-e-3']:
                curr_size = db_client.get_dalle_shape_by_tg_id(us_id)
                curr_resolution = db_client.get_dalle_quality_by_tg_id(us_id)
                await callback.message.answer(message_templates['ru']['dall_e_3_handler'],
                                              reply_markup=await dalle_3_settings(us_id, curr_resolution,curr_size))

            await callback.answer()
            logger.debug(f"Модель для пользователя {us_id} успешно обновлена до {model_name}")
        else:
            await callback.answer()

    except Exception as e:
        logger.exception(f"Ошибка в обработчике handle_model_switch: {e}")
        await callback.answer("Произошла ошибка при смене модели.")


@router.callback_query(F.data.startswith('quality:'))
async def handle_dalle_3_quality_switch(callback: types.CallbackQuery):
    try:
        curr_quality = callback.data.removeprefix("quality:")
        us_id = callback.from_user.id
        if db_client.get_dalle_quality_by_tg_id(us_id) != curr_quality:
            db_client.set_dalle_quality_by_tg_id(tg_id=us_id, dalle_quality=curr_quality)

            await callback.message.edit_text(
                'Выберите подходящие вам параметры.',
                reply_markup=await dalle_3_settings(us_id, curr_quality, db_client.get_dalle_shape_by_tg_id(us_id))
            )
            await callback.answer()
            logger.debug(f"Качество для пользователя {us_id} успешно обновлена до {curr_quality}")
        else:
            await callback.answer()

    except Exception as e:
        logger.exception(f"Ошибка в обработчике handle_dalle_3_quality_switch: {e}")
        await callback.answer("Произошла ошибка при смене dalle_3_quality.")


@router.callback_query(F.data.startswith('resolution:'))
async def handle_dalle_3_resolution_switch(callback: types.CallbackQuery):
    try:
        curr_resolution = callback.data.removeprefix("resolution:")
        us_id = callback.from_user.id
        if db_client.get_dalle_shape_by_tg_id(us_id) != curr_resolution:
            db_client.set_dalle_shape_by_tg_id(us_id, dalle_shape=curr_resolution)

            await callback.message.edit_text(
                'Выберите подходящие вам разрешение.',
                reply_markup=await dalle_3_settings(user_id=us_id, quality=db_client.get_dalle_quality_by_tg_id(us_id), resolution=curr_resolution)
            )
            await callback.answer()
            logger.debug(f"Модель для пользователя {us_id} успешно обновлена до {curr_resolution}")
        else:
            await callback.answer()

    except Exception as e:
        logger.exception(f"Ошибка в обработчике handle_dalle_3_resolution_switch: {e}")
        await callback.answer("Произошла ошибка при смене разрешения.")


async def openai_gpt_handler(message: Message, bot: Bot, state: FSMContext):
    logger.info(f"Получено сообщение от пользователя {message.from_user.id}: {message.text}")
    us_id = message.from_user.id
    user_message = message.text
    id_in_processing.add(us_id)

    try:
        if db_client.user_has_empty_curr_context_by_tg_id(us_id):
            chat_id = db_client.get_current_context_id_by_tg_id(tg_id=us_id)

            dialog_name = await request_get_topic(user_message)

            db_client.update_dialog_neame(chat_id=chat_id, dialog_name=dialog_name)

        curr_context_id = db_client.get_current_context_by_tg_id(us_id).id

        db_client.add_message(chat_id=curr_context_id, role='user', text=user_message)

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

        try:
            await message.answer(response, parse_mode="Markdown")
        except Exception as e:
            await message.answer(response)

        db_client.add_message(chat_id=curr_context_id, role='assistant', text=response)


    except Exception as e:
        logger.exception(f"Ошибка в обработчике openai_gpt_handler для пользователя {us_id}: {e}")
        await message.answer("Произошла ошибка при обработке вашего сообщения.")
    finally:
        if us_id in id_in_processing:
            id_in_processing.remove(us_id)
            logger.debug(f"Пользователь {us_id} завершил обработку сообщения в openai_gpt_handler.")


async def dall_e_3_handler(message: Message, bot: Bot, state: FSMContext):
    logger.info(f"Получено сообщение от пользователя {message.from_user.id}: {message.text} для генерации изображение")

    us_id = message.from_user.id
    if us_id in id_in_processing:
        logger.warning(f"Пользователь {us_id} пытается отправить сообщение во время обработки.")
        await message.answer(message_templates['ru']['id_in_procces'])
        return

    try:
        id_in_processing.add(us_id)

        processing_message = await message.answer(message_templates['ru']['processing'])
        await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")

        curr_size = db_client.get_dalle_shape_by_tg_id(us_id)
        curr_quality = db_client.get_dalle_quality_by_tg_id(us_id)
        ans = await generate_image(message.text, model="dall-e-3", size=curr_size, quality=curr_quality)

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
            # await message.answer("Слишком пошлый запрос")
                await message.answer("Слишком пошлый запрос")


        curr_size = db_client.get_dalle_shape_by_tg_id(us_id)
        curr_resolution = db_client.get_dalle_quality_by_tg_id(us_id)
        await message.answer(message_templates['ru']['dall_e_3_handler'],
                                      reply_markup=await dalle_3_settings(us_id, curr_resolution, curr_size))



    except Exception as e:
        logger.exception(f"Ошибка в обработчике ret_dalle_img для пользователя {us_id}: {e}")
        await message.answer("Произошла ошибка при обработке вашего сообщения.")

    finally:
        if us_id in id_in_processing:
            id_in_processing.remove(us_id)
            logger.debug(f"Пользователь {us_id} завершил обработку сообщения.")




# async def face_swap_handler(message: Message, bot: Bot):
    # file = await bot.get_file(file_id)
    # file_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{file.file_path}"
    # await file.download_to('downloaded_photo.jpg')
    #  await message.answer(f"Пришлите фотографию, которую будем менять")

        



# class DalleGeneration(StatesGroup):
#     promt = State()
#
#
# @router.message(Command('img'))
# async def get_promt(message: types.Message, state: FSMContext):
#     await state.set_state(DalleGeneration.promt)
#     await message.answer('Введите ваш запрос для генерации изображения:')

#
# @router.message(DalleGeneration.promt)
# async def ret_dalle_img(message: types.Message, state: FSMContext):
#     await state.update_data(promt=message.text)
#     data = await state.get_data()
#     # await message.answer(f'Ваш промт: {data}')
#     await state.clear()
#
#     dalle_promt = data['promt']
#     if dalle_promt == '/start':
#         await message.answer(message_templates['ru']['start'])
#         return None



class FaceSwap(StatesGroup):
    photo_1_done = State()
    
# async def get_promt(message: types.Message, state: FSMContext):
#     await state.set_state(DalleGeneration.promt)
#     await message.answer('Введите ваш запрос для генерации изображения:')


async def face_swap_handler_first_photo(message: Message, bot: Bot, state: FSMContext):
    
    photo = message.photo[-1]
    file_id = photo.file_id

    file = await bot.get_file(file_id)
    file_path = file.file_path

    img_1_url = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}'
    await state.set_state(FaceSwap.photo_1_done)
    await state.update_data(photo_1_done=img_1_url)
    await message.answer('Пришлите фотографию с желаемым лицом')
    
    
@router.message(FaceSwap.photo_1_done)
async def face_swap_handler_second_photo(message: Message, bot: Bot, state: FSMContext):
    photo = message.photo[-1]
    file_id = photo.file_id

    file = await bot.get_file(file_id)
    file_path = file.file_path

    img_2_url = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}'
    
    data = await state.get_data()
    img_1_url = data['photo_1_done']

    swapped_img_url = await run_face_swap(main_img_url=img_1_url, face_img_url=img_2_url)
    
    await message.answer(f'{swapped_img_url=}')

    
# async def face_swap_handler(message: Message, bot: Bot, state: FSMContext):
#     print('+' * 1000)

    # print(file_url)
    # await message.answer(f'Ссылка на ваше изображение: {file_url}')



model_handler = {  # для нейронки храним хендлер
    'gpt-4o-mini': openai_gpt_handler,
    'gpt-4o': openai_gpt_handler,
    'o1-mini': openai_gpt_handler,
    'o1-preview': openai_gpt_handler,
    'dall-e-3': dall_e_3_handler,
    'face-swap': face_swap_handler_first_photo
}


@router.message()
async def echo_msg(message: Message, bot: Bot, state: FSMContext):
    
    # try:
    #     # регистрация
    #     us_id = message.from_user.id
    #     if db_client.user_is_new_by_tg_id(us_id):
    #         db_client.add_user(name=message.from_user.full_name, tg_id=us_id,
    #                            last_used_model='gpt-4o-mini')  # возможно full_name пустой
    #         chat_id = db_client.create_new_context_by_tg_id(tg_id=us_id)  # новый чат с названием 'Пустой чат'
    #         db_client.set_current_context_by_tg_id(tg_id=us_id, context_id=chat_id)

    #     await message.answer(message_templates['ru']['start'])
    #     logger.debug("Ответ на /start успешно отправлен.")
    # except Exception as e:
    #     logger.exception(f'Ошибка в обработчике /start: {e}')
    #     await message.answer("Произошла ошибка при обработке команды /start.")

    
    us_id = message.from_user.id
    user_message = message.text

    print('1' * 100)
    if us_id in id_in_processing:
        await message.answer(message_templates['ru']['id_in_procces'])
        return
    
    print('2' * 100)

    last_used_model = db_client.get_user_model_by_tg_id(message.from_user.id)
    print(f'Дебаг - {last_used_model}')

    await model_handler[last_used_model](message, bot, state)
