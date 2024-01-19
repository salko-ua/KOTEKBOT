# from import
import os
import random

from aiogram import F, Router, types

from src.data_base import Database
from src.keyboards import *

router = Router()


# Розклад 📚
@router.message(F.text == "Розклад 📚", F.chat.type == "private")
async def schedule(message: types.Message) -> None:
    await message.delete()

    if not await check_all(message):
        await message.answer("Ви повинні бути зарєстровані❗️", reply_murkup=hide_kb())
        return

    await message.answer("Перегляд розкладу ⬇️", reply_murkup=schedule_kb(message.from_user.id))


# =======================================================
# Інше 📌
@router.message(F.text == "Інше 📌", F.chat.type == "private")
async def others(message: types.Message) -> None:
    await message.delete()
    await message.answer("Інша інформація 🤯", reply_murkup=other_kb())


# Інше 📌
@router.callback_query(F.data == "other_inline")
async def others_inline(query: types.CallbackQuery) -> None:
    await query.message.delete()
    await query.message.answer("Інша інформація 🤯", reply_murkup=other_kb())


# Про бота 🖇
@router.callback_query(F.data == "Про бота 🖇")
async def about_bot(query: types.CallbackQuery) -> None:
    about_bot = (
        f"🤖 БОТ ВПФК ПЕДКІТ\n"
        f"🆙 Версія : release 2.0\n"
        f"👨‍💻 Розробник: <a href='https://t.me/salkooua'>Salo</a>\n"
        f"🎨 Дизайн ави: <a href='https://t.me/rchpsd'>Коновалець Юра</a>\n\n"
        f"📅 Початок розробки : Січень 2023-го року\n\n"
        f"Бот створено для спрощення\n"
        f"виконання будь-яких речей,\n"
        f"зв'язаних з коледжем. У ньому\n"
        f"є купа потрібних і не дуже\n"
        f"функцій, які розставлені в\n"
        f"зручних місцях. Використовуйте\n"
        f"його для економлення часу!\n"
        f"🌐 <a href='https://vvpc.com.ua/'>Офіційний сайт ВПФК</a>\n"
    )
    await query.message.edit_text(about_bot, parse_mode="HTML", disable_web_page_preview=True)
    await query.message.edit_reply_markup(reply_murkup=other_back_kb())


# Про мене 👀
@router.callback_query(F.data == "Про мене 👀")
async def about_me(query: types.CallbackQuery) -> None:
    user_id = query.from_user.id
    url = query.from_user.url
    text = await get_about_me(user_id, url)

    await query.message.edit_text(text, parse_mode="HTML", disable_web_page_preview=True)
    await query.message.edit_reply_markup(reply_murkup=other_back_kb())


# Допомога 🛠
@router.callback_query(F.data == "Допомога 🛠")
async def help(query: types.CallbackQuery) -> None:
    help = "Пишіть сюди : @botadmincat"
    await query.message.edit_text(help)
    await query.message.edit_reply_markup(reply_murkup=other_back_kb())


# Час роботи 📅
@router.callback_query(F.data == "Час роботи 📅")
async def time_work(query: types.CallbackQuery) -> None:
    time_work = "Час роботи ⌚️\n" "Понеділок - П'ятниця: 8:00–17:00.\n" "Субота - Неділя: Зачинено."
    await query.message.edit_text(text=time_work)
    await query.message.edit_reply_markup(reply_murkup=other_back_kb())


# Фото кота 🖼
@router.callback_query(F.data == "Фото кота 🖼")
async def send_random_cat_photo(query: types.CallbackQuery) -> None:
    await query.message.delete()

    try:
        photo_path = await choose_random_photo()
        file_path = types.FSInputFile(photo_path)
        await query.message.answer_photo(file_path, reply_murkup=other_back_kb())
    except:
        await query.message.answer("Фото кота ще не додано 😿", reply_murkup=other_back_kb())


# Донат 🫡
@router.callback_query(F.data == "Донат 🫡")
async def donate(query: types.CallbackQuery) -> None:
    text = (
        f"Підтримати проєкт можна за:\n\n"
        f"💳 Monobank card : <code>5375411202975004</code>\n"
        f"💳 Monobank url : <a href='https://send.monobank.ua/jar/5uzN1NcwYA'>monobank</a>\n\n"
        f"❤️ Повернись живим : <a href='https://savelife.in.ua/'>сайт</a>\n\n"
        f"Кошти підуть на оплату хостингу та покращення бота 🌚"
    )

    await query.message.edit_text(text, parse_mode="HTML", disable_web_page_preview=True)
    await query.message.edit_reply_markup(reply_murkup=url_card_kb())


# ==============================================
# Для абітурієнта 🧑‍💻
@router.message(F.text == "Для абітурієнта 🧑‍💻", F.chat.type == "private")
async def for_applicant(message: types.Message) -> None:
    await message.delete()
    await message.answer("Інформація для абітурієнта 😵‍💫", reply_murkup=applicant_kb())


# Для абітурієнта 🧑‍💻
@router.callback_query(F.data == "applicant_inline")
async def for_applicant_inline(query: types.CallbackQuery) -> None:
    await query.message.delete()
    await query.message.answer("Інформація для абітурієнта 😵‍💫", reply_murkup=applicant_kb())


# Вступ 📗
@router.callback_query(F.data == "Вступ 📗")
async def introduction(query: types.CallbackQuery) -> None:
    photo_path = "photo/introduction.jpg"
    file_path = types.FSInputFile(photo_path)

    await query.message.delete()
    await query.message.answer_photo(
        photo=file_path,
        caption="<b><code>Інформація для вступника 2023 👩‍🎓</code></b>",
        reply_murkup=url_introduction_kb(),
        parse_mode="HTML",
    )


