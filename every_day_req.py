import time
import asyncio
from database import *
from parcer_dns import get_data_with_selenium


# from parcer_dns import mmmm

async def every_day_request(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        whole_things = db_select('whole_things')
        print(whole_things)
        print('Пошел жесткий парс')

        with ThreadPoolExecutor(max_workers=1) as executor:
        for i in whole_things:
            url = i[4]
            kind_id = i[1]
            price_discount = None
            price = None

            if url[:24] == 'https://www.dns-shop.ru/':
                #name_and_price = get_data_with_selenium(url)
                name_and_price = executor.s
                print(1)
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
