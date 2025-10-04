from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext

from Keyboards import key_board_admin_menu, return_to_menu

from Statements import AdminStatements

from Filters import IsValidField, IsValidNumber, IsAdmin

from Decorators import AutoDeleteMessage

admin_router = Router()

@admin_router.callback_query(F.data == "back_to_menu")
@admin_router.message(IsAdmin(), CommandStart())
@AutoDeleteMessage(num_id_prew=0)
async def admin_start(update: Message | CallbackQuery, state: FSMContext):
    if isinstance(update, Message):
        await update.answer("""
Добро пожаловать в бота, Администратор
Выберите действие по кнопкам ниже:
""", reply_markup=key_board_admin_menu())
    else:
        await update.message.answer("""
Добро пожаловать в бота, Администратор
Выберите действие по кнопкам ниже:
""", reply_markup=key_board_admin_menu())
    await state.clear()
    
    
@admin_router.message(StateFilter(None), F.text.lower() == "найти по айди")
@AutoDeleteMessage(num_id_prew=1)
async def admin_enter_id(message: Message, state: FSMContext):
    await message.answer("""
Введи id карточки
Условие: целочисленное значение от 1 до 10 символов:
""", reply_markup=return_to_menu())
    await state.set_state(AdminStatements.id_user)
    
    
@admin_router.message(StateFilter(AdminStatements.id_user))
@AutoDeleteMessage(num_id_prew=1)
async def admin_enter_id(message: Message, state: FSMContext):
    await message.answer("""
Введи корректный id карточки
Условие: целочисленное значение от 1 до 10 символов:
""", reply_markup=return_to_menu())
    
    
