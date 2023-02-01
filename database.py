import sqlite3 as sq


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
                                    shop str)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS date (
                                            thing_id INTEGER,
                                            name str,
                                            price INTEGER,
                                            date INTEGER)''')


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
        with sq.connect('PriceCompare.db') as con:
            cur = con.cursor()

            # тут функция должна достать с сайта name товара и shop
            cur.execute('''INSERT INTO things (kind_id, name, shop) VALUES (?,?,?)''',
                        (args[1], name, 'shop'))


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
            cur.execute('''SELECT kind_id, kind FROM kinds_of_things WHERE user_id = ?''', (user_id,))
            return cur.fetchall()

    # возвращает id одной группы пользователя по его user_id и названию группы.
    if args[0] == 'kind_id':
        user_id = args[1]
        kind = args[2]
        with sq.connect('PriceCompare.db') as con:
            cur = con.cursor()
            cur.execute('''SELECT kind_id FROM kinds_of_things WHERE user_id = ? and kind = ?''', (user_id, kind))
            return cur.fetchall()
