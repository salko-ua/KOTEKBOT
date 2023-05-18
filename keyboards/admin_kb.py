from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# KeyboardButton - створює одну кнопку
# ReplyKeyboardMarkup - створює клавіатуру
# ReplyKeyboardRemove - видаляє клавіатуру
# ReplyKeyboardMarkup створення клавіатури + адаптування resize_keyboard=True
# one_time_keyboard = True


back = KeyboardButton("Назад")


# ===========================1 Keyboards==============================

photo_news = KeyboardButton("Викласти 🖼")
message_news = KeyboardButton("Викласти 📝")
mixed_news = KeyboardButton("Викласти 🖼📝")
menu = KeyboardButton("Меню 👥")


kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)

kb_admin.row(photo_news, message_news).row(mixed_news, menu)
# ======================================================================


# ===========================2 Keyboards================================
butt1 = KeyboardButton("Одна")
butt2 = KeyboardButton("Всі")

kb_all_or_one = ReplyKeyboardMarkup(resize_keyboard=True).row(butt1, butt2).add(back)
# ======================================================================


# ===========================3 Keyboards================================
dont = KeyboardButton("не треба")

kb_dont = ReplyKeyboardMarkup(resize_keyboard=True).add(dont).add(back)
# ======================================================================


# ===========================4 Keyboards===============================
yes = KeyboardButton("Так")

kb_ys = ReplyKeyboardMarkup(resize_keyboard=True).add(yes).add(back)
# ======================================================================
