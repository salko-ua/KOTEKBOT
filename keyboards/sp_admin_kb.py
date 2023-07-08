from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from data_base import Database


# ===========================all func Keyboards============================
async def super_admin_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    keyboard = [
        "Адмін 🔑",
        "Меню 👥",
        "-------",
        "-------",
        "Видалити студента",
        "Видалити викладача",
        "-------",
        "-------",
        "викладача ❇️",
        "викладача 🗑",
        "групу ❇️",
        "групу 🗑",
        "-------",
        "-------",
        "групу 🗑🖼",
        "групі ❇️",
        "викладачу ❇️",
        "дзвінків ❇️",
        "дзвінків 🗑",
    ]

    for button in keyboard:
        builder.add(KeyboardButton(text=button))

    return builder.adjust(2).as_markup(resize_keyboard=True)


# ========================================================================


# ===========================1 Keyboards================================
async def group_selection_student_kb() -> ReplyKeyboardMarkup:
    db = await Database.setup()
    list_group = await db.student_group_list_sql()
    builder = ReplyKeyboardBuilder()

    for group in list_group:
        builder.add(KeyboardButton(text=group))

    builder.add(KeyboardButton(text="Назад"))

    return builder.adjust(4).as_markup(resize_keyboard=True)


# ======================================================================


# ===========================1 Keyboards================================
async def group_selection_teacher_kb() -> ReplyKeyboardMarkup:
    db = await Database.setup()
    list_teachers = await db.teacher_group_list_sql()
    builder = ReplyKeyboardBuilder()

    for teacher in list_teachers:
        builder.add(KeyboardButton(text=teacher))

    builder.add(KeyboardButton(text="Назад"))

    return builder.adjust(2).as_markup(resize_keyboard=True)


# ======================================================================
