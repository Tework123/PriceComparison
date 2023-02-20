import time
from bs4 import BeautifulSoup
import lxml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# парс цен с динамического сайта с помощью селениума
def get_data_with_selenium(url):

    # поменять путь для драйвера при установке на сервер
    ser = Service(r'C:\programmboy\python_main\PriceComparison\chromedriver.exe')
    options = webdriver.ChromeOptions()

    name_thing = None
    price_thing = None
    flag = False
    try:
    #if 1 == 1:

        # фоновый режим работы хрома
        options.headless = True

        # разрешение экран для работы в комп.версии сайта в фоновом режиме
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(service=ser, options=options)
        driver.get(url=url)

        # остановка до получения цены и названия товара
        driver.implicitly_wait(10)

        # парс цены и названия
        name_thing = driver.find_element(By.CLASS_NAME, 'product-card-top__title')
        name_thing = name_thing.text.split()

        # обработка некоторых проблем
        if name_thing[0] == 'Отзывы' or name_thing[0] == 'Оценка':
            name_thing = ' '.join(name_thing[2:])
        if name_thing[0] == 'Коммуникатор' or name_thing[0] == 'Обзоры':
            name_thing = ' '.join(name_thing[1:])
        else:
            name_thing = ' '.join(name_thing)

        price_thing = driver.find_element(By.CLASS_NAME, 'product-buy__price')

        # time.sleep(8)
        # data_page = driver.page_source
        #
        # soup = BeautifulSoup(data_page, 'lxml')
        # name_thing = soup.find(class_='container product-card'
        #                        ).find(class_="product-card-top product-card-top_full").find(
        #     class_="product-card-top__name")
        #
        # price_thing = soup.find(class_='container product-card').find(
        #     class_="product-card-top product-card-top_full") \
        #     .find(class_="product-buy product-buy_one-line") \
        #     .find(class_="product-buy__price-wrap product-buy__price-wrap_interactive").find(
        #     class_="product-buy__price")

    except:
        print('no')
        flag = True

    finally:
        # s.close()
        # s.quit()
        if flag == True:
            return None
        else:
            return name_thing, price_thing.text


if __name__ == '__main__':
    print(1)