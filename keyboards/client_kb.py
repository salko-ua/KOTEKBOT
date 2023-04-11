from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data_base.controller_db import *
from data_base.controller_db import group_list_sql


# KeyboardButton - створює одну кнопку
# ReplyKeyboardMarkup - створює клавіатуру
# ReplyKeyboardRemove - видаляє клавіатуру


# ===========================1 Keyboards================================
async def get_kb():
    h = await group_list_sql()
    kb_course = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(0, len(h)):
        kb_course.insert(h[i])
    return kb_course.add(KeyboardButton("Назад"))


# ======================================================================


# ===========================2 Keyboards================================
kb1 = KeyboardButton("Розклад пар 👀")
kb2 = KeyboardButton("Розклад дзвінків ⌚️")
kb3 = KeyboardButton("Ч/З тиждень ✏️")
kb4 = KeyboardButton("Змінити групу 🚫")
kb5 = KeyboardButton("Меню 👥")
kb6 = KeyboardButton("Тривоги ⚠️")
kb7 = KeyboardButton("Замітки 📝")
kb8 = KeyboardButton("Щось буде 🤔")

kb_client = (
    ReplyKeyboardMarkup(resize_keyboard=True).row(kb1, kb2).row(kb6, kb3).row(kb7, kb8).row(kb5, kb4)
)
# ======================================================================
