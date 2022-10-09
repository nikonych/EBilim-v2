# - *- coding: utf- 8 - *-
from aiogram import Dispatcher
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault

user_commands = [
    BotCommand("start", "♻ Перезапустить бота")
]


async def set_commands(dp: Dispatcher):
    await dp.bot.set_my_commands(user_commands, scope=BotCommandScopeDefault())
