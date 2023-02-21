from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data_base.controller_db import *



#KeyboardButton - створює одну кнопку
#ReplyKeyboardMarkup - створює клавіатуру
#ReplyKeyboardRemove - видаляє клавіатуру 



#===========================1 Keyboards================================
def get_t_kb():
    h = kb_teachers_reg.get()
    kb_name = ReplyKeyboardMarkup(resize_keyboard=True) 
    # фор то цикл він достає з бази даних по одному вчителю і пхаж в клаву ПО ОДНОМУ
    try:
        for i in range(0,len(h),2):
            kb_name.add(h[i]).insert(h[i+1])
    except IndexError:
        pass
    return kb_name.add(KeyboardButton("Назад"))
#======================================================================



#===========================2 Keyboards================================
kb1 = KeyboardButton("Розклад занять 🥱")
kb2 = KeyboardButton("Розклад дзвінків ⌚️")
kb3 = KeyboardButton("Ч/З 🤨")
kb4 = KeyboardButton("Переєструватись 🤨")
kb5 = KeyboardButton("Меню 👥")

kb_teachers = ReplyKeyboardMarkup(resize_keyboard=True).row(kb1, kb2).row(kb5, kb3).add(kb4)
#======================================================================
