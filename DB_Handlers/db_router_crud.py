from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
#FSM
from aiogram.fsm.context import FSMContext
from Statements.User_statements import UserStatements, CrudUserStates

from sqlalchemy.ext.asyncio import AsyncSession
from Middlewares import DataBaseSession
from DataBase.engine import engine, session_maker # движок и создание сессии

from DataBase.orm_query import  *




db_crud_router = Router()
db_crud_router.message.middleware(DataBaseSession(session_pool=session_maker))
db_crud_router.callback_query.middleware(DataBaseSession(session_pool=session_maker))


@db_crud_router.message_handler(Command('get_userinfo'))
async def start_process(message: Message,state:FSMContext):
    await message.answer("Введите id юзера")
    await state.set_state(CrudUserStates.user_tg_id_get)

@db_crud_router.message_handler(state=CrudUserStates.user_tg_id_get)
async def get_info_by_id(message: Message,state:FSMContext,session:AsyncSession):
    current_id = message.text.strip()
    if not current_id.isdigit():
        await message.answer("Введите числовой id")
        return
    current_user = await orm_get_card(session, current_id)
    if not current_user:
        await message.answer("Указанного юзера нет в базе")
        return
    await message.answer("вот инфа о данном юзере")
    await message.answer(str(current_user))
    # await message.answer(f'''Вот инфа о юзере{current_user.name},
    #                      {current_user.age},
    #                      {current_user.city},
    #                      {current_user.social_status},
    #                      {current_user.description}''')
    await state.clear()


@db_crud_router.message_handler(Command('all_users'))
async def get_all_users_info(message: Message,session:AsyncSession):
    all_users = await orm_get_all_cards(session)
    if not all_users:
        await message.answer("В данный момент нет инфы  о юзерах")
    text = "👥 Список пользователей:\n\n"
    for i, user in enumerate(all_users, 1):
        text += f"{i}. {user.name} | {user.age} лет | {user.city} | {user.social_status}\n"
        text += f"\n📊 Всего: {len(all_users)} пользователей"
        await message.answer(text)


@db_crud_router.message_handler(Command('delete_user'))
async def delete_user(message: Message,state:FSMContext):
    await message.answer("Введите id юзера для удаления")
    await state.set_state(CrudUserStates.user_tg_id_delete)


@db_crud_router.message_handler(state=CrudUserStates.user_tg_id_delete)
async def get_info_by_id(message: Message,state:FSMContext,session:AsyncSession):
    current_id = message.text.strip()
    if not current_id.isdigit():
        await message.answer("Введите числовой id")
        return
    current_user = await orm_get_card(session, current_id)
    if current_user:
        await message.answer("Указанного юзера нет в базе")
        return
    await orm_delete_card(session,current_id)
    await message.answer(f"Юзер с id {current_id} успешно удален")
    await state.clear()


@db_crud_router.message_handler(Command('update_user'))
async def delete_user(message: Message,state:FSMContext):
    await message.answer("Введите id юзера для обновления инфы")
    await state.set_state(CrudUserStates.user_tg_id_update)

@db_crud_router.message_handler(state=CrudUserStates.user_tg_id_update)
async def get_info_by_id(message: Message,state:FSMContext,session:AsyncSession):
    current_id = message.text.strip()
    if not current_id.isdigit():
        await message.answer("Введите числовой id")
        return
    current_user = await orm_get_card(session, current_id)
    if current_user(session, current_id):
        await message.answer("Указанного юзера нет в базе")
        return
    await state.update_data(user_id=current_id, current_user=current_user)
  # Показываем текущие данные и предлагаем выбрать поле
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Имя"), KeyboardButton(text="Возраст")],
            [KeyboardButton(text="Город"), KeyboardButton(text="Статус")],
            [KeyboardButton(text="Описание"), KeyboardButton(text="✅ Готово")]
        ],
        resize_keyboard=True
    )
    
    await message.answer(
        f"📋 Текущие данные пользователя:\n"
        f"• Имя: {current_user.name}\n"
        f"• Возраст: {current_user.age}\n"
        f"• Город: {current_user.city}\n"
        f"• Статус: {current_user.social_status}\n"
        f"• Описание: {current_user.description}\n\n"
        f"Выберите поле для изменения:",
        reply_markup=keyboard
    )
    await state.set_state(CrudUserStates.choosing_field)
    await finish_update(message,state)

# Обработка выбора поля
@db_crud_router.message(CrudUserStates.choosing_field)
async def process_field_choice(message: Message, state: FSMContext):
    field = message.text
    if field == "✅ Готово":
        state.clear()
        return
    valid_fields = ["Имя", "Возраст", "Город", "Статус", "Описание"]
    if field not in valid_fields:
        await message.answer("❌ Выберите поле из списка:")
        return
    # Сохраняем выбранное поле и запрашиваем новое значение
    await state.update_data(selected_field=field)
    field_prompts = {
        "Имя": "Введите новое имя:",
        "Возраст": "Введите новый возраст:",
        "Город": "Введите новый город:",
        "Статус": "Введите новый статус:",
        "Описание": "Введите новое описание:"
    }
    await message.answer(
        field_prompts[field],
        reply_markup=None  # Убираем клавиатуру для ввода текста
    )
    await state.set_state(CrudUserStates.updating_chosen_field)
    
# Обработка нового значения поля
@db_crud_router.message(CrudUserStates.updating_field)
async def process_field_update(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    user_id = data["user_id"]
    field = data["selected_field"]
    new_value = message.text
    
    # Валидация в зависимости от поля
    validation_error = await validate_field(field, new_value)
    if validation_error:
        await message.answer(f"❌ {validation_error}\nПопробуйте еще раз:")
        return
    
    # Обновляем поле в БД
    user = await get_user_by_id(session, user_id)
    field_mapping = {
        "Имя": "name",
        "Возраст": "age", 
        "Город": "city",
        "Статус": "social_status",
        "Описание": "description"
    }
    
    db_field = field_mapping[field]
    setattr(user, db_field, new_value)
    await session.commit()
    
    # Показываем клавиатуру снова для выбора следующего поля
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Имя"), KeyboardButton(text="Возраст")],
            [KeyboardButton(text="Город"), KeyboardButton(text="Статус")],
            [KeyboardButton(text="Описание"), KeyboardButton(text="✅ Готово")]
        ],
        resize_keyboard=True
    )
    
    await message.answer(
        f"✅ Поле '{field}' обновлено!\n"
        f"Выберите следующее поле или нажмите '✅ Готово':",
        reply_markup=keyboard
    )
    await state.set_state(CrudUserStates.choosing_field)
# Завершение обновления
async def finish_update(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data["user_id"]
    
    await message.answer(
        f"🎉 Обновление пользователя #{user_id} завершено!",
        reply_markup=None  # Убираем клавиатуру
    )
    await state.clear()

# Функция валидации полей
async def validate_field(field: str, value: str) -> str:
    if field == "Возраст":
        if not value.isdigit():
            return "Возраст должен быть числом"
        age = int(value)
        if age < 1 or age > 120:
            return "Возраст должен быть от 1 до 120"
    elif field == "Имя":
        if len(value) < 2:
            return "Имя должно содержать минимум 2 символа"
    return ""  # Нет ошибки