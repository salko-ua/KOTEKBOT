from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from data_base import Database


# ===========================1 Keyboards================================
async def reg_teacher_kb() -> ReplyKeyboardMarkup:
    db = await Database.setup()
    list_teachers = await db.teacher_group_list_sql()
    builder = ReplyKeyboardBuilder()

    for teacher in list_teachers:
        builder.add(KeyboardButton(text=teacher))

    builder.add(KeyboardButton(text="Меню 👥"))

    return builder.adjust(2).as_markup(resize_keyboard=True)


# ======================================================================


# ===========================2 Keyboards================================
async def teacher_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    keyboard = [
        "Розклад занять 👀",
        "Розклад дзвінків ⌚️",
        "Тривоги ⚠️",
        "Ч/З тиждень ✏️",
        "Замітки 📝",
        "Написати ✉️",
        "Меню 👥",
        "Вийти 🚫",
    ]

    for button in keyboard:
        builder.add(KeyboardButton(text=button))

    return builder.adjust(2).as_markup(resize_keyboard=True)


# ======================================================================
