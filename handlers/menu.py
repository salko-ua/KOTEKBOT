# from import
import os
import random

from aiogram import F, Router, types

from data_base import Database
from keyboards import *

router = Router()

# Розклад 📚
@router.message(F.text == "Розклад 📚", F.chat.type == "private")
async def schedule(message: types.Message):
    await message.delete()

    if not await check_all(message):
        await message.answer("Ви повинні бути зарєстровані❗️", reply_markup=await hide_kb())
        return

    await message.answer("Перегляд розкладу ⬇️", reply_markup=await schedule_kb(message.from_user.id))

# =======================================================
# Інше 📌
@router.message(F.text == "Інше 📌", F.chat.type == "private")
async def others(message: types.Message):
    await message.delete()
    await message.answer("Інша інформація 🤯", reply_markup=await other_kb())

# Інше 📌
@router.callback_query(F.data == "other_inline")
async def others_inline(query: types.CallbackQuery):
    await query.message.delete()
    await query.message.answer("Інша інформація 🤯", reply_markup=await other_kb())


# Стікери 👨‍👩‍👧‍👦
@router.callback_query(F.data == "Стікери 👨‍👩‍👧‍👦")
async def stick(query: types.CallbackQuery):
    await query.message.answer_sticker(r"CAACAgIAAxkBAAEH15Nj9O7fae-x_g7MdX6tus4wAh8SngACLQAD3jyHIuJ7Rhz4aJKDLgQ")
    await query.answer()

# Про бота 🖇
@router.callback_query(F.data == "Про бота 🖇")
async def about_bot(query: types.CallbackQuery):
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
    await query.message.edit_reply_markup(reply_markup=await other_back_kb())

# Про мене 👀
@router.callback_query(F.data == "Про мене 👀")
async def about_me(query: types.CallbackQuery):
    user_id = query.from_user.id
    url = query.from_user.url
    check, text = await get_about_me(user_id, url)

    await query.message.edit_text(text, 
                         parse_mode="HTML",
                         disable_web_page_preview=True)
    await query.message.edit_reply_markup(reply_markup=await other_back_kb())
    
# Допомога 🛠
@router.callback_query(F.data == "Допомога 🛠")
async def help(query: types.CallbackQuery):
    help = "Пишіть сюди : @botadmincat"
    await query.message.edit_text(help)
    await query.message.edit_reply_markup(reply_markup=await other_back_kb())

# Час роботи 📅
@router.callback_query(F.data == "Час роботи 📅")
async def time_work(query: types.CallbackQuery):
    time_work = (
        "Час роботи ⌚️\n"
        "Понеділок - П'ятниця: 8:00–17:00.\n"
        "Субота - Неділя: Зачинено."
    )
    await query.message.edit_text(text=time_work)
    await query.message.edit_reply_markup(reply_markup=await other_back_kb())

# Фото кота 🖼
@router.callback_query(F.data == "Фото кота 🖼")
async def send_random_cat_photo(query: types.CallbackQuery):
    await query.message.delete()

    try:
        photo_path = await choose_random_photo()
        file_path = types.FSInputFile(photo_path)
        await query.message.answer_photo(file_path, reply_markup=await other_back_kb())
    except:
        await query.message.answer("Фото кота ще не додано 😿", reply_markup=await other_back_kb())

# Донат 🫡
@router.callback_query(F.data == "Донат 🫡")
async def donate(query: types.CallbackQuery):
    text = (f"Підтримати проєкт можна за:\n\n"
            f"💳 Monobank card : <code>5375411202975004</code>\n"
            f"💳 Monobank url : <a href='https://send.monobank.ua/jar/5uzN1NcwYA'>monobank</a>\n\n"
            f"❤️ Повернись живим : <a href='https://savelife.in.ua/'>сайт</a>\n\n"
            f"Кошти підуть на оплату хостингу та покращення бота 🌚")

    await query.message.edit_text(
        text,
        parse_mode="HTML",
        disable_web_page_preview=True)
    await query.message.edit_reply_markup(reply_markup=await url_card_kb())

#==============================================
# Для абітурієнта 🧑‍💻
@router.message(F.text == "Для абітурієнта 🧑‍💻", F.chat.type == "private")
async def for_applicant(message: types.Message):
    await message.delete()
    await message.answer("Інформація для абітурієнта 😵‍💫", reply_markup=await applicant_kb())

# Для абітурієнта 🧑‍💻
@router.callback_query(F.data == "applicant_inline")
async def for_applicant_inline(query: types.CallbackQuery):
    await query.message.delete()
    await query.message.answer("Інформація для абітурієнта 😵‍💫",
                               reply_markup=await applicant_kb())

# Вступ 📗
@router.callback_query(F.data == "Вступ 📗")
async def introduction(query: types.CallbackQuery):
    photo_path = "photo/introduction.jpg"
    file_path = types.FSInputFile(photo_path)

    await query.message.delete()
    await query.message.answer_photo(
        photo=file_path,
        caption="<b><code>Інформація для вступника 2023 👩‍🎓</code></b>", 
        reply_markup=await url_introduction_kb(),
        parse_mode="HTML")

