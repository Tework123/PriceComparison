from aiogram import executor, types
from create_bot import dp, bot
import handlers
import database
import asyncio
import every_day_req


async def on_startup(_):
    print('БОТ вышел в онлайн')


async def send_message(id, text):
    await bot.send_message(id, text)



database.db_create()
handlers.register_handlers(dp)

# async def main():
#     task1 = asyncio.create_task(every_day_req.every_day_request(10))


if __name__ == '__main__':
    # asyncio.run(main())
    # executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    loop = asyncio.get_event_loop()
    # loop.create_task(every_day_req.every_day_request(86400))  # поставим 10 секунд, в качестве теста
    loop.create_task(every_day_req.every_day_request(10000))
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

# @dp.message_handler()
# async def msg_send_shop(message: types.Message):
#     print(message.text[:8])
#     await message.answer('Поймал')


# await message.reply('Пишите в личку') #копирует сообщение пользователя дополнительно

# await message.answer('hello') # просто ответ (и в личку, и в группу)

# await bot.send_message(message.from_user.id,'DADA_I') # отвечает только в личку


# await message.answer_photo(photo='https://m.media-amazon.com/images/M/MV5BNmQ0ODBhMjUtNDRhOC00MGQzLTk5MTAtZDliODg5NmU5MjZhXkEyXkFqcGdeQXVyNDUyOTg3Njg@._V1_FMjpg_UX1000_.jpg')
