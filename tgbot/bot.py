from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from tgbot.handlers.general import *
from tgbot.handlers.admin import *
from tgbot.handlers.client import *

from tgbot.data.config import TOKEN
from tgbot.states.admin import SpamState
from tgbot.states.admin import BalanceState

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

#общая часть
dp.register_message_handler(start_cmd, commands='start')

#админская часть
dp.register_callback_query_handler(spam_start, text='spam')
dp.register_callback_query_handler(back_to_main, text='back_to_main', state=SpamState)
dp.register_message_handler(get_spam_text, state=SpamState)
dp.register_message_handler(spam_cmd, commands='spam')

dp.register_callback_query_handler(users_call, text='users')

dp.register_callback_query_handler(active_users_call, text='active_users')
dp.register_callback_query_handler(banned_users_call, text='banned_users')
dp.register_callback_query_handler(back_to_main_menu, text='back_to_main')

dp.register_callback_query_handler(user_info_call, lambda c: c.data.startswith('user_'))
dp.register_callback_query_handler(add_balance, text='add_balance')
dp.register_message_handler(wait_add, state=BalanceState.waiting_for_add_balance)
dp.register_callback_query_handler(banned_user_info_call, lambda c: c.data.startswith('banned_user_'))
dp.register_callback_query_handler(back_to_users_call, text='back_to_users_menu')

dp.register_callback_query_handler(user_back, text='back_to_users')
dp.register_callback_query_handler(banned_user_back, text='back_to_banned_users')
dp.register_callback_query_handler(ban_user, lambda c: c.data.startswith('ban_user_'))
dp.register_callback_query_handler(unban_user, lambda c: c.data.startswith('unban_user_'))

dp.register_callback_query_handler(direct_message, text='direct_message')
dp.register_callback_query_handler(back_to_user_func, text='back_to_users_func', state=SpamState)
dp.register_message_handler(get_direct_message_text, state=SpamState.waiting_for_dm_text)


#клиентская часть
#главное меню
dp.register_message_handler(buttons_handler, content_types=types.ContentTypes.TEXT)
dp.register_callback_query_handler(profile, text='profile')
dp.register_callback_query_handler(history_menu, text='history')