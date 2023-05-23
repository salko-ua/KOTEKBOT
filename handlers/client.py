import datetime

from keyboards import *
from aiogram import types
from data_base import Database
from config import super_admin_admin, super_admin_ura

from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from schedulers.alarm import alert_func
from handlers.stats import stats_schedule_add






# ===========================Переглянути розклад============================
async def view_coupes(message: types.Message):
    db = await Database.setup()
    await stats_schedule_add("Розклад пар 👀", 1)
    if await db.user_exists_sql(message.from_user.id):
        boolen, photo, date = await db.see_rod_sql(message.from_user.id)
        if boolen:
            await message.answer_photo(photo, date)
        elif not boolen:
            await message.answer("☹️Розкладу для вашої групи ще немає...☹️")
    elif await db.teachers_exists_sql(message.from_user.id):
        boolen, photo, date = await db.see_rod_t_sql(message.from_user.id)
        if boolen:
            await message.answer_photo(photo, date)
        elif not boolen:
            await message.answer("☹️Розкладу для ваc ще немає...☹️")
    elif not await db.user_exists_sql(
        message.from_user.id
    ) and not await db.teachers_exists_sql(message.from_user.id):
        if message.chat.type == "private":
            await message.answer("❗️Нажміть кнопку реєстрації❗️", reply_markup=kb_start)
        else:
            await message.answer("❗️Перейдіть у бота та зареєструйтесь❗️")


# ===========================Змінити групу============================
async def view_calls(message: types.Message):
    db = await Database.setup()
    await stats_schedule_add("Розклад дзвінків ⌚️", 1)
    if (
        await db.user_exists_sql(message.from_user.id)
        or message.from_user.id == super_admin_admin
        or super_admin_ura == message.from_user.id
        or await db.teachers_exists_sql(message.from_user.id)
    ):
        check, value, date = await db.see_calls_sql()
        if not check:
            await message.answer("☹️Розклад дзвінків ще не додано☹️")
        elif check:
            await db.see_calls_sql()
            await message.answer_photo(value, date)
    elif not await db.user_exists_sql(
        message.from_user.id
    ) and not await db.teachers_exists_sql(message.from_user.id):
        if message.chat.type == "private":
            await message.answer("❗️Нажміть кнопку реєстрації❗️", reply_markup=kb_start)
        else:
            await message.answer("❗️Перейдіть у бота та зареєструйтесь❗️")


# ===========================Змінити групу============================
async def delete_user(message: types.Message):
    db = await Database.setup()
    if await db.user_exists_sql(message.from_user.id):
        if await db.admin_exists_sql(message.from_user.id):
            await db.delete_users_sql(message.from_user.id)
            await message.answer("🙂Зареєструйтесь знову🙂", reply_markup=kb_start_admin)
        else:
            await db.delete_users_sql(message.from_user.id)
            await message.answer("🙂Зареєструйтесь знову🙂", reply_markup=kb_start)
    elif await db.teachers_exists_sql(message.from_user.id):
        if await db.admin_exists_sql(message.from_user.id):
            await db.delete_teachers_sql(message.from_user.id)
            await message.answer("🙂Зареєструйтесь знову🙂", reply_markup=kb_start_admin)
        else:
            await db.delete_teachers_sql(message.from_user.id)
            await message.answer("🙂Зареєструйтесь знову🙂", reply_markup=kb_start)
    elif not await db.user_exists_sql(
        message.from_user.id
    ) and not await db.teachers_exists_sql(message.from_user.id):
        if message.chat.type == "private":
            await message.answer(
                "🌚Ви і так не зареєстрованні\nНажміть кнопку реєстрації",
                reply_markup=kb_start,
            )
        else:
            await message.answer(
                "🌚Ви і так не зареєстрованні\nПерейдіть у бота та зареєструйтесь"
            )


# =========================== Дріб ===========================
async def fraction(message: types.Message):
    await stats_schedule_add("Ч/З тиждень ✏️", 1)
    delta = datetime.timedelta(hours=2, minutes=0)
    todays = datetime.datetime.now(datetime.timezone.utc) + delta
    days = int(todays.strftime("%d"))
    years = int(todays.strftime("%y"))
    mouth = int(todays.strftime("%m"))
    today = datetime.date(year=years, month=mouth, day=days)
    week_number = today.isocalendar()[1]
    if week_number % 2 == 0:
        await message.answer("Цей тиждень - <b>знаменник</b> 🫡", parse_mode="HTML")
    elif week_number % 2 != 0:
        await message.answer("Цей тиждень - <b>чисельник</b> 🫡", parse_mode="HTML")


# =========================== Тривога ===========================
async def alert(message: types.Message):
    await stats_schedule_add("Тривоги ⚠️", 1)
    all_alerts, check = await alert_func()
    await message.answer(
        all_alerts + "\n" + "<a href='https://alerts.in.ua/'>Дані з сайту</a>",
        parse_mode="HTML",
        disable_web_page_preview=True,
    )


# ===========================Пустий хендлер============================
async def all_text(message: types.Message):
    db = await Database.setup()
    if await db.admin_exists_sql(message.from_user.id) and message.text == "Адмін 🔑":
        await message.answer("Адмінська частина", reply_markup=kb_admin)
    else:
        if message.chat.type == "private":
            await message.answer(
                "Незнаю такої команди\nНатисни /start і використовуй\nклавіатуру з кнопками знизу"
            )


text = {
    "view_coupes": [
        "Розклад пар 👀",
        "Розклад занять 👀",
        "який розклад?",
        "розклад",
        "пари",
        "Розклад пар",
        "Розклад занять",
        "coupes" "які завтра пари",
        "які пари",
        "які завтра пари?",
        "які пари?",
        "Які завтра пари?",
        "Яка перша пара завтра?",
        "Розклад на завтра?",
        "Які пари будуть на завтра?",
    ],
    "view_calls": ["Розклад дзвінків ⌚️", "Розклад дзвінків", "дзвінки"],
    "delete_user": ["Вийти 🚫", "Змінити групу 🚫"],
    "fraction": [
        "Ч/З тиждень ✏️",
        "чз",
        "Ч/З",
        "Ч/З тиждень",
        "чисельник",
        "знаменник",
        "який тиждень",
    ],
    "alert": ["Тривоги ⚠️", "Тривога", "alert", "тривога є?"],
}


# ===========================реєстратор============================
def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(
        view_coupes, Text(ignore_case=True, equals=text["view_coupes"])
    )
    dp.register_message_handler(
        view_calls, Text(ignore_case=True, equals=text["view_calls"])
    )
    dp.register_message_handler(delete_user, text=["Вийти 🚫", "Змінити групу 🚫"])
    dp.register_message_handler(
        fraction, Text(ignore_case=True, equals=text["fraction"])
    )
    dp.register_message_handler(alert, Text(ignore_case=True, equals=text["alert"]))
    dp.register_message_handler(all_text)
