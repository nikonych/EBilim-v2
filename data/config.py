# - *- coding: utf- 8 - *-
import configparser
import sqlite3
from random import choice

read_config = configparser.ConfigParser()
read_config.read('settings.ini')

DATABASE_PATH = 'data/database.db'  # Путь к БД
BOT_TOKEN = read_config['settings']['token'].strip()
PATH_LOGS = 'data/logs.log'  # Путь к Логам



async def updatelink(name, link):
    edit = configparser.ConfigParser()
    edit.read("settings.ini")
    links = edit["links"]
    links[name] = link
    with open("settings.ini", 'w') as file:
        edit.write(file)



async def get_choose_withdraw():
    return list(read_config['settings']['choose_withdraw'].split(','))

async def get_rand_mega_acc():
    return list(choice(list(read_config['settings']['accs_mega'].split(','))).split(':'))


def get_last_admins():
    with sqlite3.connect(DATABASE_PATH) as con:
        con.row_factory = lambda cursor, row: row[0]
        sql = "SELECT user_id FROM users where status= 'Admin'"
        return con.execute(sql).fetchall()

# Получение администраторов бота
def get_admins():
    admins = []
    admins_from_sql = get_last_admins()
    for admin in admins_from_sql:
        admins.append(admin)

    return admins