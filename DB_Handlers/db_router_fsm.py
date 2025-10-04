from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from sqlalchemy.ext.asyncio import AsyncSession

from Middlewares import DataBaseSession

from DataBase.orm_query import  orm_add_card
from DataBase.engine import engine, session_maker # движок и создание сессии
from Models.TableModels import Attributes # наша модель
from Statements.User_statements import UserStatements





db_router = Router()
db_router.message.middleware(DataBaseSession(session_pool=session_maker))
db_router.callback_query.middleware(DataBaseSession(session_pool=session_maker))

# начало режима сбора инфы
@db_router.message(Command('start_search'))
async def process_name(message: Message, state: FSMContext):
    await message.answer("Давайте создадим ваш профиль.Пожалуйста введите свое имя")
    await state.set_state(UserStatements.name)

# 2. СОХРАНЕНИЕ ИМЕНИ
@db_router.message_handler(state=UserStatements.name)
async def process_name(message: Message, state: FSMContext):
    name = message.text.strip()
    if len(name) < 2:
        await message.answer("❌ Имя слишком короткое. Введите еще раз:")
        return
    await state.update_data(name=name)
    await state.set_state(UserStatements.age)
    await message.answer("✅ Имя сохранено!\n\nШаг 2/8: Введите ваш возраст:")

# 3. СОХРАНЕНИЕ Возраста
@db_router.message_handler(state=UserStatements.age)
async def process_age(message: Message, state: FSMContext):
    age = message.text.strip()
    if not age.isdigit():
        await message.answer("❌Пожалуйста, введите возраст")
        return
    if 100 < int(age) < 2:
        await message.answer("❌ Прекрати заниматься хуйней и введи свой нормальный возраст")
        return
    
    await state.update_data(age=age)
    await state.set_state(UserStatements.city)
    await message.answer("✅ Возраст сохранен, пожалууйста введите город проживания")

# 4. СОХРАНЕНИЕ Города
@db_router.message_handler(state=UserStatements.city)
async def process_city(message: Message, state: FSMContext):
    city = message.text.strip()
    if len(city) == len(set(city)):
        await message.answer("введите реальный город а не набор букв")
    await state.update_data(city = city)
    await state.set_state(UserStatements.social_status)
    await message.answer("✅ Место проживания сохранено, введите свой социальный статус(не из ВК)")

# 5. СОХРАНЕНИЕ Статуса
@db_router.message_handler(state=UserStatements.social_status)
async def process_status(message: Message, state: FSMContext):
    status  = message.text.strip()
    if status not  in ['холост', 'женат', 'не женат', 'замужем','в разводе', 'разведен', 'разведена','в активном поиске','свободен','свободна', 'вдовец','вдова']:
        await message.answer("Пожалуйста введите точную информацию, например женат/не женат/холост")
        return

    await state.update_data(social_status = status)
    await state.set_state(UserStatements.description)
    await message.answer("✅ Ваш соц статус сохранен, пожалуйста добавьте пару слов о себе")

# 6. СОХРАНЕНИЕ СЕМЕЙНОГО СТАТУСА (последний степ)
@db_router.message_handler(state=UserStatements.description)
async def process_family_status(message: Message, state: FSMContext, session:AsyncSession):
    description = message.text.strip().lower()

    await state.update_data(description = description)

    current_user_info = await state.get_data() # собираем всю инфу заполненную юзером
    current_user_info['id_telegeam_user'] = message.from_user.id
    orm_add_card(session=session,data=current_user_info)

    await state.clear()
    await message.answer("Поздравляю, ваша карточка создана и успешно сохранена")

# 8. КОМАНДА ОТМЕНЫ
@db_router.message_handler(commands=['cancel'], state="*")
async def cancel_registration(message:Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state:
        await state.finish()
        await message.answer("❌ Регистрация отменена.")