# import
import asyncio


# from import
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import (
    MessageToDeleteNotFound,
    MessageCantBeDeleted,
    BadRequest,
)
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import *
from data_base.controller_db import *
from random import randint as rd
from handlers.stats import stats_schedule_add, see_all_stats


passwords = str(rd(10, 20)) + str(rd(10, 20)) + str(rd(10, 20)) + str(rd(10, 20))


# answer - повідомлення
# reply - повідомлення відповідь
# send_massage - повідомлення в лс


# =========Класс машини стану=========
class FSMReg(StatesGroup):
    course_groupe_reg = State()
    teachers_reg = State()
    password_reg = State()
    reply_reg = State()
    specialtys = State()


#                            СТАРТ
async def start(message: types.Message):
    if message.chat.type == "private":
        if await admin_exists_sql(message.from_user.id):
            await message.answer("Ви адмін", reply_markup=kb_start_admin)
        elif await user_exists_sql(message.from_user.id):
            await message.answer("⬇️ Клавіатура ⬇️", reply_markup=kb_start_user)
        elif await teachers_exists_sql(message.from_user.id):
            await message.answer("⬇️ Клавіатура ⬇️", reply_markup=kb_start_user)
        else:
            await message.answer("⬇️ Клавіатура ⬇️", reply_markup=kb_start)
    else:
        try:
            msg = await message.answer(
                "❗️Цю команду можна використовувати тільки в особистих повідомленнях\nПерейдіть до @pedbot_bot",
                reply_markup=ReplyKeyboardRemove(),
            )
            await asyncio.sleep(6)
            await message.delete()
            await msg.delete()
        except (MessageToDeleteNotFound, MessageCantBeDeleted, BadRequest):
            await message.answer(
                "Помилка, я не можу автовидалити своє повідомлення, мені потрібні права адміна"
            )


#                          Показ меню
async def menu(message: types.Message):
    if message.chat.type == "private":
        if await admin_exists_sql(message.from_user.id):
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start_admin)
        elif await user_exists_sql(message.from_user.id):
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start_user)
        elif await teachers_exists_sql(message.from_user.id):
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start_user)
        else:
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start)
    else:
        pass


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
        await FSMReg.specialtys.set()
    else:
        await message.answer("Цю команду можна викоритовувати тільки в лс бот")


async def specialty1(m: types.Message, state=FSMContext):
    if m.chat.type == "private":
        if m.text == "🔙 Назад":
            if await admin_exists_sql(m.from_user.id):
                await m.answer("⬇️Інше 📌⬇️", reply_markup=kb_for_applicant)
            elif await user_exists_sql(m.from_user.id):
                await m.answer("⬇️Інше 📌⬇️", reply_markup=kb_for_applicant)
            elif await teachers_exists_sql(m.from_user.id):
                await m.answer("⬇️Інше 📌⬇️", reply_markup=kb_for_applicant)
            else:
                await m.answer("⬇️Інше 📌⬇️", reply_markup=kb_for_applicant)
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


