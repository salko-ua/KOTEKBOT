from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from src.data_base import Database # type: ignore


# super admin
def super_admin_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    keyboard = ["Розклад 📝", "Групи 👥", "Інше 📕", "Сховати ❌"]

    for button in keyboard:
        builder.add(InlineKeyboardButton(text=button, callback_data=button))

    return builder.adjust(2).as_markup(resize_keyboard=True)


def super_admin_schedule() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    keyboard = [
        "Додати/Змінити 🗓",
        "Додати/Змінити 🔔",
        "Видалити 🗓",
        "Видалити 🔔",
        "⬅️ Назад",
        "Сховати ❌",
    ]

    for button in keyboard:
        builder.add(InlineKeyboardButton(text=button, callback_data=button))

    return builder.adjust(2).as_markup(resize_keyboard=True)


def super_admin_group() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    keyboard = ["Додати 👥", "Видалити 👥", "⬅️ Назад", "Сховати ❌"]

    for button in keyboard:
        builder.add(InlineKeyboardButton(text=button, callback_data=button))

    return builder.adjust(2).as_markup(resize_keyboard=True)


def super_admin_other() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    keyboard = ["Додати фото 🖼","⬅️ Назад","Сховати ❌ "]

    for button in keyboard:
        builder.add(InlineKeyboardButton(text=button, callback_data=button))

    return builder.adjust(1,2).as_markup(resize_keyboard=True)


# список груп - студенти
async def group_selection_student_kb() -> InlineKeyboardMarkup:
    db = await Database.setup()
    list_group = await db.student_group_list()
    builder = InlineKeyboardBuilder()
    print(list_group)
    for group in list_group:
        builder.add(InlineKeyboardButton(text=group, callback_data=f"delete_group:{group}"))

    builder.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="back_super_admin"))

    return builder.adjust(4).as_markup(resize_keyboard=True)





def super_admin_back_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    keyboard = ["⬅️ Назад", "Сховати ❌"]

    for button in keyboard:
        builder.add(InlineKeyboardButton(text=button, callback_data=button))

    return builder.adjust(2).as_markup(resize_keyboard=True)