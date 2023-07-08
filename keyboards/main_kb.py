from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


# ===========================1 Keyboards============================
async def start_all_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    keyboard = [
        "Реєстрація 📝",
        "Налаштування ⚙️",
        "Інше 📌",
        "Для абітурієнта 🧑‍💻",
    ]

    for button in keyboard:
        builder.add(KeyboardButton(text=button))

    return builder.adjust(2).as_markup(resize_keyboard=True)


# ===========================2 Keyboards============================
async def start_user_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    keyboard = [
        "Розклад 📅",
        "Налаштування ⚙️",
        "Інше 📌",
        "Для абітурієнта 🧑‍💻",
    ]

    for button in keyboard:
        builder.add(KeyboardButton(text=button))

    return builder.adjust(2).as_markup(resize_keyboard=True)


# ===========================3 Keyboards============================
async def start_admin_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    keyboard = [
        "Розклад 📅",
        "Адмін 🔑",
        "Інше 📌",
        "Для абітурієнта 🧑‍💻",
    ]

    for button in keyboard:
        builder.add(KeyboardButton(text=button))

    return builder.adjust(2).as_markup(resize_keyboard=True)


# ===========================4 Keyboards============================
async def other_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    keyboard = [
        "Про бота 🖇",
        "Про мене 👀",
        "Розробка 🧩",
        "Статистика 🧮",
        "Допомога 🛠",
        "Час роботи 📅",
        "Фото кота 🖼",
        "Стікери 👨‍👩‍👧‍👦",
        "Меню 👥",
        "Донат 🫡",
    ]

    for button in keyboard:
        builder.add(KeyboardButton(text=button))

    return builder.adjust(2).as_markup(resize_keyboard=True)


# ===========================5 Keyboards============================
async def for_applicant_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    keyboard = [
        "Вступ 📗",
        "Про коледж 🛡",
        "Адреса 📫",
        "Контакти 📘",
        "Реквізити 💳",
        "Офіційний сайт 🌎",
        "Меню 👥",
        "Спеціальності 📜",
    ]

    for button in keyboard:
        builder.add(KeyboardButton(text=button))

    return builder.adjust(2).as_markup(resize_keyboard=True)
