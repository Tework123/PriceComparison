import numpy as np
import matplotlib.pyplot as plt

def get_graf(list_times):

#еще надо shop из базы достать и подкрутить к названию
# а то может совпадать, также можно цвет линий изменить
# под магазин

    list_times = sorted(list_times, key=lambda x: x[0])
    for i in list_times:
        print(i)
    for i in range(len(list_times)):
        if list_times[i] == list_times[i][0]:
            #сразу несколько добавить x y в график, посмотреть сережу

    x = np.array([i[4] for i in list_times])
    y = np.array([i[1] for i in list_times])

    plt.plot(x,y)
    plt.savefig('graf_price.png')

