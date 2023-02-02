from database import *
from aiogram import Dispatcher, types
from create_bot import bot, dp
from keyboards import *
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


async def send_welcome(message: types.Message):  # + стартовая клава
    user_id = message.from_id
    user_name = message.from_user['first_name'] + '_' + message.from_user['last_name']
    try:
        db_insert('users', user_id, user_name)
    except:
        print('Пользователь уже в базе')

    await bot.send_message(message.from_user.id, 'Hello!\nI`m Bot', reply_markup=keyb_start)


# класс для запоминания нескольких сообщений пользователя
class FSMAdmin(StatesGroup):
    # состояния для select и insert
    choose_group = State()
    url_thing = State()
    name_new_group = State()

    # состояния для delete
    delete = State()
    delete_group_thing = State()
    delete_thing = State()


# ФУНКЦИИ ДЛЯ ДОБАВЛЕНИЯ НОВОГО ТОВАРА В СУЩЕСТВУЮЩУЮ ГРУППУ
# Функция для добавления товара, активирует состояние запоминания сообщений
async def msg_put_thing(message: types.Message):
    user_id = message.from_id
    groups = db_select('whole_groups', user_id)
    await FSMAdmin.choose_group.set()
    await message.answer('Выберите группу, в которую нужно добавить товар',
                         reply_markup=keyboard_groups(groups))  # + выводит все группы и клаву с назад


# функция для выбора группы, в которую нужно добавить товар. Активно состояние прослушки
async def msg_choose_group(message: types.Message, state: FSMContext):
    user_id = message.from_id
    async with state.proxy() as data:
        data['choose_group'] = message.text
    await FSMAdmin.next()
    await message.answer('Отправьте мне ссылку на товар')


# функция для получения ссылки на товар. Активно состояние прослушки, тут же оно закрывается
async def msg_put_url(message: types.Message, state: FSMContext):
    user_id = message.from_id

    async with state.proxy() as data:
        data['url_thing'] = message.text
        one_group = db_select('kind_id', user_id, data['choose_group'])
        # ЗДЕСЬ РАЗОБРАТЬ ССЫЛКУ КАК HTML
        try:
            db_insert('thing', one_group[0][0], data['url_thing'])
            await message.answer(f'Добавил товар в группу {data["choose_group"]}', reply_markup=keyb_start)
        except:
            await message.answer('Групп еще нет', reply_markup=keyb_start)
    await state.finish()


# ФУНКЦИИ ДЛЯ ДОБАВЛЕНИЯ НОВОЙ ГРУППЫ
# функция для добавления новой группы. Активирует состояние прослушки
async def msg_put_new_group(message: types.Message):
    user_id = message.from_id
    groups = db_select('whole_groups', user_id)
    await FSMAdmin.name_new_group.set()
    await message.answer('Введите название новой группы, оно должно отличаться от уже имеющихся',
                         reply_markup=keyboard_groups(groups))


# функция получение названия новой группы. Активно состояние прослушки, тут же оно закрывается
async def msg_put_new_group_end(message: types.Message, state: FSMContext):
    user_id = message.from_id

    async with state.proxy() as data:
        data['name_new_group'] = message.text
        exist_groups = db_select('whole_groups', user_id)
        flag = False
        for i in exist_groups:
            if data['name_new_group'] == i[1]:
                await message.answer('Группа с таким названием уже есть', reply_markup=keyb_start)
                flag = True
        if flag == True:
            await state.finish()
        else:
            db_insert('new_group', user_id, data['name_new_group'])
            await message.answer('Записал новую группу', reply_markup=keyb_start)
            await state.finish()


# ФУНКЦИИ ДЛЯ УДАЛЕНИЯ ГРУППЫ ИЛИ ТОВАРА
# Функция для выбора того, что нужно удалить, активируется состояние прослушки
async def msg_delete(message: types.Message):
    user_id = message.from_id
    await message.answer('Выберите то, что хотите удалить', reply_markup=keyb_delete)
    await FSMAdmin.delete.set()


