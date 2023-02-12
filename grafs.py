import matplotlib.pyplot as plt
import datetime
import time
import random
from datetime import date
import matplotlib.dates as mdates
from matplotlib.axis import Axis


def get_time(time):
    time_1 = datetime.datetime.fromtimestamp(time)
    time_2 = date(time_1.year, time_1.month, time_1.day)
    return time_2
    # time_3 = str(time_2)[5:]
    # time_4 = time_3[3:5] + '-' + time_3[:2]
    # return time_4


def get_graf(list_times):
    # еще надо shop из базы достать и подкрутить к названию
    # а то может совпадать, также можно цвет линий изменить
    # под магазин

    list_times = sorted(list_times, key=lambda x: x[0])

    thing = list_times[0][0]
    result = []
    text_for_message = []
    count = 0
    for i in range(len(list_times)):
        if thing == list_times[i][0] and count == 0:
            result.append([list_times[i]])
        if thing == list_times[i][0] and count != 0:
            result[-1].append(list_times[i])
        count += 1
        if thing != list_times[i][0]:
            thing = list_times[i][0]
            result.append([list_times[i]])
            count = 1

    # for i in result:
    #     print(i)


    years = mdates.YearLocator()
    months = mdates.MonthLocator()
    days = mdates.DayLocator()
    timeFmt = mdates.DateFormatter('%d-%m')
    fig, ax = plt.subplots()

    for one_list in result:
        print(one_list)

        text_for_message.append((one_list[-1][0],one_list[-1][1]
        ,(one_list[-1][2]),one_list[-1][3], one_list[-1][4]))

        prices = []
        times = []
        for price in one_list:
            if price[2] == None:
                prices.append(price[1])
            else:
                prices.append(price[2])
        for time1 in one_list:
            time1 = time1[4]
            time2 = get_time(time1)
            times.append(time2)

        ax.plot(times, prices,label=f'{one_list[0][0]}')



    # c = 0
    # for i in range(1, 6):
    #     count = 0
    #     times = []
    #     for time1 in range(1, 100):
    #         time1 = time.time() + count
    #
    #         time_2 = get_time(time1)
    #         times.append(time_2)
    #         count += 86400
    #
    #     prices = []
    #     c += 6000
    #     for price in range(1, 100):
    #         price = random.randrange(26000, 30000) + c
    #
    #         prices.append(price)
    #     print(times)
    #     print(prices)
    #     ax.plot(times, prices, label=f'{list_times[i][0]}')


    if len(result[0]) < 10:
        Axis.set_major_locator(ax.xaxis, days)
    if 10 <= len(result[0]) < 200:
        Axis.set_minor_locator(ax.xaxis, days)
        Axis.set_major_locator(ax.xaxis, months)

    if 200 <= len(result[0]) < 100000:
        Axis.set_minor_locator(ax.xaxis, months)
        Axis.set_major_locator(ax.xaxis, years)


    fig.set_figheight(10)
    fig.set_figwidth(17)

    ax.xaxis.set_major_formatter(timeFmt)
    #ax.xaxis.set_major_formatter(timeFmt)

    ax.grid(True)
    ax.legend( loc='upper right', fontsize=10, framealpha=0.8)
    #plt.show()
    plt.savefig('graf_price.png')
    return text_for_message


