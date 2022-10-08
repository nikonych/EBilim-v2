import asyncio
import concurrent.futures
import os
import queue
import zipfile
from threading import Thread
from typing import Union

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from keyboards.inline_admin import accept_user_inl
from keyboards.reply_z_all import menu_frep
from keyboards.inline_user import *
from loader import dp, bot
import services.dbhandler as db
from services.parser import *
import time
import data.config as config

from services.user_functions import get_profile_text
from utils.misc.bot_filters import IsNoBan


# Открытие главного меню
@dp.message_handler(IsNoBan() , text=['⬅ Главное меню', '/start'], state="*")
async def main_start(message: Message, state: FSMContext):
    await state.finish()
    get_user = db.get_userx(user_id=message.from_user.id)
    if get_user is not None:
        await message.answer(f"Рад увидеть твою рожу снова!",
                             reply_markup=menu_frep(message.from_user.id))
    else:
        await message.answer("Как юнга в первом плаванье, принимай соглашение!", reply_markup=await accept_license(message.from_user.id))


@dp.callback_query_handler(text_startswith="add_user:", state="*")
async def insert_login(message: Union['Message', 'CallbackQuery'], state: FSMContext):
    await state.finish()
    await message.message.answer("Якорь мне в бухту! Теперь введи логин от eBilim")
    await state.set_state("insert_login")


@dp.message_handler(state='insert_login')
async def gg(message: Message, state: FSMContext):
    await state.update_data(insert_login=message.text)
    await message.answer("Как искатель сокровищ, введи пароль:")
    await state.set_state("insert_password")


@dp.message_handler(state='insert_password')
async def gg(message: Message, state: FSMContext):
    async with state.proxy() as data:
        login = data['insert_login']
    password = message.text
    if check_ebilim(login, password):
        await message.answer("Полных парусов и сухого пороха!", reply_markup=menu_frep(message.from_user.id))
        db.add_userx(message.from_user.id, message.from_user.username, message.from_user.full_name, login, password)
        await state.finish()
    else:
        await message.answer("Проклятье медузы!!! Повторим снова")
        await state.finish()
        await state.set_state('insert_login')



# Профиль
@dp.message_handler(text="📥 Транскрипт", state="*")
async def user_profile(message: Message, state: FSMContext):
    await state.finish()
    info = get_transkript2(message.from_user.id)
    # db.addTranskript(message.from_user.id, info)
    print(info)
    total = 0
    count = 0
    text = ''
    # time.sleep(2)
    for k, v in info.items():
        v = v.split(',')
        pos = k[1].split(" ")
        pos[2] = str(100 - int(pos[2][:-1])) + "%"
        if v[1] == "67":
            if int(float('.'.join(v))) + 1 > 98:
                mark = 5.0
            elif int(float('.'.join(v))) + 1 > 95:
                mark = 4.9
            elif int(float('.'.join(v))) + 1 > 92:
                mark = 4.8
            elif int(float('.'.join(v))) + 1 > 89:
                mark = 4.7
            elif int(float('.'.join(v))) + 1 > 86:
                mark = 4.6
            elif int(float('.'.join(v))) + 1 > 84:
                mark = 4.5
            elif int(float('.'.join(v))) + 1 > 83:
                mark = 4.4
            elif int(float('.'.join(v))) + 1 > 82:
                mark = 4.3
            elif int(float('.'.join(v))) + 1 > 81:
                mark = 4.2
            elif int(float('.'.join(v))) + 1 > 80:
                mark = 4.1
            elif int(float('.'.join(v))) + 1 > 79:
                mark = 4.0
            elif int(float('.'.join(v))) + 1 > 78:
                mark = 3.9
            elif int(float('.'.join(v))) + 1 > 76:
                mark = 3.8
            elif int(float('.'.join(v))) + 1 > 74:
                mark = 3.7
            elif int(float('.'.join(v))) + 1 > 72:
                mark = 3.6
            else:
                mark = 'press F'
            text += '{0}\n {1}\n {2}   {3}\n\n'.format(k[0][:-7], " ".join(pos), int(float('.'.join(v))) + 1, mark)
        else:
            if int(float('.'.join(v))) > 98:
                mark = 5.0
            elif int(float('.'.join(v))) > 95:
                mark = 4.9
            elif int(float('.'.join(v))) > 92:
                mark = 4.8
            elif int(float('.'.join(v))) > 89:
                mark = 4.7
            elif int(float('.'.join(v))) > 86:
                mark = 4.6
            elif int(float('.'.join(v))) > 84:
                mark = 4.5
            elif int(float('.'.join(v))) > 83:
                mark = 4.4
            elif int(float('.'.join(v))) > 82:
                mark = 4.3
            elif int(float('.'.join(v))) > 81:
                mark = 4.2
            elif int(float('.'.join(v))) > 80:
                mark = 4.1
            elif int(float('.'.join(v))) > 79:
                mark = 4.0
            elif int(float('.'.join(v))) > 78:
                mark = 3.9
            elif int(float('.'.join(v))) > 76:
                mark = 3.8
            elif int(float('.'.join(v))) > 74:
                mark = 3.7
            elif int(float('.'.join(v))) > 72:
                mark = 3.6
            else:
                mark = 'press F'
            text += '{0}\n {1}\n {2}   {3}\n\n'.format(k[0][:-7], " ".join(pos), int(float('.'.join(v))), mark)
        total += float('.'.join(v))
        count += 1
    await message.answer(text)
    await message.answer("Средний балл за семестр: " + str(round(total / count, 2)))






# Информация
@dp.message_handler(text="📕 Информация", state="*")
async def info_handler(message: Message, state: FSMContext):
    await state.finish()
    info_kb = await info_buttons(db.get_settings())
    dict_logs = db.get_logs_cols_sum()
    text = config.info_text.format(total_logs=dict_logs['SUM(alllogs)'],
                                   total_colds=dict_logs['SUM(allcolds)'],
                                   day_logs=dict_logs['SUM(daylogs)'],
                                   day_colds=dict_logs['SUM(daycolds)'],
                                   week_logs=dict_logs['SUM(weeklogs)'],
                                   week_colds=dict_logs['SUM(weekcolds)'],
                                   month_logs=dict_logs['SUM(monthlogs)'],
                                   month_colds=dict_logs['SUM(monthcolds)'],
                                   total_users=len(db.get_all_usersx()))
    await message.answer(text,reply_markup=info_kb)







# Доп функции
@dp.message_handler(text="💎 Доп. функции", state="*")
async def additional_functions_handler(message: Message, state: FSMContext):
    await message.answer('⚙️В разработке')