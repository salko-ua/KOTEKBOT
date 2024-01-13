from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Реєстрація 📝
async def reg_choice_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    keyboard = [
        "Студент 👩‍🎓",
        "Викладач 👨‍🏫",
        "Адміністратор 🔐",
        "Сховати ❌",
    ]

    for button in keyboard:
        builder.add(InlineKeyboardButton(text=button, callback_data=button))

    return builder.adjust(2).as_markup(resize_keyboard=True)
