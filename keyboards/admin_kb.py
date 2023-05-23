from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# KeyboardButton - створює одну кнопку
# ReplyKeyboardMarkup - створює клавіатуру
# ReplyKeyboardRemove - видаляє клавіатуру
# ReplyKeyboardMarkup створення клавіатури + адаптування resize_keyboard=True
# one_time_keyboard = True


# ===========================1 Keyboards==============================

photo_news = KeyboardButton("Викласти 🖼")
message_news = KeyboardButton("Викласти 📝")
mixed_news = KeyboardButton("Викласти 🖼📝")
menu = KeyboardButton("Меню 👥")


kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)

kb_admin.row(photo_news, message_news).row(mixed_news, menu)
# ======================================================================

# ===========================2 Keyboards==============================

back = KeyboardButton("Назад")

kb_back = ReplyKeyboardMarkup(resize_keyboard=True)

kb_back.add(back)
# ======================================================================
