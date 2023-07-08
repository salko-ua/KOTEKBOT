from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# KeyboardButton - створює одну кнопку
# ReplyKeyboardMarkup - створює клавіатуру
# ReplyKeyboardRemove - видаляє клавіатуру
# ReplyKeyboardMarkup створення клавіатури + адаптування resize_keyboard=True
# one_time_keyboard = True


# ===========================1 Keyboards==============================
async def admin_kb() -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()

    keyboard = [
        "Викласти 🖼",
        "Викласти 📝",
        "Викласти 🖼📝",
        "Меню 👥",
    ]

    for button in keyboard:
        builder.add(KeyboardButton(text=button))

    return builder.adjust(2).as_markup(resize_keyboard=True)


# ======================================================================


# ===========================2 Keyboards==============================
async def back_kb() -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text="Назад"))

    return builder.adjust(2).as_markup(resize_keyboard=True)


# ======================================================================
