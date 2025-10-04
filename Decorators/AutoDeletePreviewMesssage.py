import functools

from sqlalchemy.ext.asyncio import AsyncSession

from create_bot import bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext


# Пример класса - декоратора для асиньки
class AutoDeleteMessage:
    def __init__(self, num_id_prew):
        self.num_id_prew = num_id_prew

    def __call__(self, func):
        @functools.wraps(func)
        async def inner_decorate(update: Message | CallbackQuery, **kwargs):
            if isinstance(update, Message):
                await bot.delete_message(chat_id=update.chat.id, message_id=update.message_id - self.num_id_prew)
            else:
                await bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id - self.num_id_prew)
            return await func(update, **kwargs)
        return inner_decorate
