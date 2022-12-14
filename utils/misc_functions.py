# - *- coding: utf- 8 - *-
import asyncio
from datetime import datetime

import requests
from aiogram import Dispatcher
from bs4 import BeautifulSoup

from loader import bot
from services.dbhandler import get_all_trans, update_transx
from services.parser import get_transkript2, get_transkript_only_num, get_transkript_only_sub_names


# Рассылка сообщения всем администраторам
# async def send_admins(message, markup=None, not_me=0):
#     for admin in get_admins():
#         if markup == "default":
#             markup = menu_frep(admin)
#
#         try:
#             if str(admin) != str(not_me):
#                 await bot.send_message(admin, message, reply_markup=markup, disable_web_page_preview=True)
#         except:
#             pass


# Автоматическая очистка ежедневной статистики после 00:00
# async def update_logs_day():
#     print("day_start")
#     update_logs(daylogs=0, daycolds=0)
#
# async def update_logs_week():
#     update_logs(weeklogs=0, weekcolds=0)
#


async def check_trans():
    all_trans = get_all_trans()
    for user in all_trans:
        info = get_transkript_only_num(user['user_id'])
        print(info)
        flag = False
        c = -1
        print(user)
        for k, v in user.items():
            flag = False
            if c == -1:
                c += 1
                continue
            if float(v) != info[c]:
                flag = True
            if flag:
                sub_names = get_transkript_only_sub_names(user['user_id'])
                print(sub_names)
                print(k, c)
                await bot.send_message(user['user_id'], f"Поставили оценку!\n"
                                                  f"<b>{sub_names[c]}</b> - <code>{info[c]}</code>")
            c += 1
        update_transx(user_id=user['user_id'], f1=info[0],f2=info[1],f3=info[2],f4=info[3],f5=info[4],f6=info[5],f7=info[6])





async def update_logs_month():
    await check_trans()

