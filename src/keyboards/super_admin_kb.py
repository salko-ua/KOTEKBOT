from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.data_base import Database


# super admin
def super_admin_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    keyboard = [
        "Пароль 🔐",
        "База даних 🖥",
        "Змінити 🔔",
        "Оновити 📅",
        "Групи 👥",
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


def super_admin_back_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    keyboard = ["⬅️ Назад", "Сховати ❌"]

    for button in keyboard:
        builder.add(InlineKeyboardButton(text=button, callback_data=button))

    return builder.adjust(2).as_markup(resize_keyboard=True)


# список груп - студенти
async def group_selection_student_kb() -> InlineKeyboardMarkup:
    db = await Database.setup()
    list_group = await db.student_group_list()
    builder = InlineKeyboardBuilder()
    for group in list_group:
        builder.add(InlineKeyboardButton(text=group, callback_data=group))

    builder.add(
        InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data="⬅️ Назад",
        )
    )

    return builder.adjust(4).as_markup(resize_keyboard=True)
