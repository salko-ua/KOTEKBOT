from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data_base import Database


# KeyboardButton - створює одну кнопку
# ReplyKeyboardMarkup - створює клавіатуру
# ReplyKeyboardRemove - видаляє клавіатуру


# ===========================1 Keyboards================================
async def get_t_kb():
    db = await Database.setup()
    list_teachers = await db.teachers_name_list_sql()
    kb_name = ReplyKeyboardMarkup(resize_keyboard=True)
    try:
        for i in range(0, len(list_teachers), 2):
            kb_name.add(list_teachers[i]).insert(list_teachers[i + 1])
    except IndexError:
        pass
    return kb_name.add(KeyboardButton("Меню 👥"))


# ======================================================================


# ===========================2 Keyboards================================
kb1 = KeyboardButton("Розклад занять 👀")
kb2 = KeyboardButton("Розклад дзвінків ⌚️")
kb3 = KeyboardButton("Ч/З тиждень ✏️")
kb4 = KeyboardButton("Вийти 🚫")
kb5 = KeyboardButton("Меню 👥")
kb6 = KeyboardButton("Тривоги ⚠️")
kb7 = KeyboardButton("Замітки 📝")
kb8 = KeyboardButton("Написати ✉️")

kb_teachers = (
    ReplyKeyboardMarkup(resize_keyboard=True)
    .row(kb1, kb2)
    .row(kb6, kb3)
    .row(kb7, kb8)
    .row(kb5, kb4)
)
# ======================================================================
