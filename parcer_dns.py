import time
from bs4 import BeautifulSoup
import lxml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


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
        return name_thing.text, price_thing.text