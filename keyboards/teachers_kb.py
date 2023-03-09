from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data_base.controller_db import *


# KeyboardButton - створює одну кнопку
# ReplyKeyboardMarkup - створює клавіатуру
# ReplyKeyboardRemove - видаляє клавіатуру


# ===========================1 Keyboards================================
async def get_t_kb():
    list_teachers = await teachers_name_list_sql()
    kb_name = ReplyKeyboardMarkup(resize_keyboard=True)
    try:
        for i in range(0, len(list_teachers), 2):
            kb_name.add(list_teachers[i]).insert(list_teachers[i + 1])
    except IndexError:
        pass
    return kb_name.add(KeyboardButton("Назад"))


# ======================================================================


# ===========================2 Keyboards================================
kb1 = KeyboardButton("Розклад занять 🥱")
kb2 = KeyboardButton("Розклад дзвінків ⌚️")
kb3 = KeyboardButton("Ч/З 🤨")
kb4 = KeyboardButton("Переєструватись 🤨")
kb5 = KeyboardButton("Меню 👥")
kb_teachers = (
    ReplyKeyboardMarkup(resize_keyboard=True).row(kb1, kb2).row(kb5, kb3).add(kb4)
)
# ======================================================================