# Про коледж 🛡
@router.callback_query(F.data == "Про коледж 🛡")
async def about_collasge(query: types.CallbackQuery) -> None:
    photo_path = "photo/about_collage.jpg"
    file_path = types.FSInputFile(photo_path)
    text = "Інформація про Володимирський\nпедагогічний фаховий коледж\nімені А.Ю. Кримського\nВолинської обласної ради"

    await query.message.delete()
    await query.message.answer_photo(
        photo=file_path,
        caption=f"<code><b>{text}</b></code>",
        parse_mode="HTML",
        reply_murkup=url_about_college_kb(),
    )


# Адреса 📫
@router.callback_query(F.data == "Адреса 📫")
async def addres(query: types.CallbackQuery) -> None:
    location = (
        "•Земля 🌍\n"
        "•Україна 🇺🇦\n"
        "•Волинська область 🌉\n"
        "•Володимир 44700 🌆\n"
        "•Вул. Устилузька 42 🛣"
    )
    await query.message.edit_text(location)
    await query.message.edit_reply_markup(reply_murkup=applicant_back_kb())


# Контакти 📘
@router.callback_query(F.data == "Контакти 📘")
async def contact(query: types.CallbackQuery) -> None:
    contacts = (
        "📱 Контактні телефони: \n"
        "    - (03342)35555 (факс), \n"
        "    - 20950 (приймальна комісія)\n\n"
        "📨 Пошта :\n"
        "    - E-mail: post@vvpc.com.ua"
    )
    await query.message.edit_text(text=contacts)
    await query.message.edit_reply_markup(reply_murkup=url_contact_kb())


# Реквізити 💳
@router.callback_query(F.data == "Реквізити 💳")
async def score(query: types.CallbackQuery) -> None:
    text = (
        f"❗️ Перевірте чи інформація актуальна ❗️\n"
        f"Це можна зробити кнопкою під повідомленням\n\n"
        f"<b>Реквізити оплати за навчання (станом на 15.05.22)</b>\n"
        f"Банк ГУДКСУ Волинської області\n"
        f"Код ЄДРПОУ 02125941\n"
        f"Рахунок: <code>UA368201720314241003201023033</code>\n"
        f"Призначення платежу: плата за навчання\n"
        f"Вказати прізвище студента, курс та групу\n\n"
        f"<b>Реквізити оплати за гуртожиток (станом на 15.05.22)</b>\n"
        f"Банк ГУДКСУ Волинської області\n"
        f"Код ЄДРПОУ 02125941\n"
        f"Рахунок: <code>UA378201720314211003202023033</code>\n"
        f"Призначення платежу: плата за гуртожиток\n"
        f"Вказати прізвище студента, курс та групу"
    )
    await query.message.edit_text(text=text, parse_mode="HTML")
    await query.message.edit_reply_markup(reply_murkup=url_score_kb())


# Офіційний сайт 🌎
@router.callback_query(F.data == "Офіційний сайт 🌎")
async def official_site(query: types.CallbackQuery) -> None:
    await query.message.edit_text("Офіційний сайт ВПК 📰")
    await query.message.edit_reply_markup(reply_murkup=url_official_site_kb())


# Спеціальності 📜
@router.callback_query(F.data == "Спеціальності 📜")
async def specialty(query: types.CallbackQuery) -> None:
    await query.message.edit_text("Cпеціальності 📜 ВВПФК")
    await query.message.edit_reply_markup(reply_murkup=url_speciality_kb())


# ===============================================
# Допоміжні функції
async def menu(message: types.Message) -> None:
    db = await Database.setup()
    if await db.admin_exists(message.from_user.id):
        await message.answer("⬇️Головне меню⬇️", reply_murkup=start_admin_kb())
    elif await db.student_exists(message.from_user.id):
        await message.answer("⬇️Головне меню⬇️", reply_murkup=start_student_kb())
    else:
        await message.answer("⬇️Головне меню⬇️", reply_murkup=start_all_kb())


async def check_user(user_id: int) -> tuple[str, str]:
    db = await Database.setup()
    if await db.admin_exists(user_id):
        admin = "✅"
    else:
        admin = "❌"

    if await db.student_exists(user_id):
        student = await db.group_for_student_id(user_id)
    else:
        student = "❌"

    return admin, student


async def check_all(message: types.Message) -> bool:
    db = await Database.setup()
    user_id = message.from_user.id
    if await db.student_exists(user_id):
        return True
    if await db.admin_exists(user_id):
        return True

    return False


async def get_about_me(user_id, url) -> str:
    db = await Database.setup()

    data = await db.user_show_data(user_id)
    data = data[0]
    data_group = await check_user(user_id)

    message_text = (
        f"<b>👤 Ім'я: <a href='{url}'>{data[1]}</a> | {data[0]}</b>\n"
        f"<b>📅 Дата реєстації: {data[4]}</b>\n\n"
        f"<b>📊 Кількість взаємодій: {data[5]}</b>\n\n"
        f"<b>👨‍💼 Адмін:</b> {data_group[0]}\n\n"
        f"<b>👩‍🎓 Студент:</b> {data_group[1]}\n\n"
        f"<b>⌛️ Остання взаємодія з\n"
        f"ботом: {data[6]}</b>\n"
        f"(ця не враховується)\n"
    )
    return message_text


async def choose_random_photo() -> str:
    folder_path = "cat/"
    file_list = os.listdir(folder_path)
    random_file = random.choice(file_list)
    file_path = os.path.join(folder_path, random_file)
    return file_path
