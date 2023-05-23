from aiogram.types import Message

from tgbot.database.db import Database
from tgbot.markups.admin import main_menu
from tgbot.markups.client import super_main
from tgbot.data.config import ADMIN

db = Database('database.sql')


async def start_cmd(message: Message):
    db.create_table()
    db.create_banned_table()
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    username = message.from_user.username
    date = message.date

    if user_id == ADMIN:
        await message.answer('Admin mode', reply_markup=main_menu)

    elif db.get_banned_id(user_id) is not None:
        await message.answer('Вы в бане')

    elif not db.user_exist(user_id):
        db.add_user(user_id, user_name, username, date)
        await message.answer('Привет', reply_markup=super_main)

    else:
        await message.answer('Привет', reply_markup=super_main)