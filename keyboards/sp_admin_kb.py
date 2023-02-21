from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


#===========================all func Keyboards============================
text = KeyboardButton("Клавіатури ⌨️")
button2 = KeyboardButton("Адмін 🔑")
menu = KeyboardButton ("Меню 👥")
text1 = KeyboardButton("Перегляд бази данних 👀")
button5 = KeyboardButton("таблиця студентів")
button6 = KeyboardButton("таблиця за групою")
button7 = KeyboardButton("таблиця групи")
button8 = KeyboardButton("таблиця адмінів")

sadmin = ReplyKeyboardMarkup(resize_keyboard=True).add(text).row(button2, menu).add(text1).row(button5, button8).row(button6, button7)

