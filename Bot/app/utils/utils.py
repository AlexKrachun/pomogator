from aiogram.types import Message



async def print_text_message(text: str, message: Message):
    if len(text) < 4096:

        # message.answer(text)
        try:
            await message.answer(text, parse_mode="Markdown")
        except Exception:
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
                except Exception:
                    # print('2' * 100)
                    # print(e)
                    await message.answer(st)

                text = text[len(st):]
            else:

                # message.answer(st + '```')
                try:
                    await message.answer(st + '\n```', parse_mode="Markdown")
                except Exception:
                    # print('3' * 100)
                    # print(e)
                    await message.answer(st + '\n```')

                if not text:
                    break
                text = text[len(st):]
                if text.count('```') % 2 != 0:
                    text = '```\n' + text
