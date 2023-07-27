from aiogram import F, Router, types

from data_base import Database
from keyboards import *

router = Router()




# ===========================Статистика 🧮============================
@router.callback_query(F.data == "Статистика 🧮")
async def stats_all_query(query: types.CallbackQuery):
    db = await Database.setup()
    value_user = await db.count_user_sql()
    value_student = await db.count_student_sql()
    value_teacher = await db.count_teacher_sql()
    stats = (
        f"📊 <b>Статистика користувачів :</b>\n"
        f" • Загальна к-сть користувачів : {value_user}\n\n"
        f" • Кількість студентів у боті : {value_student}\n"
        f" • Кількість викладачів у боті : {value_teacher}"
    )

    error = (
        "На жаль, статистика не змінилася.\n"
        "Чому б не запропонувати\n"
        "бота своїм одногрупникам? 😋"
    )

    try:
        await query.message.edit_text(text=stats, reply_markup=await update_kb(), parse_mode="HTML")
    except:
        await query.answer(text=error, show_alert=True,)
