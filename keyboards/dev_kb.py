from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


# 🧩 dev
async def dev_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text="Запит на участь 📝", callback_data="request"))
    builder.add(
        InlineKeyboardButton(text="Надіслати відгук ☺️", callback_data="response")
    )
    builder.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="other_inline"))
    builder.add(InlineKeyboardButton(text="Помилки? 🤔", callback_data="error"))

    return builder.adjust(2).as_markup()


# 🧩 choise
async def dev_choise_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="back_dev"))
    builder.add(InlineKeyboardButton(text="Підтвердити 🫡", callback_data="okay"))

    return builder.adjust(1).as_markup()
