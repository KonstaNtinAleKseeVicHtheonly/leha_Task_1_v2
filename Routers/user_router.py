from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext

from Keyboards import key_board_user_menu, return_to_menu, vacant_buttons, check_user_buttons

from Statements import UserStatements

from Filters import IsValidField, IsValidNumber

from Decorators import AutoDeleteMessage

user_router = Router()


@user_router.callback_query(F.data == "back_to_menu")
@user_router.message(CommandStart())
@AutoDeleteMessage(num_id_prew=0)
async def start_user(update: Message | CallbackQuery, state: FSMContext) -> None:
    if isinstance(update, Message):
        await update.answer("""
Добро пожаловать в бота, Пользователь
Выберите действие по кнопкам ниже:
""", reply_markup=key_board_user_menu())
    else:
        await update.message.answer("""
Добро пожаловать в бота, Пользователь
Выберите действие по кнопкам ниже:
""", reply_markup=key_board_user_menu())
    await state.clear()
    

@user_router.callback_query(F.data == "reset")
@user_router.message(StateFilter(None), F.text.lower() == "создать карточку")
@AutoDeleteMessage(num_id_prew=1)
async def name_user(update: Message | CallbackQuery, state: FSMContext):
    if isinstance(update, Message):
        await update.answer("""
Введи свое имя
Условие: от 3 до 30 символов, латинскими маленькими или большими буквами, цифры и символ "_":
""", reply_markup=return_to_menu())
    else:
        await update.message.answer("""
Введи свое имя
Условие: от 3 до 30 символов, латинскими маленькими или большими буквами, цифры и символ "_":
""", reply_markup=return_to_menu())
    await state.set_state(UserStatements.name)
    
    
@user_router.message(UserStatements.name, IsValidField('_', 3, 30))
@AutoDeleteMessage(num_id_prew=1)
async def age_user(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("""
Введи возраст
Условие: целочисленное от 1 до 149:
""", reply_markup=return_to_menu())
    await state.set_state(UserStatements.age)
    
@user_router.message(UserStatements.name)
@AutoDeleteMessage(num_id_prew=1)
async def name_user(message: Message, state: FSMContext):
    await message.answer("""
Введи корректное имя
Условие: от 3 до 30 символов, латинскими маленькими или большими буквами, цифры и символ "_":
""", reply_markup=return_to_menu())
    
    
@user_router.message(UserStatements.age, IsValidNumber(1, 149))
@AutoDeleteMessage(num_id_prew=1)
async def vacant_user(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("""
Выбери должность из предложенных внизу или нажми кнопку Вернуться в меню, чтобы отменить рег карточки:
""", reply_markup=vacant_buttons(["сотрудник", "начотдела", "старший спец", "техлид"]))
    await state.set_state(UserStatements.vacant)
    
    
@user_router.message(UserStatements.age)
@AutoDeleteMessage(num_id_prew=1)
async def age_user(message: Message, state: FSMContext):
    await message.answer("""
Введи корректный возраст
Условие: целочисленное от 1 до 149:
""", reply_markup=return_to_menu())
    

@user_router.callback_query(F.data.func(lambda x: x in ["сотрудник", "начотдела", "старший спец", "техлид"]))
@AutoDeleteMessage(num_id_prew=1)
async def salary_user(update: CallbackQuery, state: FSMContext):
    await state.update_data(vacant=update.data)
    await update.message.answer("""
Если есть, укажите заработную плату
Условие: в диапазоне от 10000 до 150000 у.е.:
""", reply_markup=return_to_menu())
    await state.set_state(UserStatements.salary)
    

@user_router.message(UserStatements.salary, IsValidNumber(10000, 150000))
@AutoDeleteMessage(num_id_prew=1)
async def description_user(message: Message, state: FSMContext):
    await state.update_data(salary=message.text)
    await message.answer("""
Укажите дополнительную информацию:
""", reply_markup=return_to_menu())
    await state.set_state(UserStatements.description)
    

@user_router.message(UserStatements.salary)
@AutoDeleteMessage(num_id_prew=1)
async def salary_user(message: Message, state: FSMContext):
    await message.answer("""
Укажите корректную заработную плату
Условие: в диапазоне от 10000 до 150000 у.е.:
""", reply_markup=return_to_menu())
    
@user_router.message(UserStatements.description)
@AutoDeleteMessage(num_id_prew=1)
async def check_data_before_sender(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    await message.answer(f"""
Проверьте данные:
Имя: {data["name"]}
Возраст: {data["age"]}
Должность: {data["vacant"]}
Заработная плата: {data["salary"]}
Дополнительно: {data["description"]}
""", reply_markup=check_user_buttons())
    
