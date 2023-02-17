from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


#===========================all func Keyboards============================
text = KeyboardButton("- Клавіатури : ")
button2 = KeyboardButton("адмін")
button3 = KeyboardButton("власник")
button4 = KeyboardButton("студент")
text1 = KeyboardButton("- Перегляд бази данних")
button5 = KeyboardButton("Показати таблицю студентів")
button6 = KeyboardButton("Показати користувачів за групою")
button7 = KeyboardButton("Показати таблицю групи")
button8 = KeyboardButton("Показати таблицю адмінів")

sadmin = ReplyKeyboardMarkup(resize_keyboard=True).add(text).row(button2, button3, button4)\
                                                  .add(text1).add(button5).add(button6).add(button7).add(button8)