# Функция для удаления группы или товара, активно состояние
async def msg_delete_choose(message: types.Message, state: FSMContext):
    user_id = message.from_id
    groups = db_select('whole_groups', user_id)
    async with state.proxy() as data:
        if message.text == '/Удалить_группу':
            data['data'] = '/Удалить_группу'
            await message.answer('Выберите группу для удаления', reply_markup=keyboard_groups(groups))
            await FSMAdmin.next()
        if message.text == '/Удалить_товар':
            data['data'] = '/Удалить_товар'
            await message.answer('Выберите группу, в которой находится товар', reply_markup=keyboard_groups(groups))
            await FSMAdmin.next()


# Функция для удаления группы и finish. Для удаления товара и next (вернет клавиатуру с товарами группы)
async def msg_delete_group_thing(message: types.Message, state: FSMContext):
    user_id = message.from_id

    async with state.proxy() as data:
        if data['data'] == '/Удалить_группу':
            one_group_id = db_select('kind_id', user_id, message.text)
            try:
                db_delete('delete_group', user_id, one_group_id[0][0])
                await message.answer(f'Удалил группу: {message.text}', reply_markup=keyb_start)
                await state.finish()
            except:
                await message.answer('Нет такой группы', reply_markup=keyb_start)
                await state.finish()

        if data['data'] == '/Удалить_товар':
            one_group_id = db_select('kind_id', user_id, message.text)
            data['one_group_id'] = one_group_id
            try:
                things = db_select('few_things', one_group_id[0][0])
                print(things)
                await message.answer('Выберите товар для удаления', reply_markup=keyboard_groups(things))
                await FSMAdmin.next()
            except:
                await message.answer('Нет такой группы', reply_markup=keyb_start)
                await state.finish()


# Функция для удаления товара finish
async def msg_delete_thing(message: types.Message, state: FSMContext):
    user_id = message.from_id
    async with state.proxy() as data:
        one_group_id = data['one_group_id']

        if db_select('one_thing', one_group_id[0][0], message.text) != []:
            db_delete('delete_thing', one_group_id[0][0], message.text)
            await message.answer(f'Удалил товар: {message.text}', reply_markup=keyb_start)
        else:
            await message.answer(f'Такого товара нет: {message.text}', reply_markup=keyb_start)
        await state.finish()


# для выхода из любого состояния
async def exit(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer('/Назад', reply_markup=keyb_start)
    else:
        await state.finish()
        await message.answer('Я вышел из прослушки', reply_markup=keyb_start)


# ФУНКЦИИ ДЛЯ ВЫВОДА ГРАФИКОВ
# функция для вывода графиков, тут тоже нужно группы выводить и активировать состояние
async def msg_put_graf(message: types.Message):
    if message.text == '/Получить_графики':
        await message.answer('Выгружаю графики')


async def msg_catcher(message: types.Message):
    await message.answer('Нет такой команды', reply_markup=keyb_start)
    await message.delete()


# регистрация функций
def register_handlers(dp: Dispatcher):
    # старт
    dp.register_message_handler(send_welcome, commands=['start', 'help'])
    dp.register_message_handler(exit, state='*', commands=['Назад'])

    # для добавления нового товара
    dp.register_message_handler(msg_put_thing, commands=['Добавить_товар'], state=None)
    dp.register_message_handler(msg_choose_group, state=FSMAdmin.choose_group)
    dp.register_message_handler(msg_put_url, state=FSMAdmin.url_thing)

    # для добавления новой группы
    dp.register_message_handler(msg_put_new_group, commands=['Добавить_новую_группу'], state=None)
    dp.register_message_handler(msg_put_new_group_end, state=FSMAdmin.name_new_group)

    # для удаления товара
    dp.register_message_handler(msg_delete, commands=['Удалить'], state=None)
    dp.register_message_handler(msg_delete_choose, commands=['Удалить_группу', 'Удалить_товар'], state=FSMAdmin.delete)
    dp.register_message_handler(msg_delete_group_thing, state=FSMAdmin.delete_group_thing)
    dp.register_message_handler(msg_delete_thing, state=FSMAdmin.delete_thing)

    dp.register_message_handler(msg_catcher)
