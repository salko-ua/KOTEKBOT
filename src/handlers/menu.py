
from aiogram import F, Router, types

from src.keyboards import *
from src.utils import check_who, choose_random_photo, get_about_me

router = Router()


@router.message(F.text == "Розклад 📚")
async def schedule(message: types.Message) -> None:
    await message.delete()
    telegram_id = message.from_user.id

    if not await check_who(message):
        await message.answer(text="Ви повинні бути зарєстровані❗️", reply_markup=hide_kb())
        return

    await message.answer(text="Перегляд розкладу ⬇️", reply_markup=await schedule_kb(telegram_id))


@router.callback_query(F.data == "student_back_kb")
async def back_student(query: types.CallbackQuery) -> None:
    telegram_id = query.from_user.id
    await query.message.delete()
    await query.message.answer(
        text="Ваша клавіатура ⌨️", reply_markup=await schedule_kb(telegram_id)
    )


@router.message(F.text == "Інше 📌")
@router.callback_query(F.data == "other_inline")
async def others(event: types.Message | types.CallbackQuery) -> None:
    if not isinstance(event, types.Message):
        await event.message.delete()
        await event.message.answer(text="Інша інформація 🤯", reply_markup=other_kb())
        return

    await event.delete()
    await event.answer(text="Інша інформація 🤯", reply_markup=other_kb())


@router.message(F.text == "Для абітурієнта 🧑‍💻")
@router.callback_query(F.data == "applicant_inline")
async def for_applicant(event: types.Message | types.CallbackQuery) -> None:
    if not isinstance(event, types.Message):
        await event.message.delete()
        await event.message.answer(
            text="Інформація для абітурієнта 😵‍💫", reply_markup=applicant_kb()
        )
        return

    await event.delete()
    await event.answer(text="Інформація для абітурієнта 😵‍💫", reply_markup=applicant_kb())


@router.callback_query(F.data == "Про бота 🖇")
async def about_bot(query: types.CallbackQuery) -> None:
    about_bot_text = (
        f"🤖 БОТ ВПФК ПЕДКІТ\n"
        f"🆙 Версія : 2.1\n"
        f"👨‍💻 Розробник: <a href='https://t.me/salkooua'>Salo</a>\n"
        f"🎨 Дизайн ави: <a href='https://t.me/pupqwert'>Reloadddddd</a>\n\n"
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
    await query.message.edit_text(about_bot_text, parse_mode="HTML", disable_web_page_preview=True)
    await query.message.edit_reply_markup(reply_markup=other_back_kb())


@router.callback_query(F.data == "Про мене 👀")
async def about_me(query: types.CallbackQuery) -> None:
    user_id = query.from_user.id
    url = query.from_user.url
    text = await get_about_me(user_id, url)

    await query.message.edit_text(text, parse_mode="HTML", disable_web_page_preview=True)
    await query.message.edit_reply_markup(reply_markup=other_back_kb())


@router.callback_query(F.data == "Допомога 🛠")
async def get_help(query: types.CallbackQuery) -> None:
    help_text = "Пишіть сюди : @botadmincat"
    await query.message.edit_text(help_text)
    await query.message.edit_reply_markup(reply_markup=other_back_kb())


@router.callback_query(F.data == "Час роботи 📅")
async def time_work(query: types.CallbackQuery) -> None:
    time_work_text = (
        "Час роботи ⌚️\n" "Понеділок - П'ятниця: 8:00–17:00.\n" "Субота - Неділя: Зачинено."
    )
    await query.message.edit_text(text=time_work_text)
    await query.message.edit_reply_markup(reply_markup=other_back_kb())


@router.callback_query(F.data == "Фото кота 🖼")
async def send_random_cat_photo(query: types.CallbackQuery) -> None:
    await query.message.delete()

    try:
        photo_path = await choose_random_photo()
        file_path = types.FSInputFile(photo_path)
        await query.message.answer_photo(file_path, reply_markup=other_back_kb())
    except Exception:
        await query.message.answer(text="Фото кота ще не додано 😿", reply_markup=other_back_kb())


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
    await query.message.edit_reply_markup(reply_markup=url_card_kb())


@router.callback_query(F.data == "Вступ 📗")
async def introduction(query: types.CallbackQuery) -> None:
    photo_path = "photo/introduction.jpg"
    file_path = types.FSInputFile(photo_path)

    await query.message.delete()
    await query.message.answer_photo(
        photo=file_path,
        caption="<b><code>Інформація для вступника 2023 👩‍🎓</code></b>",
        reply_markup=url_introduction_kb(),
        parse_mode="HTML",
    )


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
        reply_markup=url_about_college_kb(),
    )


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
    await query.message.edit_reply_markup(reply_markup=applicant_back_kb())


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
    await query.message.edit_reply_markup(reply_markup=url_contact_kb())


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
    await query.message.edit_reply_markup(reply_markup=url_score_kb())


@router.callback_query(F.data == "Офіційний сайт 🌎")
async def official_site(query: types.CallbackQuery) -> None:
    await query.message.edit_text("Офіційний сайт ВПК 📰")
    await query.message.edit_reply_markup(reply_markup=url_official_site_kb())


@router.callback_query(F.data == "Спеціальності 📜")
async def specialty(query: types.CallbackQuery) -> None:
    await query.message.edit_text("Cпеціальності 📜 ВВПФК")
    await query.message.edit_reply_markup(reply_markup=url_speciality_kb())