# Про коледж 🛡
@router.callback_query(F.data == "Про коледж 🛡")
async def about_collasge(query: types.CallbackQuery):
    photo_path = "photo/about_collage.jpg"
    file_path = types.FSInputFile(photo_path)

    await query.message.delete()
    await query.message.answer_photo(
        photo=file_path,
        caption="""<code><b>Інформація про Володимирський\nпедагогічний фаховий коледж\nімені А.Ю. Кримського\nВолинської обласної ради</b></code>""",
        parse_mode="HTML",
        reply_markup=await url_about_college_kb(),)

# Адреса 📫
@router.callback_query(F.data == "Адреса 📫")
async def addres(query: types.CallbackQuery):
    location = (
        "•Земля 🌍\n"
        "•Україна 🇺🇦\n"
        "•Волинська область 🌉\n"
        "•Володимир 44700 🌆\n"
        "•Вул. Устилузька 42 🛣"
    )
    await query.message.edit_text(location)
    await query.message.edit_reply_markup(reply_markup=await applicant_back_kb())

# Контакти 📘
@router.callback_query(F.data == "Контакти 📘")
async def contact(query: types.CallbackQuery):
    contacts = (
        "📱 Контактні телефони: \n"
        "    - (03342)35555 (факс), \n"
        "    - 20950 (приймальна комісія)\n\n"
        "📨 Пошта :\n"
        "    - E-mail: post@vvpc.com.ua"
    )
    await query.message.edit_text(text=contacts)
    await query.message.edit_reply_markup(reply_markup=await url_contact_kb())

# Реквізити 💳
@router.callback_query(F.data == "Реквізити 💳")
async def score(query: types.CallbackQuery):
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
        f"Вказати прізвище студента, курс та групу")
    await query.message.edit_text(text=text, parse_mode="HTML")
    await query.message.edit_reply_markup(reply_markup=await url_score_kb())

# Офіційний сайт 🌎
@router.callback_query(F.data == "Офіційний сайт 🌎")
async def official_site(query: types.CallbackQuery):
    await query.message.edit_text("Офіційний сайт ВПК 📰")
    await query.message.edit_reply_markup(reply_markup=await url_official_site_kb())

# Спеціальності 📜
@router.callback_query(F.data == "Спеціальності 📜")
async def specialty(query: types.CallbackQuery):
    await query.message.edit_text("Cпеціальності 📜 ВВПФК")
    await query.message.edit_reply_markup(reply_markup=await url_speciality_kb())


# ===============================================
# Допоміжні функції
async def menu(message: types.Message):
    db = await Database.setup()
    if await db.admin_exists_sql(message.from_user.id):
        await message.answer("⬇️Головне меню⬇️", reply_markup=await start_admin_kb())
    elif await db.student_exists_sql(message.from_user.id):
        await message.answer("⬇️Головне меню⬇️", reply_markup=await start_student_kb())
    elif await db.teacher_exists_sql(message.from_user.id):
        await message.answer("⬇️Головне меню⬇️", reply_markup=await start_teacher_kb())
    else:
        await message.answer("⬇️Головне меню⬇️", reply_markup=await start_all_kb())

async def check_user(user_id: int):
    db = await Database.setup()
    if await db.admin_exists_sql(user_id):
        admin = "✅"
    else:
        admin = "❌"

    if await db.student_exists_sql(user_id):
        student = await db.group_for_student_id_sql(user_id)
    else:
        student = "❌"

    if await db.teacher_exists_sql(user_id):
        teacher = await db.group_for_teacher_id_sql(user_id)
    else:
        teacher = "❌"

    return admin, student, teacher

async def check_all(message: types.Message):
    db = await Database.setup()
    user_id = message.from_user.id
    if (await db.student_exists_sql(user_id) or
        await db.teacher_exists_sql(user_id) or
        await db.admin_exists_sql(user_id)):
        return True
    else:
        return False

async def get_about_me(user_id, url):
    db = await Database.setup()
    
    if not await db.user_exists_sql(user_id):
        return False, None
    
    data = await db.user_show_data_sql(user_id)
    data = data[0]
    data_group = await check_user(user_id)

    message_text = (
        f"<b>👤 Ім'я: <a href='{url}'>{data[1]}</a> | {data[0]}</b>\n"
        f"<b>📅 Дата реєстації: {data[4]}</b>\n\n"
        f"<b>📊 Кількість взаємодій: {data[5]}</b>\n\n"
        f"<b>👨‍💼 Адмін:</b> {data_group[0]}\n"
        f"<b>👩‍🎓 Студент:</b> {data_group[1]}\n"
        f"<b>👨‍🏫 Викладач:</b> {data_group[2]}\n\n"
        f"<b>⌛️ Остання взаємодія з\n"
        f"ботом: {data[6]}</b>\n"
        f"(ця не враховується)\n"
    )

    return True, message_text

async def choose_random_photo():
    folder_path = "cat/"
    file_list = os.listdir(folder_path)
    random_file = random.choice(file_list)
    file_path = os.path.join(folder_path, random_file)
    return file_path

