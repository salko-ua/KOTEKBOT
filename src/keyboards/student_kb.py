from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from src.data_base import Database


# 👨‍🎓 student keyboard
def student_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    keyboard = ["Сховати ❌"]

    for button in keyboard:
        builder.add(InlineKeyboardButton(text=button, callback_data=button))

    return builder.adjust(2).as_markup(resize_keyboard=True)


# Клавіатура для списку груп студентів
async def student_group_list_kb() -> InlineKeyboardMarkup:
    db = await Database.setup()
    group_list = await db.student_group_list()
    builder = InlineKeyboardBuilder()

    for group in group_list:
        builder.add(InlineKeyboardButton(text=group, callback_data=group))

    builder.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="Назад"))

    return builder.adjust(4).as_markup()
