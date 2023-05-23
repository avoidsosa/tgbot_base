from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.database.db import Database

db = Database('database.sql')

#Main Menu
users = InlineKeyboardButton('Пользователи', callback_data='users')
spam = InlineKeyboardButton('Рассылка', callback_data='spam')
arbitr = InlineKeyboardButton('Арбитражи', callback_data='arbitr')

main_menu = InlineKeyboardMarkup(row_width=2).add(users, spam, arbitr)

#Back to main
back_to_main = InlineKeyboardButton('Назад', callback_data='back_to_main')

back_main = InlineKeyboardMarkup().add(back_to_main)

#Users Menu
active_users = InlineKeyboardButton('Активные пользователи', callback_data='active_users')
banned_users = InlineKeyboardButton('Пользователи в бане', callback_data='banned_users')

users_menu = InlineKeyboardMarkup().add(active_users, banned_users).add(back_to_main)

#Back To Users Menu
back_to_users_menu = InlineKeyboardButton(text='Назад', callback_data='back_to_users_menu')

#Back To Users Menu
back_to_banned_users_menu = InlineKeyboardButton(text='Назад', callback_data='back_to_banned_users_menu')

#Users
def create_keyboard():
    # получаем текущий список пользователей из базы данных
    users = db.get_table()

    # создаем список кнопок для каждого пользователя
    buttons = []
    for user in users:
        button_text = f"{user[0]} - @{user[2]}"
        button_data = f"user_{user[0]}"
        buttons.append([InlineKeyboardButton(text=button_text, callback_data=button_data)])
    # создаем объект клавиатуры
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    keyboard.add(back_to_users_menu)
    return keyboard

def create_ban_keyboard():
    # получаем текущий список пользователей из базы данных
    users = db.get_banned()
    # создаем список кнопок для каждого пользователя
    buttons = []
    for user in users:
        button_text = f"{user[0]} - @{user[2]}"
        button_data = f"banned_user_{user[0]}"
        buttons.append([InlineKeyboardButton(text=button_text, callback_data=button_data)])

    # создаем объект клавиатуры
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    keyboard.add(back_to_users_menu)

    return keyboard

#back to user func

back_to_users_func = InlineKeyboardButton('Назад', callback_data='back_to_users_func')

back_users_func = InlineKeyboardMarkup().add(back_to_users_func)