from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# стартовая клавиатура
b1 = KeyboardButton('/Добавить_товар')
b2 = KeyboardButton('/Добавить_новую_группу')
b3 = KeyboardButton('/Получить_графики')
b4 = KeyboardButton('/Назад')

keyb_start = ReplyKeyboardMarkup(resize_keyboard=True)
keyb_start.add(b1).insert(b2).add(b3)

# keyb_groups = ReplyKeyboardMarkup(resize_keyboard=True)
# keyb_groups.add(b4)

# создание клавиатуры групп для каждого пользователя в зависимости от его групп
def keyboard_groups(groups):
    keyb_groups = []
    keyb_groups = ReplyKeyboardMarkup(resize_keyboard=True)
    keyb_groups.add(b4)
    if len(keyb_groups['keyboard']) <= 1:
        for i in groups:
            b = KeyboardButton(f'{i[1]}')
            keyb_groups.insert(b)
        return keyb_groups
    else:
        print('Уже создал клаву')
        return keyb_groups


# class keyboard_groups:
#     def __init__(self,groups):
#         self.keyb_groups = ReplyKeyboardMarkup(resize_keyboard=True)
#         # if self.keyb_groups == None:
#         #     self.b4 = KeyboardButton('/Назад')
#         #     self.keyb_groups.insert(self.b4)
#         for i in groups:
#             self.b = KeyboardButton(f'/{i[0]}')
#             self.keyb_groups.insert(self.b)
#         self.b4 = KeyboardButton('/Назад')
#         self.keyb_groups.insert(self.b4)
#         print(self.keyb_groups)
#
#     def get_keyb(self):
#         keyb_groups = self.keyb_groups
#         return keyb_groups
