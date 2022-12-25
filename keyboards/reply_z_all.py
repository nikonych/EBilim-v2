# - *- coding: utf- 8 - *-
from aiogram.types import ReplyKeyboardMarkup

from data.config import get_admins


# from tgbot.data.config import get_admins


# Кнопки главного меню
# from tgbot.services.api_sqlite import get_userx


def menu_frep(user_id):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("👤 Профиль", "📥 Транскрипт")
    keyboard.row("📁 Предметы", "📕 Расписание")
    keyboard.row("😈 Темные делишки")

    if user_id in get_admins():
        keyboard.row("⚙ Админ панель")
    #     keyboard.row("🎁 Реферальная система", "🔒Админ панель")
    #     # keyboard.row("🛍 Управление товарами", "📜 Статистика")
    #     # keyboard.row("⚙ Настройки", "🔆 Общие функции", "🔑 Платежные системы")
    # else:
    #     keyboard.row("🎁 Реферальная система")

    return keyboard


def darknet(user_id):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Тесты", "Лабораторные")
    keyboard.row("Экзамены", "Домашки")
    keyboard.row("Инструкция")
    keyboard.row("Назад")


    return keyboard