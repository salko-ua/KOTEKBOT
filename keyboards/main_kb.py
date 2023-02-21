from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove



#KeyboardButton - створює одну кнопку
#ReplyKeyboardMarkup - створює клавіатуру
#ReplyKeyboardRemove - видаляє клавіатуру 
#ReplyKeyboardMarkup створення клавіатури + адаптування resize_keyboard=True
#one_time_keyboard = True


#===========================1 Keyboards============================
introduction = KeyboardButton("Вступ 📗")
specialty = KeyboardButton("Спеціальності 📜")
reg = KeyboardButton("Реєстрація ⚙️")
about_collage = KeyboardButton("Про коледж 🛡")
stikers = KeyboardButton("Стікери 👨‍👩‍👧‍👦")
others = KeyboardButton("Інше 📌")


kb_start = ReplyKeyboardMarkup(resize_keyboard=True)
kb_start.row(introduction, about_collage).row(reg, stikers).row(others,specialty)
#===========================2 Keyboards============================
introduction = KeyboardButton("Вступ 📗")
specialty = KeyboardButton("Спеціальності 📜")
reg = KeyboardButton("Розклад ⚙️")
about_collage = KeyboardButton("Про коледж 🛡")
stikers = KeyboardButton("Стікери 👨‍👩‍👧‍👦")
others = KeyboardButton("Інше 📌")

kb_start_user = ReplyKeyboardMarkup(resize_keyboard=True)
kb_start_user.row(introduction, about_collage).row(reg, stikers).row(others,specialty)
#===========================3 Keyboards============================
#ADMIN 1 reg
introduction = KeyboardButton("Вступ 📗")
specialty = KeyboardButton("Спеціальності 📜")
admin = KeyboardButton("Адмін 🔑")
reg = KeyboardButton("Розклад ⚙️")
about_collage = KeyboardButton("Про коледж 🛡")
stikers = KeyboardButton("Стікери 👨‍👩‍👧‍👦")
others = KeyboardButton("Інше 📌")

kb_start_admin = ReplyKeyboardMarkup(resize_keyboard=True)
kb_start_admin.row(introduction, about_collage).row(reg, admin).row(others,specialty).add(stikers)
#===========================4 Keyboards============================
about_author =KeyboardButton("Про бота 🖇")
time_work = KeyboardButton("Час роботи 📅")
addres = KeyboardButton("Адреса 📫")
fraction = KeyboardButton("Ч/З 🤨")
menu = KeyboardButton("Меню 👥")
kb_infs = ReplyKeyboardMarkup(resize_keyboard=True)
kb_infs.row(about_author, fraction).row(addres, time_work).add(menu)
#===========================5 Keyboards============================
spec012 = KeyboardButton('Дошкільна освіта')
spec013 = KeyboardButton('Початкова освіта')
spec014 = KeyboardButton('Трудове навчання')
spec014_12 = KeyboardButton('Образотворче 🎨')
spec015_39 = KeyboardButton('Цифрові технології')
spec029 = KeyboardButton('Діловодство')
menu = KeyboardButton("Меню 👥")

kb_speciality = ReplyKeyboardMarkup(resize_keyboard=True)
kb_speciality.add(spec012).insert(spec013).add(spec014).insert(spec015_39).row(spec014_12, spec029).add(menu)