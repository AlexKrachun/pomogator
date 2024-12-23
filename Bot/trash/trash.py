from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types.file import File
import asyncio
from aiogram import Router, F
from aiogram.types import Message
import os


API_TOKEN = "7618816734:AAGKGYh_-wCZqTKlDyGY2GLHLoPZWoWJey4"
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.reply("Отправьте мне фотографию, и я сохраню её на устройстве!")


SAVE_DIR = "../app/photos"


os.makedirs(SAVE_DIR, exist_ok=True)

os.makedirs(SAVE_DIR, exist_ok=True)


@dp.message(F.content_type.in_({'text', 'photo'}))

async def handle_text_and_photo(message: Message, bot: Bot):
    if message.text:

        await message.answer(f"Вы отправили текст: {message.text}")
    elif message.photo:

        await message.answer(f"Подпись к фото: {message.caption if message.caption else 'Нет подписи'}")
        await message.answer("Вы отправили фото!")


        photo = message.photo[-1]


        file_info = await bot.get_file(photo.file_id)
        file_path = os.path.join(SAVE_DIR, f"{photo.file_id}.jpg")
        await bot.download_file(file_info.file_path, destination=file_path)


        await message.answer(f"Фото сохранено как: {file_path}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

