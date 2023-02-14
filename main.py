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

if __name__ == '__main__':
    # asyncio.run(main())
    # executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    try:
        loop = asyncio.get_event_loop()
        # loop.create_task(every_day_req.every_day_request(86400))  # поставим 10 секунд, в качестве теста
        loop.create_task(every_day_req.every_day_request(10000))
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    except:
        print('Я сломался')
