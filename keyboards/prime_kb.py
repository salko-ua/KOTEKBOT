from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

# ======================================================================
async def text_inline_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(text="Змінити замітку ✏️", callback_data="edit_text")
    )
    builder.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="reg_inline"))
    builder.add(InlineKeyboardButton(text="Сховати ❌", callback_data="Сховати ❌"))

    return builder.adjust(1,2).as_markup()


async def cancle_inline_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text="Відмінити ❌", callback_data="cancel"))

    return builder.adjust(2).as_markup()


# ======================================================================