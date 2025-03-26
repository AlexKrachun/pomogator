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

from utils.utils import print_text_message

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

async def dall_e_3_handler(message: Message, bot: Bot):
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
                await message.answer(f"Не удалось отправить изображение : {e}")
        else:
            # Если ответ openai API содержит сообщение об ошибке
            await message.answer("Запрос не подходит для генерации")
            # print(ans)

        curr_size = db_client.get_dalle_shape_by_tg_id(us_id)
        curr_resolution = db_client.get_dalle_quality_by_tg_id(us_id)
        await message.answer(message_templates['ru']['dall_e_3_handler'],
                             reply_markup=await dalle_3_settings(us_id, curr_resolution, curr_size),
                             parse_mode="Markdown")



    except Exception as e:
        logger.debug(f"Ошибка в обработчике ret_dalle_img для пользователя {us_id} : {e}")
        await message.answer("Произошла ошибка при обработке вашего сообщения.")

    finally:
        if us_id in id_in_processing:
            id_in_processing.remove(us_id)
            logger.debug(f"Пользователь {us_id} завершил обработку сообщения.")
