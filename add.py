import sqlite3 as sq


with sq.connect('PriceCompare.db') as con:
    cur = con.cursor()
    cur.execute('''DROP TABLE IF EXISTS users''')
    cur.execute('''DROP TABLE IF EXISTS kinds_of_things''')
    cur.execute('''DROP TABLE IF EXISTS things''')
    cur.execute('''DROP TABLE IF EXISTS time''')

