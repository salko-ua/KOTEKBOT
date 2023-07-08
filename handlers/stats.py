from keyboards import *
from aiogram import types, Router
from data_base import Database

from aiogram.filters import Text

router = Router()


text = {
    "stats_all": ["Статистика 🧮", "Статистика", "Stats", "stat", "S"],
}


# ===========================Статистика 🧮============================
@router.message(Text(text=text["stats_all"], ignore_case=True))
async def stats_all(message: types.Message):
    db = await Database.setup()
    value_user = await db.count_user_sql()
    value_student = await db.count_student_sql()
    value_teacher = await db.count_teacher_sql()
    await message.answer(
        f"""📊 <b>Статистика користувачів :</b>
 • Загальна к-сть користувачів : {value_user}

 • Кількість студентів у боті : {value_student}
 • Кількість викладачів у боті : {value_teacher}
""",
        reply_markup=await update_kb(),
        parse_mode="HTML",
    )


@router.callback_query(Text("update"))
async def stats_all_query(query: types.CallbackQuery):
    db = await Database.setup()
    value_user = await db.count_user_sql()
    value_student = await db.count_student_sql()
    value_teacher = await db.count_teacher_sql()
    try:
        await query.message.edit_text(
            f"""📊 <b>Статистика користувачів :</b>
 • Загальна к-сть користувачів : {value_user}

 • Кількість студентів у боті : {value_student}
 • Кількість викладачів у боті : {value_teacher}
""",
            reply_markup=await update_kb(),
            parse_mode="HTML",
        )
    except:
        await query.answer(
            "На жаль, статистика не змінилася.\nЧому б не запропонувати\nбота своїм одногрупникам? 😋",
            show_alert=True,
        )
