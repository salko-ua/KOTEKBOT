from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# ===========================all func Keyboards============================
text = KeyboardButton("Клавіатури ⌨️")
admin = KeyboardButton("Адмін 🔑")
menu = KeyboardButton("Меню 👥")
text1 = KeyboardButton("Перегляд бази данних 👀")
button1 = KeyboardButton("таблиця студентів")
button2 = KeyboardButton("таблиця за групою")
button3 = KeyboardButton("таблиця адмінів")
button4 = KeyboardButton("таблиця викладачів")
text2 = KeyboardButton("Користувачі 👥")
button5 = KeyboardButton("Студент за ID")
button6 = KeyboardButton("Видалити студента")
button7 = KeyboardButton("Викладач за ID")
button8 = KeyboardButton("Видалити викладача")

sadmin = (
    ReplyKeyboardMarkup(resize_keyboard=True)
    .add(text)
    .row(admin, menu)
    .add(text1)
    .row(button1, button4)
    .row(button2, button3)
    .add(text2)
    .row(button5, button7)
    .row(button6, button8)
)
