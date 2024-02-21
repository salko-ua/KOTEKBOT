from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from src.data_base import Database


# super admin
def super_admin_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    keyboard = [
        "Розклад 📝",
        "Групи 👥",
    ]

    for button in keyboard:
        builder.add(InlineKeyboardButton(text=button, callback_data=button))

    return builder.adjust().as_markup(resize_keyboard=True)


def super_admin_schedule() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    keyboard = [
        "Додати/Змінити 🗓",
        "Додати/Змінити 🔔",
        "Видалити 🗓",
        "Видалити 🔔",
        "⬅️ Назад",
    ]

    for button in keyboard:
        builder.add(InlineKeyboardButton(text=button, callback_data=button))

    return builder.adjust(2).as_markup(resize_keyboard=True)


def super_admin_group() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    keyboard = [
        "Додати 👥",
        "Видалити 👥",
        "⬅️ Назад",
    ]

    for button in keyboard:
        builder.add(InlineKeyboardButton(text=button, callback_data=button))

    return builder.adjust(2).as_markup(resize_keyboard=True)


# список груп - студенти
async def group_selection_student_kb() -> ReplyKeyboardMarkup:
    db = await Database.setup()
    list_group = await db.student_group_list()
    builder = ReplyKeyboardBuilder()

    for group in list_group:
        builder.add(KeyboardButton(text=group))

    builder.add(KeyboardButton(text="Назад"))

    return builder.adjust(4).as_markup(resize_keyboard=True)
