from aiogram.fsm.state import StatesGroup, State


class AdminStatements(StatesGroup):
    id_user = State()