# - *- coding: utf- 8 - *-
import math
import random
import sqlite3

from data.config import DATABASE_PATH
from utils.const_functions import get_unix, get_date, clear_html


# Преобразование полученного списка в словарь
def dict_factory(cursor, row):
    save_dict = {}

    for idx, col in enumerate(cursor.description):
        save_dict[col[0]] = row[idx]

    return save_dict


####################################################################################################
##################################### ФОРМАТИРОВАНИЕ ЗАПРОСА #######################################
# Форматирование запроса без аргументов
def update_format(sql, parameters: dict):
    if "XXX" not in sql:
        sql += " XXX "

    values = ", ".join([
        f"{item} = ?" for item in parameters
    ])
    sql = sql.replace("XXX", values)

    return sql, list(parameters.values())


# Форматирование запроса с аргументами
def update_format_args(sql, parameters: dict):
    sql = f"{sql} WHERE "

    sql += " AND ".join([
        f"{item} = ?" for item in parameters
    ])

    return sql, list(parameters.values())



####################################################################################################
########################################### ЗАПРОСЫ К БД ###########################################
# Добавление пользователя
def add_userx(user_id, user_login, user_name, inai_login, inai_password):
    with sqlite3.connect(DATABASE_PATH) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO users "
                    "(user_id, user_login, user_name, inai_login, inai_password, status) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    [user_id, user_login, user_name, inai_login, inai_password, 'Матрос'])
        con.commit()


def remove_req(**kwargs):
    with sqlite3.connect(DATABASE_PATH) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM request"
        sql, parameters = update_format_args(sql, kwargs)
        con.execute(sql, parameters)
        con.commit()


def get_req(**kwargs):
    with sqlite3.connect(DATABASE_PATH) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM request"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()

def get_reqs(**kwargs):
    with sqlite3.connect(DATABASE_PATH) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM request"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()

# Получение настроек чатов
def get_settings(**kwargs):
    with sqlite3.connect(DATABASE_PATH) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM settings"
        return con.execute(sql).fetchone()

# Получение пользователя
def get_userx(**kwargs):
    with sqlite3.connect(DATABASE_PATH) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM users"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()


def isBan(user_id):
    with sqlite3.connect(DATABASE_PATH) as con:
        con.row_factory = dict_factory
        sql = f"SELECT is_banned FROM users where `user_id` = {user_id}"
        try:
            return con.execute(sql).fetchall()[0]['is_banned']
        except:
            return False

# Получение пользователей
def get_usersx(**kwargs):
    with sqlite3.connect(DATABASE_PATH) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM users"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()


# Получение всех пользователей
def get_all_usersx():
    with sqlite3.connect(DATABASE_PATH) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM users"
        return con.execute(sql).fetchall()


# Получение всех  user_id  пользователей
def get_all_users_id():
    with sqlite3.connect(DATABASE_PATH) as con:
        con.row_factory = lambda cursor, row: row[0]
        sql = "SELECT user_id FROM users"
        return con.execute(sql).fetchall()


# Редактирование пользователя
def update_userx(user_id, **kwargs):
    with sqlite3.connect(DATABASE_PATH) as con:
        con.row_factory = dict_factory
        sql = f"UPDATE users SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(user_id)
        con.execute(sql + "WHERE user_id = ?", parameters)
        con.commit()


# Создание всех таблиц для БД
def create_dbx():
    with sqlite3.connect(DATABASE_PATH) as con:
        con.row_factory = dict_factory

        # Создание БД с хранением данных пользователей
        if len(con.execute("PRAGMA table_info(users)").fetchall()) == 7:
            print("All db was found")
        else:
                con.execute("CREATE TABLE users("
                            "user_id INTEGER PRIMARY KEY ,"
                            "user_login TEXT,"
                            "user_name Text,"
                            "inai_login text,"
                            "inai_password text,"
                            "status text,"
                            "is_banned boolean default FALSE)")
                print("DB was not found(1) | Creating...")

            # Создание БД с хранением данных настроек
        if len(con.execute("PRAGMA table_info(settings)").fetchall()) == 2:
            print("DB was found(2)")
        else:
            con.execute("CREATE TABLE settings("
                        "is_work boolean default true,"
                        "week_num int default 1)")

            con.execute("INSERT INTO settings("
                        "is_work) "
                        "VALUES (?)",
                        [True])
            print("DB was not found(2) | Creating...")


            #
            # if len(con.execute("PRAGMA table_info(storage_subcategory)").fetchall()) == 4:
            #     print("DB was found(11)")
            # else:
            #     con.execute("create table storage_subcategory("
            #                 "increment integer,"
            #                 "subcategory_id integer,"
            #                 "subcategory_name text,"
            #                 "category_id integer"
            #                 ")")
            #     print("DB was not found(11) | Creating...")

        con.commit()