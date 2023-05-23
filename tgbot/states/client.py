from aiogram.dispatcher.filters.state import State, StatesGroup



class CryptoState(StatesGroup):
    choose_crypto = State()
    choose_bank = State()
    enter_tips = State()
    enter_sum = State()