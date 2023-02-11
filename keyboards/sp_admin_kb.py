from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


#===========================all func Keyboards============================
button1 = KeyboardButton("======ADMIN======")
button2 = KeyboardButton("/admin")
button3 = KeyboardButton("/sadmin")
button4 = KeyboardButton("/user")
button5 = KeyboardButton("/showuser")
button6 = KeyboardButton("/showgroupa")
button7 = KeyboardButton("/showadmin")

sadmin = ReplyKeyboardMarkup(resize_keyboard=True).add(button1).add(button2).add(button3).add(button4).add(button5).add(button6).add(button7)


#===========================user SA Keyboards============================
kb2 = KeyboardButton("Переглянути розклад дзвінків")

sadmin_cl = ReplyKeyboardMarkup(resize_keyboard=True).add(kb2)


#===========================admin SA Keyboards============================
but_add_group = KeyboardButton("Додати групу")
but_delete_group = KeyboardButton("Видалити групу")
but_couples = KeyboardButton("Додати розклад до групи")   
but_add_calls = KeyboardButton("Додати розклад дзвінків")
but_delete_calls = KeyboardButton("Видалити розклад дзвінків")
but_post_news = KeyboardButton("Викласти новину")
but_list_group = KeyboardButton("Список груп") 


sadmin_ad = ReplyKeyboardMarkup(resize_keyboard=True) 

sadmin_ad.add(but_add_group).insert(but_delete_group)\
.add(but_couples).add(but_add_calls).add(but_delete_calls).add(but_post_news).insert(but_list_group)