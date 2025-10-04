from aiogram.filters import BaseFilter
from aiogram.types import Message

from string import ascii_lowercase as al, ascii_uppercase as au, digits as dig


class IsValidField(BaseFilter):
    def __init__(self, allow_chars: str, min_len: int, max_len: int):
        self.allow_chars = allow_chars
        self.min_len = min_len
        self.max_len = max_len

    async def __call__(self, message: Message):
        return self.min_len <= len(message.text) <= self.max_len and all([ch in al + au + dig + self.allow_chars for ch in message.text])
    

class IsValidNumber(BaseFilter):
    def __init__(self, min_len: int, max_len: int):
        self.min_len = min_len
        self.max_len = max_len

    async def __call__(self, message: Message):
        if message.text:
            try:
                return self.min_len <= int(message.text) <= self.max_len
            except ValueError:
                return False
        else:
            return 0