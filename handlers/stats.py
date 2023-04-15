from aiogram import types
from aiogram.dispatcher import Dispatcher
from keyboards import *
from aiogram.dispatcher.filters import Text
from data_base import Database


async def stats_schedule_add(name, count):
    db = await Database.setup()
    await db.add_or_update_stats_sql(name, count)


# ===========================Статистика 🧮============================
async def stats_all(message: types.Message):
    await stats_schedule_add("Статистика 🧮", 1)
    db = await Database.setup()
    always, month, week = await db.see_all_stats_sql()
    value_stud = await db.count_user_sql()
    value_teach = await db.count_teacher_sql()
    await message.answer(
f"""📊 <b>Статистика користувачів :</b>
 • Кількість студентів у боті : {value_stud}
 • Кількість викладачів у боті : {value_teach}

🧮<b>Загальна статистика активності :</b>
{always}
(Натискання цих кнопок)
""", reply_markup = inline_stats_kb_month, parse_mode="HTML")

async def stats_month(Query: types.CallbackQuery):
    db = await Database.setup()
    always, month, week = await db.see_all_stats_sql()
    value_stud = await db.count_user_sql()
    value_teach = await db.count_teacher_sql()
    await Query.message.edit_text(
f"""📊 <b>Статистика користувачів :</b>
 • Кількість студентів у боті : {value_stud}
 • Кількість викладачів у боті : {value_teach}

🧮<b>Статистика активності за місяць :</b>
{month}
(Натискання цих кнопок)
""", reply_markup = inline_stats_kb_week, parse_mode="HTML")

async def stats_week(Query: types.CallbackQuery):
    db = await Database.setup()
    always, month, week = await db.see_all_stats_sql()
    value_stud = await db.count_user_sql()
    value_teach = await db.count_teacher_sql()
    await Query.message.edit_text(
f"""📊 <b>Статистика користувачів :</b>
 • Кількість студентів у боті : {value_stud}
 • Кількість викладачів у боті : {value_teach}

🧮<b>Статистика активності за тиждень:</b>
{week}
(Натискання цих кнопок)
""", reply_markup = inline_stats_kb_always, parse_mode="HTML")

async def stats_all_inline(Query: types.CallbackQuery):
    db = await Database.setup()
    always, month, week = await db.see_all_stats_sql()
    value_stud = await db.count_user_sql()
    value_teach = await db.count_teacher_sql()
    await Query.message.edit_text(
f"""📊 <b>Статистика користувачів :</b>
 • Кількість студентів у боті : {value_stud}
 • Кількість викладачів у боті : {value_teach}

🧮<b>Загальна статистика активності :</b>
{always}
(Натискання цих кнопок)
""", reply_markup = inline_stats_kb_month, parse_mode="HTML")




text = {
    "stats_all": ["Статистика 🧮", "Статистика", "Stats", "stat", "S"],
}


def register_handler_stats(dp: Dispatcher):
    dp.register_message_handler(
        stats_all, Text(ignore_case=True, equals=text["stats_all"])
    )
    dp.register_callback_query_handler(stats_month, text = "2")
    dp.register_callback_query_handler(stats_all_inline, text = "1")
    dp.register_callback_query_handler(stats_week, text = "3")