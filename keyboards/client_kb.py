from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data_base.controller_db import *



#KeyboardButton - створює одну кнопку
#ReplyKeyboardMarkup - створює клавіатуру
#ReplyKeyboardRemove - видаляє клавіатуру 



#===========================1 Keyboards================================
def get_kb():
    h = kb_user_reg.get()
    kb_course = ReplyKeyboardMarkup(resize_keyboard=True) 
    for i in range(0,len(h)):
        kb_course.insert(h[i])
    return kb_course.add(KeyboardButton("Назад"))
#======================================================================



#===========================2 Keyboards================================
kb1 = KeyboardButton("Переглянути розклад пар")
kb2 = KeyboardButton("Переглянути розклад дзвінків")
last = KeyboardButton("Змінити групу")

kb_client = ReplyKeyboardMarkup(resize_keyboard=True).add(kb1).add(kb2).add(last)
#======================================================================


    

