# from import
from aiogram import F, Router, types
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext

from data_base import Database
from handlers.text_handlers import menu_text
from keyboards import *

router = Router()


# ===========================Меню 👥============================
async def menu(message: types.Message):
    db = await Database.setup()
    if await db.admin_exists_sql(message.from_user.id):
        await message.answer("⬇️Головне меню⬇️", reply_markup=await start_admin_kb())
    elif await db.student_exists_sql(message.from_user.id):
        await message.answer("⬇️Головне меню⬇️", reply_markup=await start_user_kb())
    elif await db.teacher_exists_sql(message.from_user.id):
        await message.answer("⬇️Головне меню⬇️", reply_markup=await start_user_kb())
    else:
        await message.answer("⬇️Головне меню⬇️", reply_markup=await start_all_kb())


#                          Елемнти Меню
@router.message(Text(text=menu_text["introduction"], ignore_case=True))
# ===========================Вступ 📗============================
async def introduction(message: types.Message):
    photo_path = "photo/introduction.jpg"
    file_path = types.FSInputFile(photo_path)
    await message.answer_photo(
        photo=file_path,
        caption="<code><b>Інформація для вступника 2023</b></code>",
        parse_mode="HTML",
        reply_markup=await url_introduction_kb(),
    )


@router.message(Text(text=menu_text["about_collasge"], ignore_case=True))
# ===========================Про коледж 🛡============================
async def about_collasge(message: types.Message):
    photo_path = "photo/about_collage.jpg"
    file_path = types.FSInputFile(photo_path)
    await message.answer_photo(
        photo=file_path,
        caption="""<code><b>Інформація про Володимирський\nпедагогічний фаховий коледж\nімені А.Ю. Кримського\nВолинської обласної ради</b></code>""",
        parse_mode="HTML",
        reply_markup=await url_about_college_kb(),
    )


@router.message(Text(text=menu_text["time_work"], ignore_case=True))
# ===========================Час роботи 📅============================
async def time_work(message: types.Message):
    await message.answer(
        """Час роботи ⌚️
Понеділок - П'ятниця: 8:00–17:00.
Субота - Неділя: Зачинено."""
    )


@router.message(Text(text=menu_text["addres"], ignore_case=True))
# ===========================Адреса 📫============================
async def addres(message: types.Message):
    await message.answer(
        """•Земля 🌍
•Україна 🇺🇦
•Волинська область 🌉
•Володимир 44700 🌆
•Вул. Устилузька 42 🛣"""
    )


@router.message(Text(text=menu_text["contact"], ignore_case=True))
# ===========================Контакти ============================
async def contact(message: types.Message):
    await message.answer(
        """
📱 Контактні телефони: 
    - (03342)35555 (факс), 
    - 20950 (приймальна комісія)

📨 Пошта :
    - E-mail: post@vvpc.com.ua
""",
        reply_markup=await url_contact_kb(),
    )


@router.message(Text(text="Спеціальності 📜", ignore_case=True))
# ===========================Спеціальності 📜============================
async def specialty(message: types.Message, state: FSMContext):
    await message.answer(
        "Cпеціальності 📜 ВВПФК", reply_markup=await url_speciality_kb()
    )


@router.message(Text(text=menu_text["others"], ignore_case=True))
# ===========================Інше 📌============================
async def others(message: types.Message):
    await message.answer("Інше 🫤", reply_markup=await other_kb())


@router.message(Text(text=menu_text["stick"], ignore_case=True))
# ===========================Стікери 👨‍👩‍👧‍👦============================
async def stick(message: types.Message):
    await message.answer_sticker(
        r"CAACAgIAAxkBAAEH15Nj9O7fae-x_g7MdX6tus4wAh8SngACLQAD3jyHIuJ7Rhz4aJKDLgQ"
    )


@router.message(Text(text=menu_text["about_bot"], ignore_case=True))
# ===========================Про бота 🖇============================
async def about_bot(message: types.Message):
    await message.answer(
        """🤖 БОТ ВПФК ПЕДКІТ
🆙 Версія : release 2.0
👨‍💻 Розробник: <a href='https://t.me/salkooua'>Salo</a>
🎨 Дизайн ави: <a href='https://t.me/rchpsd'>Коновалець Юра</a>

📅 Початок розробки : Січень 2023-го року

Бот створено для спрощення
виконання будь-яких речей,
зв'язаних з коледжем. У ньому
є купа потрібних і не дуже
функцій, які розставлені в
зручних місцях. Використовуйте
його для економлення часу!

🌐 <a href='https://vvpc.com.ua/'>Офіційний сайт ВПФК</a>
""",
        parse_mode="HTML",
        disable_web_page_preview=True,
    )


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


@router.message(Command("me"))
@router.message(Text(text=menu_text["about_me"], ignore_case=True))
# ===========================Про бота 🖇============================
async def about_bot(message: types.Message):
    db = await Database.setup()
    user_id = message.from_user.id

    if await db.user_exists_sql(user_id):
        data = await db.user_show_data_sql(user_id)
        data = data[0]
        data_group = await check_user(user_id)

        message_text = f"""
<b>👤 Ім'я: <a href="{message.from_user.url}">{data[1]}</a> | {data[0]}</b>
<b>📅 Дата реєстації: {data[4]}</b>

<b>📊 Кількість повідомлень: {data[5]}</b>

<b>👨‍💼 Адмін:</b> {data_group[0]}
<b>👩‍🎓 Студент:</b> {data_group[1]}
<b>👨‍🏫 Викладач:</b> {data_group[2]}

<b>⌛️ Останнє повідомлення 
боту: {data[6]}</b>
(це не враховується)
"""
        await message.answer(
            message_text, disable_web_page_preview=True, parse_mode="HTML"
        )


@router.message(Text(text="Для абітурієнта 🧑‍💻", ignore_case=True))
# ===========================Інформація для абітурієнта============================
async def for_applicant(message: types.Message):
    await message.answer(
        "Інформація для абітурієнта 😵‍💫", reply_markup=await for_applicant_kb()
    )


@router.message(Text(text=menu_text["score"], ignore_case=True))
async def score(message: types.Message):
    await message.answer(
        """
❗️ Перевірте чи інформація актуальна ❗️
Це можна зробити кнопкою під повідомленням

<b>Реквізити оплати за навчання (станом на 15.05.22)</b>
Банк ГУДКСУ Волинської області

Код ЄДРПОУ 02125941

Рахунок: <code>UA368201720314241003201023033</code>

Призначення платежу: плата за навчання

Вказати прізвище студента, курс та групу

 
<b>Реквізити оплати за гуртожиток (станом на 15.05.22)</b>
Банк ГУДКСУ Волинської області

Код ЄДРПОУ 02125941

Рахунок: <code>UA378201720314211003202023033</code>

Призначення платежу: плата за гуртожиток

Вказати прізвище студента, курс та групу
        """,
        parse_mode="HTML",
        reply_markup=await url_score_kb(),
    )


@router.message(Text(text=menu_text["official_site"], ignore_case=True))
async def official_site(message: types.Message):
    await message.answer(
        "Офіційний сайт ВПК 📰", reply_markup=await url_official_site_kb()
    )
