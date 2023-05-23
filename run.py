from aiogram import Bot, Dispatcher, executor

from tgbot.database.db import Database
from tgbot.bot import dp

db = Database('database.sql')

async def on_startup():
    db.create_table()
    db.create_banned_table()

async def on_shutdown(dp: Dispatcher):
    await dp.storage.close()
    await dp.storage.wait_closed()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)