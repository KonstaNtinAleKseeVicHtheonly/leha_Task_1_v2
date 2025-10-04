from aiogram.fsm.state import StatesGroup, State


class UserStatements(StatesGroup):
    id = State()
    name = State()
    age = State()
    vacant = State()
    salary = State()
    description = State()