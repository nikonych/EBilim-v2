# - *- coding: utf- 8 - *-
import logging as bot_logger
import os
import sys
from datetime import datetime

import colorama
from aiogram import executor, Dispatcher
from colorama import Fore


from handlers import dp
from loader import scheduler
from services.api_session import RequestsSession
from middlewares import setup_middlewares
from services.dbhandler import create_dbx
from utils.misc.bot_commands import set_commands

# from utils.misc_functions import update_logs_day, update_logs_week, update_logs_month

colorama.init()


# Запуск шедулеров
# async def scheduler_start():
#     scheduler.add_job(update_logs_week, "cron", day_of_week="fri", hour=00)
#     scheduler.add_job(update_logs_day, "cron", hour=00)
#     scheduler.add_job(update_logs_month, "cron", day=9, hour=00)


# Выполнение функции после запуска бота
async def on_startup(dp: Dispatcher):
    await dp.bot.get_updates(offset=-1)
    dp.bot['rSession'] = RequestsSession()

    # await scheduler_start()
    await set_commands(dp)

    bot_logger.exception("BOT WAS STARTED")
    print(Fore.LIGHTYELLOW_EX + "~~~~~ Bot was started ~~~~~")
    print(Fore.RESET)


# Выполнение функции после выключения бота
async def on_shutdown(dp: Dispatcher):
    rSession: RequestsSession = dp.bot['rSession']
    await rSession.close()
    await dp.storage.close()
    await dp.storage.wait_closed()
    await (await dp.bot.get_session()).close()

    if sys.platform.startswith("win"):
        os.system("cls")
    else:
        os.system("clear")


if __name__ == "__main__":
    create_dbx()

    scheduler.start()
    setup_middlewares(dp)

    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)