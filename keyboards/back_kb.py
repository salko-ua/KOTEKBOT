from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# ⬅️ Back admin
async def admin_back_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="Назад"))

    return builder.adjust(2).as_markup(resize_keyboard=True)

# ⬅️ Back prime
async def prime_back_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="інша"))

    return builder.adjust(2).as_markup(resize_keyboard=True)

# ⬅️ Back dev
async def dev_back_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="back_dev"))

    return builder.as_markup()

# ⬅️ Back other
async def other_back_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="other_inline"))
    builder.add(InlineKeyboardButton(text="Сховати ❌", callback_data="Сховати ❌"))

    return builder.adjust(2).as_markup()

# ⬅️ Back applicant
async def applicant_back_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="applicant_inline"))
    builder.add(InlineKeyboardButton(text="Сховати ❌", callback_data="Сховати ❌"))

    return builder.adjust(2).as_markup()

# ⬅️ Back user
async def user_back_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="user_inline"))
    builder.add(InlineKeyboardButton(text="Сховати ❌", callback_data="Сховати ❌"))

    return builder.adjust(2).as_markup()

# ⬅️ Back reg
async def reg_back_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="reg_inline"))
    builder.add(InlineKeyboardButton(text="Сховати ❌", callback_data="Сховати ❌"))

    return builder.adjust(2).as_markup()

# ❌ General hide
async def hide_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text="Сховати ❌", callback_data="Сховати ❌"))

    return builder.as_markup()