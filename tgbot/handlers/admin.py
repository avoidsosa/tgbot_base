from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import ChatNotFound
import asyncio

from tgbot.database.db import Database
from tgbot.states.admin import SpamState
from tgbot.states.admin import BalanceState
from tgbot.markups.admin import *

db = Database('database.sql')

#Рассылка
async def spam_start(call):
    await call.message.edit_text('Напишите сообщение для рассылки:', reply_markup=back_main)
    await SpamState.waiting_for_spam_text.set()

async def back_to_main(call, state: FSMContext):
    await state.reset_state()  # сбрасывается состояние ожидания сообщения
    await call.message.edit_text('Вы вернулись в главное меню:', reply_markup=main_menu)

async def get_spam_text(message: Message, state: FSMContext):
    text = message.text
    await state.finish()
    users = db.get_users()
    for row in users:
        user_id = row[0]
        try:
            chat = await message.bot.get_chat(user_id)
            await message.bot.send_message(chat.id, text, parse_mode="HTML")
        except ChatNotFound:
            print(f"User {user_id} not found")
        except Exception as e:
            print(f"Failed to send message to user {user_id}. Error: {e}")
    sent_message = await message.answer('Рассылка прошла успешно')
    await asyncio.sleep(1)
    await message.bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)
    await message.answer('Вы в админ-панели', reply_markup=main_menu)

#рассылка с помощью команды
async def spam_cmd(message:Message):
    text = message.text[6:]
    users = db.get_users()
    for row in users:
        user_id = row[0]
        try:
            chat = await message.bot.get_chat(user_id)
            await message.bot.send_message(chat.id, text, parse_mode="Markdown")
        except ChatNotFound:
            print(f"User {user_id} not found")
        except Exception as e:
            print(f"Failed to send message to user {user_id}. Error: {e}")
    await message.answer('Рассылка прошла успешно')

#---Меню пользователи---
#Обработка кнопки пользователи
async def users_call(call):
    quantity = db.get_user_count()
    await call.message.edit_text(f'Количество активных пользователей: {quantity}', reply_markup=users_menu)

#Обработка кнопки активные пользователи
async def active_users_call(call):
    keyboard = create_keyboard()
    await call.message.edit_text('Активные пользователи', reply_markup=keyboard)

#Обработка кнопки забаненные пользователи
async def banned_users_call(call):
    keyboard = create_ban_keyboard()
    await call.message.edit_text('Активные пользователи', reply_markup=keyboard)

async def back_to_main_menu(call):
    await call.message.edit_text('Вы в админ-панели:', reply_markup=main_menu)

#нажатие кнопки назад в блоке ниже меню пользователей(возврат в меню пользователей)
async def back_to_users_call(call):
    await call.message.edit_text('Вы в админ-панели:', reply_markup=users_menu)


#нажатие на кнопку пользователя в блоке активные пользователи
async def user_info_call(call):
    global dm_user_id
    dm_user_id = call.data.split('_')[1]
    user = db.get_user(dm_user_id)
    global user_info_text
    user_info_text = f"{user[1]} (@{user[2]}) - зарегистрирован {user[3],} баланс {user[4]}"

    ban_button = InlineKeyboardButton('Забанить', callback_data=f'ban_user_{dm_user_id}')
    direct_message = InlineKeyboardButton('Личное Сообщение', callback_data='direct_message')
    add_balance =  InlineKeyboardButton('Добавить баланс', callback_data='add_balance')
    back_to_users = InlineKeyboardButton('Назад', callback_data='back_to_users')

    global users_func
    users_func = InlineKeyboardMarkup().add(ban_button, direct_message).add(back_to_users, add_balance)

    await call.message.edit_text(text=call.message.text + f"\n\n{user_info_text}", reply_markup=users_func)

async def add_balance(call):
    await call.message.edit_text('Пополнить баланс на:')
    await BalanceState.waiting_for_add_balance.set()

async def wait_add(message: Message, state: FSMContext):
    user_id = message.from_user.id
    amount = int(message.text)
    await state.finish()
    db.add_balance(user_id, amount)
    await message.answer('Баланс успешно пополнен!')


async def banned_user_info_call(call):
    user_id = call.data.split('_')[2]
    user = db.get_banned_user(user_id)

    text = f"{user[1]} (@{user[2]}) - зарегистрирован {user[3]}"

    ban_button = InlineKeyboardButton('Разбанить', callback_data=f'unban_user_{user_id}')
    back_to_users = InlineKeyboardButton('Назад', callback_data='back_to_banned_users')
    global ban_users_func
    ban_users_func = InlineKeyboardMarkup().add(ban_button).add(back_to_users)

    await call.message.edit_text(text=call.message.text + f"\n\n{text}", reply_markup=ban_users_func)

#обработчик кнопки назад (возврат к клавиатуре с активными польователями)
async def user_back(call):
    keyboard = create_keyboard()
    await call.message.edit_text('Список пользователей:', reply_markup=keyboard)


#тоже самое что выше, только в забанненых
async def banned_user_back(call):
    keyboard = create_ban_keyboard()
    await call.message.edit_text('Список пользователей:', reply_markup=keyboard)

#обработчик кнопки Забанить
async def ban_user(call):
    user_id = call.data.split('_')[2]
    chat = await call.bot.get_chat(user_id)
    username = chat.username

    db.ban_user(user_id)

    sent_message = await call.message.answer(f"Пользователь @{username} забанен!")
    await asyncio.sleep(3)
    await call.bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)


async def unban_user(call):
    user_id = call.data.split('_')[2]
    print(user_id)
    chat = await call.bot.get_chat(user_id)
    username = chat.username

    db.unban_user(user_id)

    sent_message = await call.message.answer(f"Пользователь @{username} разбанен!")
    await asyncio.sleep(3)
    await call.bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)

#обработчик кнопки личное сообщение пользователю

async def direct_message(call):
    await call.message.edit_text('Напишите сообщение для рассылки:', reply_markup=back_users_func)
    await SpamState.waiting_for_dm_text.set()

async def get_direct_message_text(message: Message, state: FSMContext):
    dm_text = message.text
    await state.finish()
    user_id = dm_user_id
    try:
        chat = await message.bot.get_chat(user_id)
        await message.answer(chat.id, dm_text, parse_mode="HTML")
    except ChatNotFound:
        print(f"User {user_id} not found")
    except Exception as e:
        print(f"Failed to send message to user {user_id}. Error: {e}")

    sent_message = await message.answer("Личное сообщение пользователю отправлено.")
    await asyncio.sleep(1)
    await message.bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)
    await message.answer('Вы в админ-панели', reply_markup= main_menu)

async def back_to_user_func(call, state: FSMContext):
    await state.reset_state()  # сбрасывается состояние ожидания сообщения
    await call.message.edit_text(user_info_text, reply_markup=users_func)