from aiogram.fsm.state import StatesGroup, State
from pydantic import BaseModel, Field, validator 
from typing import Optional

# для FSM дл CRUD операций
class CrudUserStates(StatesGroup):
    user_tg_id_get = State()
    user_tg_id_delete = State()
    user_tg_id_update = State()
    choosing_field_for_update = State()  
    updating_chosen_field = State

class UserStatements(StatesGroup):
    '''определяет какие поля будут заполнять в режиме FSM юзером'''
    name = State()
    age = State()
    city = State()
    social_status = State()
    description = State()
    user_tg_id = State() 


# Pydantic модель для валидации данных в FSN
class CardData(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(ge=1, le=120)
    city: str = Field(min_length=2, max_length=50)
    social_status: str = Field(min_length=2, max_length=50)
    description: str = Field(min_length=10, max_length=500)
    id_telegram_user: Optional[int] = None

    @validator('name')
    def name_must_contain_letters(cls, v):
        if not any(c.isalpha() for c in v):
            raise ValueError('Имя должно содержать буквы')
        return v.title()

    @validator('age')
    def age_must_be_reasonable(cls, v):
        if v < 1:
            raise ValueError('Возраст должен быть положительным числом')
        return v
    
# пример применения в хэнжлерах FSM 
#   try:
#         # Пробуем провалидировать имя
#         card_data = CardData(name=message.text)
#         await state.update_data(name=message.text)
#         await message.answer("Отлично! Теперь введите ваш возраст:")
#         await state.set_state(CardStates.age)
#     except ValidationError as e:
#         error_msg = e.errors()[0]['msg']
#         await message.answer(f"❌ Ошибка: {error_msg}\nПопробуйте еще раз:")