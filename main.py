from aiogram import executor, types
from create_bot import dp, bot
import handlers
import database


async def on_startup(_):
    print('БОТ вышел в онлайн')


database.db_create()
handlers.register_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

# @dp.message_handler()
# async def msg_send_shop(message: types.Message):
#     print(message.text[:8])
#     await message.answer('Поймал')


# await message.reply('Пишите в личку') #копирует сообщение пользователя дополнительно

# await message.answer('hello') # просто ответ (и в личку, и в группу)

# await bot.send_message(message.from_user.id,'DADA_I') # отвечает только в личку


# await message.answer_photo(photo='https://m.media-amazon.com/images/M/MV5BNmQ0ODBhMjUtNDRhOC00MGQzLTk5MTAtZDliODg5NmU5MjZhXkEyXkFqcGdeQXVyNDUyOTg3Njg@._V1_FMjpg_UX1000_.jpg')
