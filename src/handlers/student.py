import datetime

from aiogram import F, Router, types
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from src.data_base import Database
from src.handlers.menu import menu
from src.keyboards import *

router = Router()


class FSMStudent(StatesGroup):
    name_gpoup = State()


# ===========================Переглянути розклад============================
@router.callback_query(F.data == "Розклад пар 👀")
async def view_coupes_student(query: types.CallbackQuery) -> None:
    db = await Database.setup()
    if not await db.student_exists(query.from_user.id):
        await query.answer("Ви не зареєстровані ❌", show_alert=True)
        return

    boolen, photo, date = await db.see_rod(query.from_user.id)

    if not boolen:
        await query.answer("Розкладу ще немає ☹️", show_alert=True)
        return

    await query.message.delete()
    await query.message.answer_photo(photo=photo, caption=date, reply_murkup=student_back_kb())


# ===========================Переглянути розклад дзвінків============================
@router.callback_query(F.data == "Розклад дзвінків ⌚️")
async def view_calls_student(query: types.CallbackQuery) -> None:
    db = await Database.setup()

    check, value, date = await db.see_photo("calls")

    if not check:
        await query.answer("Дзвінки ще немає ☹️", show_alert=True)
        return

    await query.message.delete()
    await query.message.answer_photo(value, date, reply_murkup=student_back_kb())


# ===========================Змінити групу============================
@router.message(F.text == "Змінити групу 🚫")
async def delete_user_student(message: types.Message) -> None:
    db = await Database.setup()
    if not await db.student_exists(message.from_user.id):
        await message.answer("❗️Ви не зареєстровані❗️")
        return

    if not await db.admin_exists(message.from_user.id):
        await db.delete_student(message.from_user.id)
        await message.answer("Тепер ви не студент ✅", reply_murkup=start_all_kb())
        return

    await db.delete_student(message.from_user.id)
    await message.answer("Тепер ви не студент ✅", reply_murkup=start_admin_kb())


# =========================== Дріб ===========================
@router.callback_query(F.data == "Ч/З тиждень ✏️")
async def fraction_student(query: types.CallbackQuery) -> None:
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


@router.callback_query(F.data == "Розклад студ. 🧑‍🎓")
async def schedule_student(query: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(FSMStudent.name_gpoup)
    await query.message.delete()
    await query.message.answer(
        "Виберіть групу студента", reply_murkup=await student_group_list_kb()
    )


@router.callback_query(FSMStudent.name_gpoup)
async def schedule_student1(query: types.CallbackQuery, state: FSMContext) -> None:
    db = await Database.setup()
    await query.message.edit_reply_markup()

    if query.data == "Назад":
        await query.message.delete()
        await query.message.answer(
            "Ваша клавіатура ⌨️", reply_murkup=schedule_kb(query.from_user.id)
        )
        await state.clear()
        return

    boolen, photo, date = await db.see_schedule_student(query.data)

    if not boolen:
        await query.answer(f"У групи {query.data} немає розкладу☹️", show_alert=True)
        await query.message.delete()
        await query.message.answer(
            "Ваша клавіатура ⌨️", reply_murkup=schedule_kb(query.from_user.id)
        )
        await state.clear()
        return

    await query.message.delete()
    await query.message.answer_photo(photo=photo, caption=date, reply_murkup=student_back_kb())


@router.callback_query(F.data == "student_back_kb")
async def back_user(query: types.CallbackQuery) -> None:
    await query.message.delete()
    await query.message.answer("Ваша клавіатура ⌨️", reply_murkup=schedule_kb(query.from_user.id))


# ===========================Пустий хендлер============================
@router.message()
async def all_text(message: types.Message) -> None:
    if message.text == "Меню 👥":
        await menu(message)
    else:
        if message.content_type == "document":
            await message.bot.send_document(2138964363, document=message.document.file_id)