# ===========================Реєстрація ⚙️============================
async def registration(message: types.Message):
    if message.text == "Розклад ⚙️":
        await stats_schedule_add("Розклад ⚙️", 1)
    if (
        (not await user_exists_sql(message.from_user.id))
        and (not await admin_exists_sql(message.from_user.id))
        and (not await teachers_exists_sql(message.from_user.id))
    ):
        if message.chat.type == "private":
            await message.answer(
                "🤔 Реєстрація 🤔\nВиберіть тип акаунту ⬇️", reply_markup=kb_choice
            )
            await FSMReg.reply_reg.set()
        else:
            try:
                msg = await message.answer(
                    "🤨 Перейдіть в особисті повідомлення до @pedbot_bot\nі зареєструйтесь за командою /start"
                )
                await asyncio.sleep(2)
                await message.delete()
                await msg.delete()
            except (MessageToDeleteNotFound, MessageCantBeDeleted, BadRequest):
                await message.answer(
                    "Помилка, я не можу автовидалити своє повідомлення, мені потрібні права адміна"
                )
    elif await user_exists_sql(message.from_user.id):
        if message.chat.type == "private":
            await message.answer("Ваша клавіатура ⌨️", reply_markup=kb_client)
        else:
            try:
                msg = await message.answer("⚠️ Ви зареєстрованні")
                await asyncio.sleep(2)
                await message.delete()
                await msg.delete()
            except (MessageToDeleteNotFound, MessageCantBeDeleted, BadRequest):
                await message.answer(
                    "Помилка, я не можу автовидалити своє повідомлення, мені потрібні права адміна"
                )
    elif await teachers_exists_sql(message.from_user.id):
        if message.chat.type == "private":
            await message.answer("Ваша клавіатура ⌨️", reply_markup=kb_teachers)
        else:
            try:
                msg = await message.answer("⚠️ Ви зареєстрованні")
                await asyncio.sleep(2)
                await message.delete()
                await msg.delete()
            except (MessageToDeleteNotFound, MessageCantBeDeleted, BadRequest):
                await message.answer(
                    "Помилка, я не можу автовидалити своє повідомлення, мені потрібні права адміна"
                )
    elif await admin_exists_sql(message.from_user.id):
        if message.chat.type == "private":
            await message.answer(
                "🤔 Реєстрація 🤔\nВиберіть тип акаунту ⬇️", reply_markup=kb_choice
            )
            await FSMReg.reply_reg.set()
        else:
            try:
                msg = await message.answer(
                    "🤨 Перейдіть в особисті повідомлення до @pedbot_bot\nі зареєструйтесь за командою /start"
                )
                await asyncio.sleep(2)
                await message.delete()
                await msg.delete()
            except (MessageToDeleteNotFound, MessageCantBeDeleted, BadRequest):
                await message.answer(
                    "Помилка, я не можу автовидалити своє повідомлення, мені потрібні права адміна"
                )


async def reg(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.finish()
        if await admin_exists_sql(message.from_user.id):
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start_admin)
        elif await user_exists_sql(message.from_user.id):
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start_user)
        elif await teachers_exists_sql(message.from_user.id):
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start_user)
        else:
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start)
    elif message.text == "Адміністратор 🔐":
        await FSMReg.password_reg.set()
        await message.answer("🔒 Введіть пароль 🔑", reply_markup=ReplyKeyboardRemove())
    elif message.text == "Студент 👩‍🎓":
        await FSMReg.course_groupe_reg.set()
        await message.answer(
            "⬇️ Введіть курс і групу з наведених нижче", reply_markup=await get_kb()
        )
    elif message.text == "Викладач 👨‍🏫":
        await FSMReg.teachers_reg.set()
        await message.answer(
            "⬇️ Введіть ініціали з наведених нижче", reply_markup=await get_t_kb()
        )
    else:
        await message.answer("☹️ Немає такої відповіді ☹️", reply_markup=kb_start)
        await state.finish()


async def regAdmin(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.finish()
        if await admin_exists_sql(message.from_user.id):
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start_admin)
        elif await user_exists_sql(message.from_user.id):
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start_user)
        elif await teachers_exists_sql(message.from_user.id):
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start_user)
        else:
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start)
    elif message.text == passwords:
        if await admin_exists_sql(message.from_user.id):
            await message.answer("Ви вже адмін", reply_markup=kb_start_admin)
            await state.finish()
        else:
            first_name = message.from_user.first_name
            username = message.from_user.username
            await add_admin_sql(message.from_user.id, first_name, username)
            await message.answer("✅ Реєстрація завершена ✅", reply_markup=kb_admin)
            await state.finish()
    else:
        await message.answer("☹️ пароль неправильний ☹️", reply_markup=kb_start)
        await state.finish()


