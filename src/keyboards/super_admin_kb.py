from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.data_base import Database


# super admin
async def super_admin_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    keyboard = [
        "Адмін 🔑",
        "Меню 👥",
        "Видалення користувачів",
        "Видалити студента",
        "Видалити викладача",
        "Налаштування груп",
        "викладача ❇️",
        "викладача 🗑",
        "групу ❇️",
        "групу 🗑",
        "Налаштування розкладу",
        "групу 🗑🖼",
        "групі ❇️",
        "викладачу ❇️",
        "дзвінків ❇️",
        "дзвінків 🗑",
    ]

    for button in keyboard:
        builder.add(KeyboardButton(text=button))

    return builder.adjust(2, 1, 2, 1, 2, 2, 1, 2, 2, 1).as_markup(resize_keyboard=True)


# список груп - студенти
async def group_selection_student_kb() -> ReplyKeyboardMarkup:
    db = await Database.setup()
    list_group = await db.student_group_list()
    builder = ReplyKeyboardBuilder()

    for group in list_group:
        builder.add(KeyboardButton(text=group))

    builder.add(KeyboardButton(text="Назад"))

    return builder.adjust(4).as_markup(resize_keyboard=True)
