from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup


def return_to_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Вернуться в меню", callback_data="back_to_menu")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def vacant_buttons(items: list[str]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for item in items:
        kb.button(text=item, callback_data=item)
    kb.button(text="Вернуться в меню", callback_data="back_to_menu")
    kb.adjust(2,2,1)
    return kb.as_markup(resize_keyboard=True)


def check_user_buttons() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Отправить данные", callback_data="sender")
    kb.button(text="Заполнить заново", callback_data="reset")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)