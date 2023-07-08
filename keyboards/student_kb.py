from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from data_base import Database


# ===========================1 Keyboards================================
async def reg_student_kb() -> ReplyKeyboardMarkup:
    db = await Database.setup()
    list_group = await db.student_group_list_sql()
    builder = ReplyKeyboardBuilder()

    for group in list_group:
        builder.add(KeyboardButton(text=group))

    builder.add(KeyboardButton(text="Меню 👥"))

    return builder.adjust(4).as_markup(resize_keyboard=True)


# ======================================================================


# ===========================2 Keyboards================================
async def student_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    keyboard = [
        "Розклад пар 👀",
        "Розклад дзвінків ⌚️",
        "Тривоги ⚠️",
        "Ч/З тиждень ✏️",
        "Замітки 📝",
        "Написати ✉️",
        "Меню 👥",
        "Змінити групу 🚫",
    ]

    for button in keyboard:
        builder.add(KeyboardButton(text=button))

    return builder.adjust(2).as_markup(resize_keyboard=True)


# ======================================================================
