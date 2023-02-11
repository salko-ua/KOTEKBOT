from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram import types


#KeyboardButton - створює одну кнопку
#ReplyKeyboardMarkup - створює клавіатуру
#ReplyKeyboardRemove - видаляє клавіатуру 
#ReplyKeyboardMarkup створення клавіатури + адаптування resize_keyboard=True
#one_time_keyboard = True


back =KeyboardButton('Назад')


#===========================1 Keyboards==============================
but_add_group = KeyboardButton("Додати групу")
but_delete_group = KeyboardButton("Видалити групу")
but_couples = KeyboardButton("Додати розклад до групи")   
but_add_calls = KeyboardButton("Додати розклад дзвінків")
but_delete_calls = KeyboardButton("Видалити розклад дзвінків")
but_post_news = KeyboardButton("Викласти новину")
but_list_group = KeyboardButton("Список груп") 
last = KeyboardButton("Видалити акаунт")

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True) 

kb_admin.add(but_add_group).insert(but_delete_group)\
.add(but_couples).add(but_add_calls).add(but_delete_calls).add(but_post_news).insert(but_list_group).add(last)
#======================================================================



#===========================2 Keyboards================================
butt1 = KeyboardButton("Одна")
butt2 = KeyboardButton("Всі")

kb_all_or_one = ReplyKeyboardMarkup(resize_keyboard=True).row(butt1,butt2).add(back)
#======================================================================



#===========================3 Keyboards================================
dont = KeyboardButton("не треба")

kb_dont = ReplyKeyboardMarkup(resize_keyboard=True).add(dont).add(back)
#======================================================================



#===========================4 Keyboards===============================
yes = KeyboardButton("Так")

kb_ys = ReplyKeyboardMarkup(resize_keyboard=True).add(yes).add(back)
#======================================================================





