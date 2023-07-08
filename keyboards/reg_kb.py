from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


# ===========================1 Keyboards============================
async def reg_choice_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    keyboard = [
        "Студент 👩‍🎓",
        "Викладач 👨‍🏫",
        "Адміністратор 🔐",
        "Меню 👥",
    ]

    for button in keyboard:
        builder.add(KeyboardButton(text=button))

    return builder.adjust(2).as_markup(resize_keyboard=True)


# ==================================================================
