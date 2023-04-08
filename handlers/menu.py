# from import
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import *
from data_base.controller_db import *
from handlers.stats import stats_schedule_add
from aiogram.dispatcher.filters import ChatTypeFilter, Text


# =========Класс машини стану=========
class FSMSpecialty(StatesGroup):
    specialty = State()


# ===========================Меню 👥============================
async def menu(message: types.Message):
    if await admin_exists_sql(message.from_user.id):
        await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start_admin)
    elif await user_exists_sql(message.from_user.id):
        await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start_user)
    elif await teachers_exists_sql(message.from_user.id):
        await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start_user)
    else:
        await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start)


#                          Елемнти Меню


# ===========================Вступ 📗============================
async def introduction(message: types.Message):
    await stats_schedule_add("Вступ 📗", 1)
    await message.answer(
        "Інформація про <a href='https://telegra.ph/%D0%86nformac%D1%96ya-dlya-vstupnika-2023-02-21'>вступ</a> на 2023 рік\nвсе скопійовано з офіційного\nсайту.У 2023 році - актуально",
        parse_mode="HTML",
    )


# ===========================Про коледж 🛡============================
async def about_collasge(message: types.Message):
    await stats_schedule_add("Про коледж 🛡", 1)
    await message.answer(
        "<a href='https://telegra.ph/Pro-koledzh-02-21'>Про коледж</a>",
        parse_mode="HTML",
    )


# ===========================Час роботи 📅============================
async def time_work(message: types.Message):
    await stats_schedule_add("Час роботи 📅", 1)
    await message.answer(
        """Час роботи ⌚️
Понеділок - П'ятниця: 8:00–17:00.
Субота - Неділя: Зачинено."""
    )


# ===========================Адреса 📫============================
async def addres(message: types.Message):
    await stats_schedule_add("Адреса 📫", 1)
    await message.answer(
        """•Земля 🌍
•Україна 🇺🇦
•Волинська область 🌉
•Володимир 🌆
•Вул. Устилузька 42 🛣"""
    )


# ===========================Спеціальності 📜============================
async def specialty(message: types.Message):
    await stats_schedule_add("Спеціальності 📜", 1)
    if message.chat.type == "private":
        await message.answer("Cпеціальності 📜 ВВПФК", reply_markup=kb_speciality)
        await FSMSpecialty.specialty.set()
    else:
        await message.answer("Цю команду можна викоритовувати тільки в лс бот")


async def specialty1(m: types.Message, state=FSMContext):
    if m.chat.type == "private":
        if m.text == "🔙 Назад":
            if await admin_exists_sql(m.from_user.id):
                await m.answer("⬇️Головне меню⬇️", reply_markup=kb_for_applicant)
            elif await user_exists_sql(m.from_user.id):
                await m.answer("⬇️Головне меню⬇️", reply_markup=kb_for_applicant)
            elif await teachers_exists_sql(m.from_user.id):
                await m.answer("⬇️Головне меню⬇️", reply_markup=kb_for_applicant)
            else:
                await m.answer("⬇️Головне меню⬇️", reply_markup=kb_for_applicant)
            await state.finish()
        else:
            if m.text == "Діловодство":
                await m.answer(
                    """Спеціальність 029 Інформаційна, бібліотечна та архівна справа \n(<a href='https://telegra.ph/Spec%D1%96aln%D1%96st-029-%D0%86nformac%D1%96jna-b%D1%96bl%D1%96otechna-ta-arh%D1%96vna-sprava-D%D1%96lovodstvo-02-20-2'> Діловодство </a>)""",
                    parse_mode="HTML",
                )
            elif m.text == "Дошкільна освіта":
                await m.answer(
                    """Спеціальність 012 \n(<a href='https://telegra.ph/SHvidkij-pereglyad-02-20'> Дошкільна освіта </a>)""",
                    parse_mode="HTML",
                )
            elif m.text == "Початкова освіта":
                await m.answer(
                    """Спеціальність 013 \n(<a href='https://telegra.ph/CHas-roboti-02-20'> Початкова освіта </a>)""",
                    parse_mode="HTML",
                )
            elif m.text == "Трудове навчання":
                await m.answer(
                    """Спеціальність 014 Середня освіта \n(<a href='https://telegra.ph/Spec%D1%96aln%D1%96st-014-Serednya-osv%D1%96ta-Trudove-navchannya-ta-tehnolog%D1%96i-02-21'> Трудове навчання та технології </a>)""",
                    parse_mode="HTML",
                )
            elif m.text == "Образотворче 🎨":
                await m.answer(
                    """Спеціальність 014.12 Середня освіта \n(<a href='https://telegra.ph/Spec%D1%96aln%D1%96st-01412-Serednya-osv%D1%96ta-Obrazotvorche-mistectvo-02-21'> Образотворче мистецтво </a>)""",
                    parse_mode="HTML",
                )
            elif m.text == "Цифрові технології":
                await m.answer(
                    """Спеціальність 015.39 Професійна освіта \n(<a href='https://telegra.ph/Spec%D1%96aln%D1%96st-029-%D0%86nformac%D1%96jna-b%D1%96bl%D1%96otechna-ta-arh%D1%96vna-sprava-D%D1%96lovodstvo-02-20'> Цифрові технології </a>)""",
                    parse_mode="HTML",
                )
    else:
        await m.answer("Цю команду можна викоритовувати тільки в лс бота")
        await state.finish()


