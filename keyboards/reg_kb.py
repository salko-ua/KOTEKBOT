from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


# KeyboardButton - створює одну кнопку
# ReplyKeyboardMarkup - створює клавіатуру
# ReplyKeyboardRemove - видаляє клавіатуру
# ReplyKeyboardMarkup створення клавіатури + адаптування resize_keyboard=True
# one_time_keyboard = True


# ===========================1 Keyboards============================
student = KeyboardButton("Студент 👩‍🎓")
teacher = KeyboardButton("Викладач 👨‍🏫")
admin = KeyboardButton("Адміністратор 🔐")
back = KeyboardButton("Назад")

kb_choice = (
    ReplyKeyboardMarkup(resize_keyboard=True).row(student, teacher).add(admin).add(back)
)
# ===========================2 Keyboards============================
