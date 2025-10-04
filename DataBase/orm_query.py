from typing import Any, Dict
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from Models import Attributes # импорт модели БД

# Здесь пропишем все запросы удаления, добавления, изменения (асинхронка)



async def orm_add(session:AsyncSession, table):
    '''добавление записи в таблицу'''
    session.add(table)
    await session.commit()

async def orm_add_card(session:AsyncSession, data):
    '''создание строки с карточкой товара'''
    # Получаем список допустимых атрибутов модели
    valid_attrs = {column.name for column in Attributes.__table__.columns}
    # Фильтруем входные данные, оставляя только допустимые атрибуты
    filtered_data = {key: value for key, value in data.items() if key in valid_attrs}

    obj = Attributes(**filtered_data) # записывает с отфильтроваными значениями

    session.add(obj)
    await session.commit()

async def orm_get_all_cards(session:AsyncSession)-> Dict[str, Any]:
    '''запрос на возрат всех строк модели'''
    query = select(Attributes)
    result = await session.execute(query)
    if result:
        return result.scalars().all()
    return False

async def orm_get_card(session: AsyncSession, id_: int) -> Dict[str, Any]:
    '''запрос на возрващение строки по указанному id, если такого юзера нет, вернет False'''
    query = select(Attributes).where(Attributes.id_telegram_user == id_)
    if query:
        result = await session.execute(query)
        return result.scalar()
    return False

async def orm_update_card(session: AsyncSession, id_: int, table_data) -> None:
    '''обновленеи строки в таблице по указанном id (словарь table_data собирается после всех fsm с накопившейся инфой
    ,которую пользователь отправил)'''
    dictionary = {attr: getattr(table_data, attr) for attr in table_data.__dict__ if not attr.startswith("_")}
    # старый вариан тquery = update(Attributes).where(Attributes.id_telegram_user == id_).values(
    # name = table_data["name"],
    #price = float(table_data['price'])
    #)
    # актуальный вариант, если не сработает, менять на старый
    query = update(Attributes).where(Attributes.id_telegram_user == id_).values(dictionary)
    await session.execute(query)
    await session.commit()

async def orm_delete_card(session: AsyncSession, id_: int) -> None:
    '''удаление строки товара'''
    query = delete(Attributes).where(id_== Attributes.id_telegram_user)
    await session.execute(query)
    await session.commit()