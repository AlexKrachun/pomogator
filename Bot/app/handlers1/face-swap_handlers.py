'''
    DEAD CODE =-)
'''

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

    except Exception:
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


    except Exception:
        # logger.debug(f"Ошибка в обработчике face_swap_handler_first_photo для пользователя {us_id} : {e}")
        await message.answer("Произошла ошибка при обработке вашей фотографии, отправьте фото еще раз.")
    finally:
        await message.bot.delete_message(
            chat_id=processing_message.chat.id,
            message_id=processing_message.message_id
        )
