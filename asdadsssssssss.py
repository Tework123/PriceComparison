import time
from bs4 import BeautifulSoup
import lxml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from concurrent.futures import ThreadPoolExecutor


def get_data_with_selenium(url):
    # поменять путь для драйвера
    ser = Service(r'C:\Users\danil\PycharmProjects\Telega_price\chromedriver.exe')
    op = webdriver.ChromeOptions()
    s = webdriver.Chrome(service=ser, options=op)
    try:
        s = webdriver.Chrome(service=ser, options=op)
        s.get(url=url)
        time.sleep(2)
        data_page = s.page_source
        name_thing = None
        price_thing = None
        soup = BeautifulSoup(data_page, 'lxml')
        name_thing = soup.find(class_='container product-card'
                               ).find(class_="product-card-top product-card-top_full").find(
            class_="product-card-top__name")

        price_thing = soup.find(class_='container product-card').find(
            class_="product-card-top product-card-top_full") \
            .find(class_="product-buy product-buy_one-line") \
            .find(class_="product-buy__price-wrap product-buy__price-wrap_interactive").find(
            class_="product-buy__price")
    except:
        print('no')

    finally:
        # s.close()
        s.quit()
        print(name_thing.text, price_thing.text)
        return name_thing.text, price_thing.text

СДЕЛАТЬ ВОРКЕРОВ ДЛЯ ДОБАВЛЕНИЯ ЮРЛ И ПАРСА
ДЛЯ ВК БОТА: СКАЧАТЬ ФОТКУ РАСПИСАНИЯ И ПРОПИСАТЬ К НЕЙ НОВЫЙ ПУТЬ

ДЛЯ ТЕЛЕГРАМ-БОТА: НАСТРОИТЬ ЦИКЛ ПАРСА, ЭТОТ ФАЙЛ УДАЛИТЬ, СКАЧАТЬ ХРОМДРАЙВЕР, НЕ ЗАБЫТЬ ТОКЕНЫ. рЕКВАЙРЕМЕНТ НА ГИТХАБЕ НОРМАЛЬНЫЙ
А ТАКЖЕ SQLLITE
result = []
whole_things = ['https://www.dns-shop.ru/product/64e68538a1c93330/polirovalnaa-masina-makita-9237cb/opinion/',
                'https://www.dns-shop.ru/product/ff0f5ce6c4eb2ff2/podstavka-dla-plastinok-record-pro-gk-r25/',
                'https://www.dns-shop.ru/product/88d109cec4eb2ff2/podstavka-dla-plastinok-record-pro-gk-r25m/',
                'https://www.dns-shop.ru/product/3a6d610ec4ec2ff2/podstavka-dla-plastinok-record-pro-gk-r40a/',
                'https://www.dns-shop.ru/product/64e68538a1c93330/polirovalnaa-masina-makita-9237cb/opinion/',
                'https://www.dns-shop.ru/product/ff0f5ce6c4eb2ff2/podstavka-dla-plastinok-record-pro-gk-r25/',
                'https://www.dns-shop.ru/product/88d109cec4eb2ff2/podstavka-dla-plastinok-record-pro-gk-r25m/',
                'https://www.dns-shop.ru/product/3a6d610ec4ec2ff2/podstavka-dla-plastinok-record-pro-gk-r40a/'
                ]

with ThreadPoolExecutor(max_workers=3) as ex:
    start = time.time()
    for i in whole_things:
        #result.append(ex.submit(get_data_with_selenium, i))
        ex.submit(get_data_with_selenium, i)
print(finish-start)
# for i in whole_things:
#     start = time.time()
#     get_data_with_selenium(i)
#     finish = time.time()
#     print(finish-start)
