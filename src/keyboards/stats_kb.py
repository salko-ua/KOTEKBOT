from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class StatsKeyboards:
    # ♻️ update
    async def update_kb() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        builder.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="other_inline"))
        builder.add(
            InlineKeyboardButton(
                text="Оновити ♻️",
                callback_data="Статистика 🧮",
            )
        )

        return builder.as_markup()
