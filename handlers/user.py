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
@dp.message_handler(text="📕 Расписание", state="*")
async def info_handler(message: Message, state: FSMContext):
    sch = get_shedule(message.from_user.id)
    text = ""
    for k, v in sch.items():
        if v == []:
            continue
        text += f"<b>{k}</b> :\n"
        for i in v:
            for j in i:
                if j == i[0] or j == i[3]:
                    text += f"<code>{j}</code> | "
                else:
                    text += f"{j} | "
            text += "\n\n"
        text += "\n\n"
    await message.answer(text)



@dp.message_handler(text="👤 Профиль", state="*")
async def info_handler(message: Message, state: FSMContext):
     await message.answer(await get_profile_text(message.from_user.id))


@dp.callback_query_handler(text_startswith="return_subjects", state="*")
@dp.message_handler(text="📁 Предметы", state="*")
async def info_handler(message: Union['Message', 'CallbackQuery'], state: FSMContext):
    try:
        await message.answer("Предметы", reply_markup=await get_subjects_inl(message.from_user.id))
    except:
        await message.message.edit_text("Предметы", reply_markup=await get_subjects_inl(message.from_user.id))

@dp.callback_query_handler(text_startswith="/StudentJurnal", state="*")
async def insert_login(message: Union['Message', 'CallbackQuery'], state: FSMContext):
    await message.message.edit_text("Есть только один флаг и он такой же черный, как черно дно марианской впадины...\n<b>Жди матрос!</b>")
    link = message.data
    subject = get_subject(message.from_user.id, link)
    text = f"Оценки по предмету: <code>{subject[14]}</code>\n" \
           f"Преподаватель: <code>{subject[15]}</code>\n\n"
    print(len(subject))
    if len(subject) >= 17:
        k = 1
        text1 = ['Тест', 'Устно', 'Письменно', '', '', '', '', '', '', 'Итог коллок	', 'Допбалл', 'Сумма', 'Оценка']
        for i in range(len(subject[:13])):
            if i in [0, 3, 6]:
                type = text1[0]
            elif i in [1, 4, 7]:
                type = text1[1]
            elif i in [2, 5, 8]:
                type = text1[2]
            if i == 3 or i == 6 or i >= 9:
                k += 1
                text += '\n'
            if i < 9:
                text += f"{k}-{type}: <code>{subject[i]}\n</code>"
            else:
                text += f"{text1[i]}: <code>{subject[i]}\n</code>"

        await message.message.edit_text(text, reply_markup=await return_subjects_inl())


