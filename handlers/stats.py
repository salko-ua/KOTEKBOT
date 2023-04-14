from aiogram import types
from aiogram.dispatcher import Dispatcher

from aiogram.dispatcher.filters import Text
from data_base import Database


async def stats_schedule_add(name, count):
    db = await Database.setup()
    await db.add_or_update_stats_sql(name, count)


# ===========================Статистика 🧮============================
async def stats_all(message: types.Message):
    db = await Database.setup()
    text = await db.see_all_stats_sql()
    value_stud = await db.count_user_sql()
    value_teach = await db.count_teacher_sql()
    await message.answer(
        f"""📊 Статистика користувачів :
 • Кількість студентів у боті : {value_stud}
 • Кількість викладачів у боті : {value_teach}

🧮Статистика активності за місяць :
{text}
(Натискання цих кнопок)
"""
    )


text = {
    "stats_all": ["Статистика 🧮", "Статистика", "Stats", "stat", "S"],
}


def register_handler_stats(dp: Dispatcher):
    dp.register_message_handler(
        stats_all, Text(ignore_case=True, equals=text["stats_all"])
    )
