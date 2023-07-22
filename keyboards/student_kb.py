from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data_base import Database

# 👨‍🎓 student keyboard
async def student_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    keyboard = [
        "Тривоги ⚠️",
        "Написати ✉️",
        "Сховати ❌",
        "Замітки 📝"
    ]

    for button in keyboard:
        builder.add(InlineKeyboardButton(text=button, callback_data=button))

    return builder.adjust(2).as_markup(resize_keyboard=True)

# 👨‍🎓 Список груп студентів
async def student_group_list_kb():
    db = await Database.setup()
    group_list = await db.student_group_list_sql()
    builder = InlineKeyboardBuilder()

    for group in group_list:
        builder.add(InlineKeyboardButton(text=group, callback_data=group))

    builder.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="Назад")).adjust(4)

    return builder.adjust(4).as_markup()


