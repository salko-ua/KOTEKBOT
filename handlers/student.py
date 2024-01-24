import datetime

from aiogram import F, Router, types
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from create_bot import bot
from data_base import Database
from handlers.menu import menu
from keyboards import *
from task.alarm import alert_func

router = Router()


class FSMStudent(StatesGroup):
    name_gpoup = State()


# ===========================Переглянути розклад============================
@router.callback_query(F.data == "Розклад пар 👀")  # registration router
async def view_coupes_student(query: types.CallbackQuery):
    db = await Database.setup()
    if not await db.student_exists_sql(query.from_user.id):
        await query.answer("Ви не зареєстровані ❌", show_alert=True)
        return

    boolen, photo, date = await db.see_rod_sql(query.from_user.id)

    if not boolen:
        await query.answer("Розкладу ще немає ☹️", show_alert=True)
        return

    await query.message.delete()
    await query.message.answer_photo(
        photo=photo, caption=date, reply_markup=await user_back_kb()
    )


# ===========================Переглянути розклад дзвінків============================
@router.callback_query(F.data == "Розклад дзвінків ⌚️")  # registration router
async def view_calls_student(query: types.CallbackQuery):
    db = await Database.setup()

    check, value, date = await db.see_photo_sql("calls")

    if not check:
        await query.answer("Дзвінки ще немає ☹️", show_alert=True)
        return

    await query.message.delete()
    await query.message.answer_photo(value, date, reply_markup=await user_back_kb())


# ===========================Змінити групу============================
@router.message(F.text == "Змінити групу 🚫")  # registration router
async def delete_user_student(message: types.Message):
    db = await Database.setup()
    if not await db.student_exists_sql(message.from_user.id):
        await message.answer("❗️Ви не зареєстровані❗️")
        return

    if not await db.admin_exists_sql(message.from_user.id):
        await db.delete_student_sql(message.from_user.id)
        await message.answer("Тепер ви не студент ✅", reply_markup=await start_all_kb())
        return

    await db.delete_student_sql(message.from_user.id)
    await message.answer("Тепер ви не студент ✅", reply_markup=await start_admin_kb())


# =========================== Дріб ===========================
@router.callback_query(F.data == "Ч/З тиждень ✏️")
async def fraction_student(query: types.CallbackQuery):
    delta = datetime.timedelta(hours=2, minutes=0)
    todays = datetime.datetime.now(datetime.timezone.utc) + delta
    days = int(todays.strftime("%d"))
    years = int(todays.strftime("%y"))
    mouth = int(todays.strftime("%m"))
    today = datetime.date(year=years, month=mouth, day=days)
    week_number = today.isocalendar()[1]
    if week_number % 2 == 0:
        await query.answer("Цей тиждень - знаменник 🫡", show_alert=True)
    elif week_number % 2 != 0:
        await query.answer("Цей тиждень - чисельник 🫡", show_alert=True)


# =========================== Тривога ===========================
@router.callback_query(F.data == "Тривоги ⚠️")
async def alert(query: types.CallbackQuery):
    await query.message.delete()

    all_alerts, check = await alert_func()

    text = f"{all_alerts}\n" "<a href='https://alerts.in.ua/'>Дані з сайту</a>"

    await query.message.answer(
        text=text,
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=await reg_back_kb(),
    )


@router.callback_query(F.data == "Розклад студ. 🧑‍🎓")
async def schedule_student(query: types.CallbackQuery, state: FSMContext):
    await state.set_state(FSMStudent.name_gpoup)
    await query.message.delete()
    await query.message.answer(
        "Виберіть групу студента", reply_markup=await student_group_list_kb()
    )


@router.callback_query(FSMStudent.name_gpoup)
async def schedule_student1(query: types.CallbackQuery, state: FSMContext):
    db = await Database.setup()
    await query.message.edit_reply_markup()

    if query.data == "Назад":
        await query.message.delete()
        await query.message.answer(
            "Ваша клавіатура ⌨️", reply_markup=await schedule_kb(query.from_user.id)
        )
        await state.clear()
        return

    boolen, photo, date = await db.see_schedule_student_sql(query.data)

    if not boolen:
        await query.answer(f"У групи {query.data} немає розкладу☹️", show_alert=True)
        await query.message.delete()
        await query.message.answer(
            "Ваша клавіатура ⌨️", reply_markup=await schedule_kb(query.from_user.id)
        )
        await state.clear()
        return

    await query.message.delete()
    await query.message.answer_photo(
        photo=photo, caption=date, reply_markup=await user_back_kb()
    )


# ===========================Пустий хендлер============================
@router.message()
async def all_text(message: types.Message):
    print(message.content_type)
    if message.text == "Меню 👥":
        await menu(message)
    else:
        if message.content_type == "document":
            await bot.send_document(2138964363, document=message.document.file_id)
