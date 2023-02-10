from database import *
from aiogram import Dispatcher, types
from create_bot import bot
from keyboards import *
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from parcer_dns import get_data_with_selenium
from aiogram.types import InputFile
import grafs


async def send_welcome(message: types.Message):  # + стартовая клава
    user_id = message.from_id
    user_name = message.from_user['first_name'] + '_' + message.from_user['last_name']
    try:
        db_insert('users', user_id, user_name)
    except:
        print('Пользователь уже в базе')

    await bot.send_message(message.from_user.id, 'Hello!\nI`m Bot', reply_markup=keyb_start)


async def send_graf(id, graf):
    await bot.send_photo(id, graf)


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

    # состояния для вывода графиков
    create_graf = State()


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
        shop = None
        name_and_price = None
        price_discount = None
        try:
            if message.text[:24] == 'https://www.dns-shop.ru/' or message.text[:12] == 'dns-shop.ru/':
                name_and_price = get_data_with_selenium(message.text)
                shop = 'DNS'

                if name_and_price[1][-1] != '₽':

                    index = name_and_price[1].find('₽')
                    name = name_and_price[0]
                    price_discount = int(''.join(name_and_price[1][:index].split()))
                    price = int(''.join(name_and_price[1][index + 1:].split()))
                else:
                    name = name_and_price[0]
                    price = int(''.join(name_and_price[1][:-1].split()))

            ##if

            else:
                await message.answer('Такой магазин пока не доступен')

        except:
            await message.answer('Не нашел название и цену товара')

        one_group = db_select('kind_id', user_id, data['choose_group'])
        # ЗДЕСЬ РАЗОБРАТЬ ССЫЛКУ КАК HTML
        try:
            db_insert('thing', one_group[0][0], name, shop, data['url_thing'])
            db_insert('thing_time', one_group[0][0], name, price, price_discount, data['url_thing'])
            if price_discount == None:
                await message.answer(f'Добавил товар: {name} с ценой {price} в группу {data["choose_group"]}',
                                     reply_markup=keyb_start)

            if price_discount != None:
                await message.answer(
                    f'Добавил товар: {name} с ценой {price} в группу {data["choose_group"]}. Доступна скидка: {price_discount}',
                    reply_markup=keyb_start)
        except:
            await message.answer('Ничего не добавил', reply_markup=keyb_start)
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
        user_id = message.from_id
        groups = db_select('whole_groups', user_id)
        await message.answer('Выберите группу', reply_markup=keyboard_groups(groups))
        await FSMAdmin.create_graf.set()


async def msg_put_graf_end(message: types.Message, state: FSMContext):
    user_id = message.from_id

    try:
        one_group_id = db_select('kind_id', user_id, message.text)
        list_times = db_select('graf_time', one_group_id[0][0])

        grafs.get_graf(list_times)
        graf = InputFile(r'C:\programmboy\python_main\PriceComparison\graf_price.png')

        await send_graf(user_id, graf)

        await message.answer(f'Отправляю графики для группы: {message.text}', reply_markup=keyb_start)
        await state.finish()

    except:
        await message.answer('Нет такой группы', reply_markup=keyb_start)
        await state.finish()


# ловит остальные сообщения
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

    # для вывода графиков
    dp.register_message_handler(msg_put_graf, commands=['Получить_графики'], state=None)
    dp.register_message_handler(msg_put_graf_end, state=FSMAdmin.create_graf)

    dp.register_message_handler(msg_catcher)
