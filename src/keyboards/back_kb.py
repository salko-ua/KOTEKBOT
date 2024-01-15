from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class BackKeyboards:
    # ⬅️ Back admin
    async def admin_back_kb() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        builder.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="Назад"))

        return builder.adjust(2).as_markup(resize_keyboard=True)

    # ⬅️ Back other
    async def other_back_kb() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        builder.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="other_inline"))
        builder.add(InlineKeyboardButton(text="Сховати ❌", callback_data="Сховати ❌"))

        return builder.adjust(2).as_markup()

    # ⬅️ Back applicant
    async def applicant_back_kb() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        builder.add(
            InlineKeyboardButton(text="⬅️ Назад", callback_data="applicant_inline")
        )
        builder.add(InlineKeyboardButton(text="Сховати ❌", callback_data="Сховати ❌"))

        return builder.adjust(2).as_markup()

    # ⬅️ Back user
    async def student_back_kb() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        builder.add(
            InlineKeyboardButton(text="⬅️ Назад", callback_data="student_back_kb")
        )
        builder.add(InlineKeyboardButton(text="Сховати ❌", callback_data="Сховати ❌"))

        return builder.adjust(2).as_markup()

    # ❌ General hide
    async def hide_kb() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        builder.add(InlineKeyboardButton(text="Сховати ❌", callback_data="Сховати ❌"))

        return builder.as_markup()
