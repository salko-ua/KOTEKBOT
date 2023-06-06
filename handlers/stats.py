from keyboards import *
from aiogram import types
from data_base import Database

from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import MessageNotModified


# ===========================Статистика 🧮============================
async def stats_all(message: types.Message):
    db = await Database.setup()
    value_stud = await db.count_user_sql()
    value_teach = await db.count_teacher_sql()
    await message.answer(
f"""📊 <b>Статистика користувачів :</b>
 • Кількість студентів у боті : {value_stud}
 • Кількість викладачів у боті : {value_teach}
""", reply_markup = update_kb, parse_mode="HTML")

async def stats_all_query(query: types.CallbackQuery):
    db = await Database.setup()
    value_stud = await db.count_user_sql()
    value_teach = await db.count_teacher_sql()
    try:
        await query.message.edit_text(
f"""📊 <b>Статистика користувачів :</b>
 • Кількість студентів у боті : {value_stud}
 • Кількість викладачів у боті : {value_teach}
""", reply_markup = update_kb, parse_mode="HTML")
    except MessageNotModified:
        await query.answer("На жаль, статистика не змінилася.\nЧому б не запропонувати\nбота своїм одногрупникам? 😋", show_alert=True)



text = {
    "stats_all": ["Статистика 🧮", "Статистика", "Stats", "stat", "S"],
}


def register_handler_stats(dp: Dispatcher):
    dp.register_message_handler(
        stats_all, Text(ignore_case=True, equals=text["stats_all"])
    )
    dp.register_callback_query_handler(stats_all_query, text="update")

