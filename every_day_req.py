import time
import asyncio
from database import *
from parcer_dns import get_data_with_selenium
from concurrent.futures import ThreadPoolExecutor
from create_bot import bot
from main import send_message

import multiprocessing as mp

# ежедневный парс цен о всех добавленных товарах
async def every_day_request(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        whole_things = db_select('whole_things')
        print('Пошел жесткий парс')
        pars = []
        count = 0
        count_end = 0

        # несколько воркеров записывают инфу в список, потом инфа записывается в базу, далее
        # воркеры продолжают парсить цены, чтобы не потерять уже спаршенные данные, если программа
        # прервется
        with ThreadPoolExecutor(max_workers=2) as executor:
            for thing1 in range(len(whole_things)):
                pars.append(executor.submit(get_data_with_selenium, whole_things[thing1][4]))
                count += 1

                if count == 4 or len(whole_things) <= count_end + 4:
                    while len(pars) != 0:
                        thing = pars.pop(0).result()
                        name_and_price = thing
                        kind_id = whole_things[count_end][1]
                        url = whole_things[count_end][4]
                        count_end += 1
                        price_discount = None
                        price = None
                        name = None

                        try:
                            if name_and_price != None:

                                if url[:24] == 'https://www.dns-shop.ru/':
                                    shop = 'DNS'
                                    name = shop + '# ' + name_and_price[0]

                                    if name_and_price[1][-1] != '₽':
                                        index = name_and_price[1].find('₽')
                                        price_discount = int(''.join(name_and_price[1][:index].split()))
                                        price = int(''.join(name_and_price[1][index + 1:].split()))

                                    else:
                                        price = int(''.join(name_and_price[1][:-1].split()))

                                # через if другие магазины тут

                                else:
                                    print('В ПАРСЕ Такой магазин пока не доступен')

                                # достаем из базы последнюю цену данного товара
                                old_price = db_select('last_price', url, kind_id)

                                db_insert('thing_time', kind_id, name, price, price_discount, url, old_price[0][2])
                                if price_discount == None:
                                    print(f'В ПАРСЕ добавил товар {name} с ценой {price}')

                                if price_discount != None:
                                    print(
                                        f'В ПАРСЕ добавил товар {name} с ценой {price}. Доступна скидка: {price_discount}')

                                # сравнение цен и отправление сообщения об изменении
                                if old_price[0][0] != price:
                                    print('old', old_price)
                                    print('new', price)
                                    user_id = db_select('user_id', kind_id)

                                    await send_message(user_id[0][0], f'Цена на товар - {name} изменилась с '
                                                                      f'{old_price[0][0]} на {price}. '
                                                                      f'Вы хотите видеть цену: {old_price[0][2]}. '
                                                                      f'Ссылка: {url}')

                                if old_price[0][1] == None and price_discount != None:
                                    user_id = db_select('user_id', kind_id)

                                    await send_message(user_id[0][0], f'На товар - {name} появилась скидка: '
                                                                      f'без скидки - {old_price[0][1]}, '
                                                                      f'со скидкой - {price_discount}, '
                                                                      f'Вы хотите видеть цену: {old_price[0][2]}. '
                                                                      f'Ссылка: {url}')
                            else:
                                # заглушка
                                a = 1 / 0
                        except:
                            print('В ПАРСЕ НИчего не добавил')
                            user_id = db_select('user_id', kind_id)
                            await send_message(user_id[0][0], f'В ПАРСЕ Ничего не добавил.{name_and_price}')
                    count = 0
