from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup


def key_board_user_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Создать карточку")
    kb.button(text="Посмотреть карточку")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def key_board_admin_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Просмотреть все")
    kb.button(text="Найти по айди")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)