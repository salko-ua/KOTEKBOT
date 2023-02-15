from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


#===========================all func Keyboards============================
text = KeyboardButton("- Клавіатури : ")
button2 = KeyboardButton("адмін")
button3 = KeyboardButton("власник")
button4 = KeyboardButton("студент")
text1 = KeyboardButton("- Перегляд бази данних")
button5 = KeyboardButton("Показати таблицю студентів")
button6 = KeyboardButton("Показати таблицю групи")
button7 = KeyboardButton("Показати таблицю адмінів")

sadmin = ReplyKeyboardMarkup(resize_keyboard=True).add(text).row(button2, button3, button4).add(text1).add(button5).add(button6).add(button7)


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