async def regUser(message: types.Message, state: FSMContext):
    first_name = message.from_user.first_name
    username = message.from_user.username
    groupe = message.text
    if message.text == "Назад":
        await state.finish()
        if await admin_exists_sql(message.from_user.id):
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start_admin)
        elif await user_exists_sql(message.from_user.id):
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start_user)
        elif await teachers_exists_sql(message.from_user.id):
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start_user)
        else:
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start)
    elif await group_exists_sql(message.text):
        await add_user_sql(message.from_user.id, first_name, username, groupe)
        await state.finish()
        await message.answer("✅ Реєстрація завершена ✅", reply_markup=kb_client)
    else:
        await message.answer(
            "☹️ Немає такої групи, звяжіться з адміністратором\nдля того щоб її додали \nІ повторіть спробу",
            reply_markup=kb_start,
        )
        await state.finish()


async def regTeachers(message: types.Message, state: FSMContext):
    first_name = message.from_user.first_name
    username = message.from_user.username
    teachers_name = message.text
    if message.text == "Назад":
        await state.finish()
        if await admin_exists_sql(message.from_user.id):
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start_admin)
        elif await user_exists_sql(message.from_user.id):
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start_user)
        elif await teachers_exists_sql(message.from_user.id):
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start_user)
        else:
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start)
    elif await teachers_name_exists_sql(message.text):
        await add_teachers_sql(
            message.from_user.id, first_name, username, teachers_name
        )
        await state.finish()
        await message.answer("✅ Реєстрація завершена ✅", reply_markup=kb_teachers)
    else:
        await message.answer(
            "☹️ Немає такого вчителя, звяжіться з адміністратором\nдля того щоб його додали \nІ повторіть спробу",
            reply_markup=kb_start,
        )
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


# ===========================Інформація для абітурієнта============================
async def for_applicant(message: types.Message):
    await stats_schedule_add("Для абітурієнта 🧑‍💻", 1)
    await message.answer("Інформація для абітурієнта", reply_markup=kb_for_applicant)



#                             КОМАНДИ

# @dp.message_handler(commands=["coupes"])
async def view_coupes_comm(message: types.Message):
    if await user_exists_sql(message.from_user.id):
        boolen, photo, date = await see_rod_sql(message.from_user.id)
        if boolen:
            try:
                await message.answer_photo(photo, date)
            except BadRequest:
                pass
        elif not boolen:
            try:
                msg = await message.answer("☹️ Розкладу для вашої групи ще немає... ☹️")
                await asyncio.sleep(4)
                await message.delete()
                await msg.delete()
            except (MessageToDeleteNotFound, MessageCantBeDeleted, BadRequest):
                await message.answer(
                    "Помилка, я не можу автовидалити своє повідомлення, мені потрібні права адміна"
                )
    else:
        if message.chat.type == "private":
            await message.answer(
                "❗️Зареєструйтесь❗️", reply_markup=ReplyKeyboardRemove()
            )
        else:
            try:
                msg = await message.answer(
                    "❗️Перейдіть до @pedbot_bot і зареєструйтесь",
                    reply_markup=ReplyKeyboardRemove(),
                )
                await asyncio.sleep(4)
                await message.delete()
                await msg.delete()
            except (MessageToDeleteNotFound, MessageCantBeDeleted, BadRequest):
                await message.answer(
                    "Помилка, я не можу автовидалити своє повідомлення, мені потрібні права адміна"
                )


# @dp.message_handler(commands=["delete_keyboards"])
async def delete_keyboard(message: types.Message):
    try:
        msg = await message.answer(
            "♻️Клавіатуру видалено♻️", reply_markup=ReplyKeyboardRemove()
        )
        await asyncio.sleep(4)
        await message.delete()
        await msg.delete()
    except (MessageToDeleteNotFound, MessageCantBeDeleted, BadRequest):
        await message.answer(
            "Помилка, я не можу автовидалити своє повідомлення, мені потрібні права адміна"
        )


# @dp.message_handler(commands=["version"])
async def versions(message: types.Message):
    try:
        version = (
            "Версія бота : release 1.5 \nВерсія Python : 3.11.1\nВерсія Aiogram : 2.24"
        )
        await message.answer(version)
    except (MessageToDeleteNotFound, MessageCantBeDeleted, BadRequest):
        await message.answer(
            "Помилка, я не можу автовидалити своє повідомлення, мені потрібні права адміна"
        )


