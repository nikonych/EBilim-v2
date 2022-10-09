# - *- coding: utf- 8 - *-
from datetime import datetime, timedelta

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp, bot
import data.config as config
from services.parser import get_subjects


#from tgbot.services.api_sqlite import get_paymentx, get_crystal, get_yoo, get_settingsx






async def accept_license(user_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Пользовательское соглашение",
                                   url="https://medium.com/@mamixkik/%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8C%D1%81%D0%BA%D0%BE%D0%B5-%D1%81%D0%BE%D0%B3%D0%BB%D0%B0%D1%88%D0%B5%D0%BD%D0%B8%D0%B5-%D0%B4%D0%BB%D1%8F-%D0%BF%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F-1cebb7b9a69e"),
        )
    keyboard.add(InlineKeyboardButton(text="Прочитал и Согласен", callback_data=f'add_user:{user_id}'))
    return keyboard


async def get_subjects_inl(user_id):
    keyboard = InlineKeyboardMarkup()
    subjects = get_subjects(user_id)
    for k, v in subjects.items():
        keyboard.add(InlineKeyboardButton(k, callback_data=f"{v}"))
    return keyboard

async def return_subjects_inl():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("Назад", callback_data="return_subjects")
    )

    return keyboard