from aiogram.dispatcher.filters.state import State, StatesGroup

class SpamState(StatesGroup):
    waiting_for_spam_text = State()

    waiting_for_dm_text = State()

class BalanceState(StatesGroup):
    waiting_for_add_balance = State()