# @dp.message_handler(commands=["info"])
async def donate(message: types.Message):
    await stats_schedule_add("Донат 🫡", 1)
    version = "Підтримати проєкт можна\nза номером карти : 5375411202975004\n\
або за посиланням : <a href='https://send.monobank.ua/jar/5uzN1NcwYA'>monobank</a>"
    await message.answer(version,parse_mode="HTML",disable_web_page_preview=True)


# @dp.message_handler(commands=["help"])
async def help(message: types.Message):
    await stats_schedule_add("Команди 🛠", 1)
    try:
        help = """❗️Команди з префіксом '/'
зручно використовувати в групах.

❓Щоб використовувати бота в групах:
1.Додайте його у свою групу.
2.Дайте права адміністратора.
3.Напишіть / і бот покаже всі доступні команди.
"""
        await message.answer(help)
    except (MessageToDeleteNotFound, MessageCantBeDeleted, BadRequest):
        pass


async def about_bot(message: types.Message):
    await stats_schedule_add("Про бота 🖇", 1)
    await message.answer(
"""БОТ ВПК ПЕДКІТ
Версія : release 1.5
Розробник: <a href='https://t.me/salkooua'>Мусаєв Джаміль</a>
Зробив аватарку: <a href='https://t.me/yurchh'>Коновалець Юра</a>

Бот створено для спрощення
виконання будь - яких речей
зв'язаних з коледжем
У ньому є купа потрібних
і не дуже функцій, які
розставленні в зручних місцях

<a href='https://vvpc.com.ua/'>Офіційний сайт ВПФК</a>
""",parse_mode="HTML",disable_web_page_preview=True)


async def stats_all(message: types.Message):
    boolean, text = await see_all_stats()
    check, value_stud = await count_user_sql()
    check, value_teach = await count_teacher_sql()
    await message.answer(
f"""📊 Статистика користувачів :
 • Кількість студентів у боті : {value_stud}
 • Кількість викладачів у боті : {value_teach}

🧮Статистика активності за місяць :
{text}
(Натискання цих кнопок)
""")


# ===========================реєстратор============================
def register_handler_other(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"])
    dp.register_message_handler(menu, text="Меню 👥")
    dp.register_message_handler(about_bot, text="Про бота 🖇")
    dp.register_message_handler(about_collasge, text="Про коледж 🛡")
    dp.register_message_handler(introduction, text="Вступ 📗")
    dp.register_message_handler(time_work, text="Час роботи 📅")
    dp.register_message_handler(addres, text="Адреса 📫")
    dp.register_message_handler(others, text="Інше 📌")
    dp.register_message_handler(stick, text="Стікери 👨‍👩‍👧‍👦")
    dp.register_message_handler(for_applicant, text="Для абітурієнта 🧑‍💻")
    dp.register_message_handler(stats_all, text="Статистика 🧮")
    dp.register_message_handler(stats_all, commands=["stats"])

    dp.register_message_handler(specialty, text="Спеціальності 📜", state=None)
    dp.register_message_handler(specialty1, state=FSMReg.specialtys)
    # Реєстрація
    dp.register_message_handler(
        registration, text=["Реєстрація ⚙️", "Розклад ⚙️"], state=None
    )
    dp.register_message_handler(reg, state=FSMReg.reply_reg)
    dp.register_message_handler(regAdmin, state=FSMReg.password_reg)
    dp.register_message_handler(regUser, state=FSMReg.course_groupe_reg)
    dp.register_message_handler(regTeachers, state=FSMReg.teachers_reg)
    # Команди
    dp.register_message_handler(help, text="Команди 🛠")
    dp.register_message_handler(help, commands=["help"])
    # Підтримка
    dp.register_message_handler(donate, text="Донат 🫡")
    dp.register_message_handler(donate, commands=["donate"])
    # Розклад
    dp.register_message_handler(view_coupes_comm, commands=["coupes"])
    # Видалення клавіатури
    dp.register_message_handler(delete_keyboard, commands=["delete_keyboards"])
    # Версія
    dp.register_message_handler(versions, commands=["version"])
