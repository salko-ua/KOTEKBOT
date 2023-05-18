import datetime
import asyncio
import asyncache
import cachetools

from aiogram import types
from aiogram.dispatcher import Dispatcher
from config import super_admin_admin, super_admin_ura
from keyboards import *
from aiogram.dispatcher.filters import Text
import random as r
from create_bot import alerts_client
from handlers.stats import stats_schedule_add
from data_base import Database


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
@asyncache.cached(cachetools.TTLCache(1, 17))
async def alert_func():
    # Достаю список областей у яких повітряна тривога типу air_raid
    active_alerts = await alerts_client.get_active_alerts()
    filtered_alerts = active_alerts.filter(
        "location_type", "oblast", "alert_type", "air_raid"
    )

    # Достаю список назв областей у яких повітряна тривога
    count = len(filtered_alerts)
    all_alerts = f"🌍 Області з тривогою({count} з 26):\n\n"
    list_alerts_oblast_title = []
    for title in filtered_alerts:
        list_alerts_oblast_title.append(title.location_title)
    list_alerts_oblast_title.sort()

    #Перевірка чи є у Волинській області тривога?
    if "Волинська область" in list_alerts_oblast_title:
        our_oblast = True
    else:
        our_oblast = False

    # Області які будуть на першому місці
    need_oblast_title = [
        "Тернопільська область",
        "Івано-Франківська область",
        "Хмельницька область",
        "Чернівецька область",
        "Закарпатська область",
        "Львівська область",
        "Рівненська область",
        "Волинська область",
    ]
    # список у якому будуть області які нам підходять за списком вище і у них тривога
    need_oblast_title_list_new = []
    # Цикл пеоевірки через помилку
    for j in range(0, len(need_oblast_title)):
        try:
            list_alerts_oblast_title.index(need_oblast_title[j])
            list_alerts_oblast_title.remove(need_oblast_title[j])
            need_oblast_title_list_new.insert(0, need_oblast_title[j])
        except ValueError:
            await asyncio.sleep(0.05)
    # Роблю гарне повідомлення
    if len(need_oblast_title_list_new) == 0 and len(list_alerts_oblast_title) == 0:
        all_alerts += f" - Тривоги відсутні 🟢\n"
    else:
        if len(need_oblast_title_list_new) == 0:
            all_alerts += f"Західні області :\n • Немає\n\n"
        else:
            all_alerts += f"Західні області :\n"
            for alert in need_oblast_title_list_new:
                all_alerts += " • " + alert + "\n"
            all_alerts += "\n"
        if len(list_alerts_oblast_title) == 0:
            all_alerts += f"Інші області :\n • Немає"
        else:
            all_alerts += f"Інші області :\n"
            for alert in list_alerts_oblast_title:
                all_alerts += " • " + alert + "\n"
    return all_alerts, our_oblast


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
                "Незнаю такої командм\nНатисни /start і використовуй\nклавіатуру з кнопками знизу"
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