# ===========================Інше 📌============================
async def others(message: types.Message):
    await stats_schedule_add("Інше 📌", 1)
    await message.answer("Інше 🫤", reply_markup=kb_infs)


# ===========================Стікери 👨‍👩‍👧‍👦============================
async def stick(message: types.Message):
    await stats_schedule_add("Стікери 👨‍👩‍👧‍👦", 1)
    await message.answer_sticker(
        r"CAACAgIAAxkBAAEH15Nj9O7fae-x_g7MdX6tus4wAh8SngACLQAD3jyHIuJ7Rhz4aJKDLgQ"
    )


# ===========================Про бота 🖇============================
async def about_bot(message: types.Message):
    await stats_schedule_add("Про бота 🖇", 1)
    await message.answer(
        """БОТ ВПК ПЕДКІТ
Версія : release 1.7
Розробник: <a href='https://t.me/salkooua'>Мусаєв Джаміль</a>
Зробив аватарку: <a href='https://t.me/yurchh'>Коновалець Юра</a>

Бот створено для спрощення
виконання будь - яких речей
зв'язаних з коледжем
У ньому є купа потрібних
і не дуже функцій, які
розставленні в зручних місцях

<a href='https://vvpc.com.ua/'>Офіційний сайт ВПФК</a>
""",
        parse_mode="HTML",
        disable_web_page_preview=True,
    )


# ===========================Інформація для абітурієнта============================
async def for_applicant(message: types.Message):
    await stats_schedule_add("Для абітурієнта 🧑‍💻", 1)
    await message.answer("Інформація для абітурієнта", reply_markup=kb_for_applicant)


text = {
    "menu": ["Меню 👥", "Меню", "Menu"],
    "about_bot": ["Про бота 🖇", "Про бота", "about bot"],
    "about_collasge": ["Про коледж 🛡", "Про коледж", "about collasge"],
    "introduction": ["Вступ 📗", "Вступ", "introduction"],
    "time_work": ["Час роботи 📅", "Час роботи", "time work"],
    "addres": ["Адреса 📫", "Адреса", "addres"],
    "others": ["Інше 📌", "Інше ", "others", "other"],
    "stick": ["Стікери 👨‍👩‍👧‍👦", "Стікери", "Stickers"],
}


def register_handler_menu(dp: Dispatcher):
    dp.register_message_handler(
        menu, Text(ignore_case=True, equals=text["menu"]), ChatTypeFilter("private")
    )

    dp.register_message_handler(
        about_bot, Text(ignore_case=True, equals=text["about_bot"])
    )

    dp.register_message_handler(
        about_collasge, Text(ignore_case=True, equals=text["about_collasge"])
    )

    dp.register_message_handler(
        introduction, Text(ignore_case=True, equals=text["introduction"])
    )

    dp.register_message_handler(
        time_work, Text(ignore_case=True, equals=text["time_work"])
    )

    dp.register_message_handler(addres, Text(ignore_case=True, equals=text["addres"]))

    dp.register_message_handler(others, Text(ignore_case=True, equals=text["others"]))

    dp.register_message_handler(stick, Text(ignore_case=True, equals=text["stick"]))

    dp.register_message_handler(
        for_applicant, ChatTypeFilter("private"), text="Для абітурієнта 🧑‍💻"
    )

    dp.register_message_handler(
        specialty, ChatTypeFilter("private"), text="Спеціальності 📜", state=None
    )

    dp.register_message_handler(
        specialty1, ChatTypeFilter("private"), state=FSMSpecialty.specialty
    )