list_times1 = [('13.3" Ноутбук Apple MacBook Air серебристый', 87999, 80999,
               'https://www.dns-shop.ru/product/819584c1e861ed20/133-noutbuk-apple-macbook-air-serebristyj/',
               1676001494.1193886),
              ('13.3" Ноутбук Apple MacBook Air серебристый', 87999, 83999,
               'https://www.dns-shop.ru/product/819584c1e861ed20/133-noutbuk-apple-macbook-air-serebristyj/',
               1676001762.9192193),
              ('13.3" Ноутбук Apple MacBook Air серебристый', 87999, 72999,
               'https://www.dns-shop.ru/product/819584c1e861ed20/133-noutbuk-apple-macbook-air-serebristyj/',
               1676001909.6168816),
              ('15.6" Ноутбук MSI Modern 15 B11M-003XRU черный', 38999, None,
               'https://www.dns-shop.ru/product/4c9a77edeba9ed20/156-noutbuk-msi-modern-15-b11m-003xru-cernyj/',
               1676001571.4557638),
              ('15.6" Ноутбук MSI Modern 15 B11M-003XRU черный', 37999, None,
               'https://www.dns-shop.ru/product/4c9a77edeba9ed20/156-noutbuk-msi-modern-15-b11m-003xru-cernyj/',
               1676001763.229992),
              ('15.6" Ноутбук MSI Modern 15 B11M-003XRU черный', 36999, None,
               'https://www.dns-shop.ru/product/4c9a77edeba9ed20/156-noutbuk-msi-modern-15-b11m-003xru-cernyj/',
               1676001909.6388817),
              ('15.6" Ультрабук HUAWEI MateBook D 15 BoM-WFQ9 серебристый', 59999, None,
               'https://www.dns-shop.ru/product/cbfa8e2aebbeed20/156-ultrabuk-huawei-matebook-d-15-bom-wfq9-serebristyj/',
               1676000355.6513531),
              ('15.6" Ультрабук HUAWEI MateBook D 15 BoM-WFQ9 серебристый', 59999, None,
               'https://www.dns-shop.ru/product/cbfa8e2aebbeed20/156-ultrabuk-huawei-matebook-d-15-bom-wfq9-serebristyj/',
               1676001762.639293),
              ('15.6" Ультрабук HUAWEI MateBook D 15 BoM-WFQ9 серебристый', 59999, None,
               'https://www.dns-shop.ru/product/cbfa8e2aebbeed20/156-ultrabuk-huawei-matebook-d-15-bom-wfq9-serebristyj/',
               1676001827.138154),
              ('15.6" Ультрабук HUAWEI MateBook D 15 BoM-WFQ9 серебристый', 59999, None,
               'https://www.dns-shop.ru/product/cbfa8e2aebbeed20/156-ultrabuk-huawei-matebook-d-15-bom-wfq9-serebristyj/',
               1676001909.5949426),
              ('17.3" Ноутбук MSI GF76 Katana 11SC-483XRU черный', 65999, None,
               'https://www.dns-shop.ru/product/10668f1a19f2ed20/173-noutbuk-msi-gf76-katana-11sc-483xru-cernyj/',
               1676000382.8683684),
              ('17.3" Ноутбук MSI GF76 Katana 11SC-483XRU черный', 62999, None,
               'https://www.dns-shop.ru/product/10668f1a19f2ed20/173-noutbuk-msi-gf76-katana-11sc-483xru-cernyj/',
               1676001762.8367655),
              ('17.3" Ноутбук MSI GF76 Katana 11SC-483XRU черный', 66999, None,
               'https://www.dns-shop.ru/product/10668f1a19f2ed20/173-noutbuk-msi-gf76-katana-11sc-483xru-cernyj/',
               1676001909.606943),
              ('17.3" Ноутбук MSI Katana GF76 12UC-265XRU черный', 80999, 72899,
               'https://www.dns-shop.ru/product/450e57601c3fed20/173-noutbuk-msi-katana-gf76-12uc-265xru-cernyj/',
               1676001528.6343849),
              ('17.3" Ноутбук MSI Katana GF76 12UC-265XRU черный', 80999, 72899,
               'https://www.dns-shop.ru/product/450e57601c3fed20/173-noutbuk-msi-katana-gf76-12uc-265xru-cernyj/',
               1676001827.9676282),
              ('17.3" Ноутбук MSI Katana GF76 12UC-265XRU черный', 80999, 71899,
               'https://www.dns-shop.ru/product/450e57601c3fed20/173-noutbuk-msi-katana-gf76-12uc-265xru-cernyj/',
               1676001909.627918)
              ]

#get_graf(list_times)
