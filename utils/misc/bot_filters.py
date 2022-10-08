# - *- coding: utf- 8 - *-
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from services.dbhandler import isBan, get_req


class IsChat(BoundFilter):
    async def check(self, message: types.Message):
        if message.chat.id > 0:
            return True
        else:
            return False


class IsNoBan(BoundFilter):
    async def check(self, message: types.Message):
        isban_db = isBan(message.from_user.id)
        if isban_db is not None:
            return True
        else:
            return True



