from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message

from tgbot.markups.client import *
from tgbot.database.db import Database

db = Database('database.sql')

async def buttons_handler(message: Message):
    if message.text == "Кабинет":
        await message.answer("Ваш кабинет", reply_markup=kab_menu)
    elif message.text == "Товары":
        await message.answer("Товары", reply_markup=shop_menu)
    elif message.text == "Связь":
        await message.answer('Информация')
    else:
        await message.answer('Бляяя ты попал', reply_markup=super_main)

async def profile(call):
    user_id = call.from_user.id
    users = db.get_table()

    user_info = None
    for user in users:
        if user[0] == user_id:
            user_info = user
            break

    if user_info is not None:
        user_uname = user_info[2]
        user_date = user_info[3]
        await call.message.edit_text(
            f"Тэг: @{user_uname}\n\nДата регистрации: {user_date}\n\nБаланс: 0")
    else:
        # User not found in the table
        await call.message.edit_text("User not found.")

async def history_menu(call):
    await call.message.edit_text('В разработке')

async def balance(call):
    await call.message.edit_text('Напишите сумму для пополнения')