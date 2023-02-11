from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove



#KeyboardButton - створює одну кнопку
#ReplyKeyboardMarkup - створює клавіатуру
#ReplyKeyboardRemove - видаляє клавіатуру 
#ReplyKeyboardMarkup створення клавіатури + адаптування resize_keyboard=True
#one_time_keyboard = True


#===========================1 Keyboards============================
button1 = KeyboardButton("Студент")
button2 = KeyboardButton("Назад")

kb_choice = ReplyKeyboardMarkup(resize_keyboard=True) .add(button1).add(button2)
#===========================2 Keyboards============================






