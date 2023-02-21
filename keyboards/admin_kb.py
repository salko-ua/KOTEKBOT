from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


#KeyboardButton - створює одну кнопку
#ReplyKeyboardMarkup - створює клавіатуру
#ReplyKeyboardRemove - видаляє клавіатуру 
#ReplyKeyboardMarkup створення клавіатури + адаптування resize_keyboard=True
#one_time_keyboard = True


back =KeyboardButton('Назад')


#===========================1 Keyboards==============================
but_add_teachers = KeyboardButton("викладача ❇️")
but_delete_teachers = KeyboardButton("викладача 🗑")
but_add_group = KeyboardButton("групу ❇️")
but_delete_group = KeyboardButton("групу 🗑")
neactive = KeyboardButton("Розклад")
but_couples_t = KeyboardButton("групі ❇️")   
but_couples = KeyboardButton("викладачу ❇️")   
but_add_calls = KeyboardButton("дзвінків ❇️")
but_delete_calls = KeyboardButton("дзвінків 🗑")
but_post_news = KeyboardButton("Викласти новину")
but_list_group = KeyboardButton("Список груп") 
menu = KeyboardButton("Меню 👥")


kb_admin = ReplyKeyboardMarkup(resize_keyboard=True) 

kb_admin.add(but_post_news).insert(menu).add(but_add_teachers).insert(but_delete_teachers)\
        .add(but_add_group).insert(but_delete_group)\
        .add(neactive).add(but_couples_t).insert(but_couples).add(but_add_calls).insert(but_delete_calls)\
        .add(but_list_group)
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





