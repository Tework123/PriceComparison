import time
import asyncio
from database import *
from parcer_dns import get_data_with_selenium
from concurrent.futures import ThreadPoolExecutor


async def every_day_request(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        whole_things = db_select('whole_things')
        print('Пошел жесткий парс')
        pars = []
        with ThreadPoolExecutor(max_workers=2) as executor:
            for thing in whole_things:
                pars.append(executor.submit(get_data_with_selenium, thing[4]))

        for i in range(len(pars)):
            name_and_price = pars[i].result()
            kind_id = whole_things[i][1]
            url = whole_things[i][4]

            price_discount = None
            price = None

            if url[:24] == 'https://www.dns-shop.ru/':

                shop = 'DNS'
                if name_and_price == None:
                    print('В ПАРСЕ Не нашел магазина')
                print(name_and_price)
                if name_and_price[1][-1] != '₽':

                    index = name_and_price[1].find('₽')
                    name = name_and_price[0]
                    price_discount = int(''.join(name_and_price[1][:index].split()))
                    price = int(''.join(name_and_price[1][index + 1:].split()))
                else:
                    name = name_and_price[0]
                    price = int(''.join(name_and_price[1][:-1].split()))

            # через if другие магазины тут

            else:
                print('В ПАРСЕ Такой магазин пока не доступен')

            try:
                db_insert('thing_time', kind_id, name, price, price_discount)
                if price_discount == None:
                    print(f'В ПАРСЕ добавил товар {name} с ценой {price}')

                if price_discount != None:
                    print(
                        f'В ПАРСЕ добавил товар {name} с ценой {price}. Доступна скидка: {price_discount}')
            except:
                print('В ПАРСЕ НИчего не добавил')
