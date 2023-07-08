from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


# ======================================================================
async def dev_inline_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text="Запит на участь 📝", callback_data="request"))
    builder.add(
        InlineKeyboardButton(text="Надіслати відгук ☺️", callback_data="response")
    )
    builder.add(
        InlineKeyboardButton(text="Повідомити про помилку 🤔", callback_data="error")
    )

    return builder.adjust(1).as_markup()


# ======================================================================


# ======================================================================
async def back_inline_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="back_dev"))

    return builder.as_markup()


# ======================================================================


# ======================================================================
async def choise_inline_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="back_dev"))
    builder.add(InlineKeyboardButton(text="Підтвердити 🫡", callback_data="okay"))

    return builder.adjust(1).as_markup()


# ======================================================================
