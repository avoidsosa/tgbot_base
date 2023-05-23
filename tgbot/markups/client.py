from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

#Главная клавиатура
super_main = ReplyKeyboardMarkup(resize_keyboard=True)

kab = KeyboardButton('Кабинет')
shop = KeyboardButton('Товары')
info = KeyboardButton('Связь')

super_main.add(kab, shop, info)

#Кабинет
profile = InlineKeyboardButton(text='Профиль', callback_data='profile')
balance = InlineKeyboardButton(text='Пополнить баланс', callback_data='balance')
history = InlineKeyboardButton(text='История покупок', callback_data='history')

kab_menu = InlineKeyboardMarkup().add(profile).add(balance).add(history)

#Профиль

#Магазик
numbers = InlineKeyboardButton(text='Номера', callback_data='numbers')

shop_menu = InlineKeyboardMarkup().add(numbers)