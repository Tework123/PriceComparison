import sqlite3 as sq
import time


# создание базы данных
def db_create():
    with sq.connect('PriceCompare.db') as con:
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY UNIQUE,
                    user_name INTEGER,
                    count_things INTEGER)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS kinds_of_things (
                            kind_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER,
                            kind str)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS things (
                                    thing_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    kind_id INTEGER,
                                    name str,
                                    shop str,
                                    url str)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS time (
                                            time_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            kind_id INTEDER,
                                            name str,
                                            price INTEGER,
                                            price_discount INTEGER,
                                            url str,
                                            time_t INTEGER,
                                            desired_price INTEGER)''')


# ЗАПИСЬ ИНФОРМАЦИИ В БАЗУ ДАННЫХ
def db_insert(*args):
    # запись юзера в базу
    if args[0] == 'users':
        with sq.connect('PriceCompare.db') as con:
            cur = con.cursor()
            cur.execute('''INSERT INTO users (user_id, user_name, count_things) VALUES (?,?,0)''', (args[1], args[2]))

    # запись новой группы по id группы, id юзера, названию группы
    if args[0] == 'new_group':
        with sq.connect('PriceCompare.db') as con:
            cur = con.cursor()
            cur.execute('''INSERT INTO kinds_of_things (user_id, kind) VALUES (?,?)''',
                        (args[1], args[2]))

    # запись нового товара в базу через ссылку на товар
    if args[0] == 'thing':
        kind_id = args[1]
        name = args[2]
        shop = args[3]
        url = args[4]
        with sq.connect('PriceCompare.db') as con:
            cur = con.cursor()

            # тут функция должна достать с сайта url товара и shop
            cur.execute('''INSERT INTO things (kind_id, name, shop, url) VALUES (?,?,?,?)''',
                        (kind_id, name, shop, url))

    if args[0] == 'thing_time':
        kind_id = args[1]
        name = args[2]
        price = args[3]
        price_discount = args[4]
        url = args[5]
        desired_price = args[6]

        with sq.connect('PriceCompare.db') as con:
            cur = con.cursor()
            cur.execute('''INSERT INTO time (kind_id, name, price, price_discount, url, time_t,desired_price) VALUES (?,?,?,?,?,?,?)''',
                        (kind_id, name, price, price_discount, url, time.time(),desired_price))


# ПОЛУЧЕНИЕ ИНФОРМАЦИИ ИЗ БАЗЫ
def db_select(*args):
    # проверка на наличие юзера в базе
    if args[0] == 'users':
        user_id = args[1]
        with sq.connect('PriceCompare.db') as con:
            cur = con.cursor()
            cur.execute('''SELECT user_id FROM users''')
            for i in cur.fetchall():
                if user_id in i:
                    return True
            return False

    # возвращает все группы пользователя (кортеж с id группы и названием)
    if args[0] == 'whole_groups':
        user_id = args[1]
        with sq.connect('PriceCompare.db') as con:
            cur = con.cursor()
            cur.execute('''SELECT kind, kind_id FROM kinds_of_things WHERE user_id = ?''', (user_id,))
            return cur.fetchall()

    # возвращает id одной группы пользователя по его user_id и названию группы
    if args[0] == 'kind_id':
        user_id = args[1]
        kind = args[2]
        with sq.connect('PriceCompare.db') as con:
            cur = con.cursor()
            cur.execute('''SELECT kind_id FROM kinds_of_things WHERE user_id = ? and kind = ?''', (user_id, kind))
            return cur.fetchall()

    # возвращает товары из одной группы по ее kind_id
    if args[0] == 'few_things':
        kind_id = args[1]
        with sq.connect('PriceCompare.db') as con:
            cur = con.cursor()
            cur.execute('''SELECT name, thing_id FROM things WHERE kind_id = ?''', (kind_id,))
            return cur.fetchall()

    # возвращает один товар из группы пользователя по его kind_id и url
    if args[0] == 'one_thing':
        kind_id = args[1]
        name = args[2]
        with sq.connect('PriceCompare.db') as con:
            cur = con.cursor()
            cur.execute('''SELECT thing_id FROM things WHERE kind_id = ? and name = ?''', (kind_id, name))
            return cur.fetchall()
    # возвращает все товары для ежедневного парса
    if args[0] == 'whole_things':
        with sq.connect('PriceCompare.db') as con:
            cur = con.cursor()
            cur.execute('''SELECT * FROM things''')
            return cur.fetchall()
    # возвращает юзер id для отправки сообщения о изменении цены, удалении товара и тд
    if args[0] == 'user_id':
        kind_id = args[1]
        with sq.connect('PriceCompare.db') as con:
            cur = con.cursor()
            cur.execute('''SELECT user_id FROM kinds_of_things WHERE kind_id = ?''', (kind_id,))
            return cur.fetchall()
    # возвращает последнюю цену на товар
    if args[0] == 'last_price':
        url = args[1]
        kind_id = args[2]
        with sq.connect('PriceCompare.db') as con:
            cur = con.cursor()
            cur.execute(
                '''SELECT price, price_discount,desired_price  FROM time WHERE time_t = (SELECT MAX(time_t) FROM time WHERE name = (SELECT name FROM things WHERE url = ?) and kind_id = ?)''',
                (url, kind_id))
            return cur.fetchall()
    # возвращает список всех паршенных товаров с разными временами из time
    if args[0] == 'graf_time':
        kind_id = args[1]

        with sq.connect('PriceCompare.db') as con:
            cur = con.cursor()
            cur.execute('''SELECT name, thing_id FROM things WHERE kind_id = ?''', (kind_id,))
            a = cur.fetchall()
            #print(a)
            result = []
            for i in a:
                name = i[0]
                res_one = cur.execute('''SELECT name, price, price_discount, url, time_t, desired_price FROM time WHERE name = ?''', (name,))
                res_one = cur.fetchall()
                result += res_one

            return result


        # with sq.connect('PriceCompare.db') as con:
        #     cur = con.cursor()
        #     cur.execute('''SELECT name, price, price_discount, url, time_t, desired_price FROM time WHERE kind_id = ?''', (kind_id,))
        #     return cur.fetchall()


# УДАЛЕНИЕ ИНФОРМАЦИИ ИЗ БАЗЫ
def db_delete(*args):
    # удаление группы и связанных с нею товаров
    if args[0] == 'delete_group':
        user_id = args[1]
        kind_id = args[2]
        with sq.connect('PriceCompare.db') as con:
            cur = con.cursor()
            cur.execute('''DELETE FROM kinds_of_things WHERE user_id = ? and kind_id = ?''', (user_id, kind_id))
            cur.execute('''DELETE FROM things WHERE kind_id = ?''', (kind_id,))
            cur.execute('''DELETE FROM time WHERE kind_id = ?''', (kind_id,))

    # удаление товара
    if args[0] == 'delete_thing':
        one_group_id = args[1]
        name = args[2]
        with sq.connect('PriceCompare.db') as con:
            cur = con.cursor()
            cur.execute('''DELETE FROM things WHERE kind_id = ? and name = ?''', (one_group_id, name))
            cur.execute('''DELETE FROM time WHERE kind_id = ? and name = ?''', (one_group_id, name))
