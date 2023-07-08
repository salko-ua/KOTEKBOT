from aiogram import Router, types
from aiogram.filters import Command
from aiogram.filters.text import Text

router = Router()


@router.message(Command(commands=["start"]))
async def command_start_handler(message: types.Message) -> None:
    await message.answer(f"Hello, <b>{message.from_user.full_name}!</b>")


import datetime

from keyboards import *
from aiogram import types
from handlers.menu import menu
from data_base import Database
from task.alarm import alert_func
from config import SUPER_ADMIN
from handlers.text_handlers import *


# ===========================Переглянути розклад============================
@router.message(
    Text(text=student_text["view_coupes"], ignore_case=True)
)  # registration router
async def view_coupes(message: types.Message):
    db = await Database.setup()
    if await db.student_exists_sql(message.from_user.id):
        boolen, photo, date = await db.see_rod_sql(message.from_user.id)
        if boolen:
            await message.answer_photo(photo, date)
        elif not boolen:
            await message.answer("☹️Розкладу для вашої групи ще немає...☹️")
    elif await db.teacher_exists_sql(message.from_user.id):
        boolen, photo, date = await db.see_rod_t_sql(message.from_user.id)
        if boolen:
            await message.answer_photo(photo, date)
        elif not boolen:
            await message.answer("☹️Розкладу для ваc ще немає...☹️")
    elif not await db.student_exists_sql(
        message.from_user.id
    ) and not await db.teacher_exists_sql(message.from_user.id):
        if message.chat.type == "private":
            await message.answer(
                "❗️Нажміть кнопку реєстрації❗️", reply_markup=await start_all_kb()
            )
        else:
            await message.answer("❗️Перейдіть у бота та зареєструйтесь❗️")


# ===========================Змінити групу============================
@router.message(
    Text(text=student_text["view_calls"], ignore_case=True)
)  # registration router
async def view_calls(message: types.Message):
    db = await Database.setup()
    if (
        await db.student_exists_sql(message.from_user.id)
        or await db.teacher_exists_sql(message.from_user.id)
        or message.from_user.id in SUPER_ADMIN
    ):
        check, value, date = await db.see_photo_sql('calls')
        if not check:
            await message.answer("☹️Розклад дзвінків ще не додано☹️")
        elif check:
            await message.answer_photo(value, date)
    elif not await db.student_exists_sql(
        message.from_user.id
    ) and not await db.teacher_exists_sql(message.from_user.id):
        if message.chat.type == "private":
            await message.answer(
                "❗️Нажміть кнопку реєстрації❗️", reply_markup=await start_all_kb()
            )
        else:
            await message.answer("❗️Перейдіть у бота та зареєструйтесь❗️")


# ===========================Змінити групу============================
@router.message(
    Text(text=student_text["delete_user"], ignore_case=True)
)  # registration router
async def delete_user(message: types.Message):
    db = await Database.setup()
    if await db.student_exists_sql(message.from_user.id):
        if await db.admin_exists_sql(message.from_user.id):
            await db.delete_student_sql(message.from_user.id)
            await message.answer(
                "🙂Зареєструйтесь знову🙂", reply_markup=await start_admin_kb()
            )
        else:
            await db.delete_student_sql(message.from_user.id)
            await message.answer(
                "🙂Зареєструйтесь знову🙂", reply_markup=await start_all_kb()
            )
    elif await db.teacher_exists_sql(message.from_user.id):
        if await db.admin_exists_sql(message.from_user.id):
            await db.delete_teacher_sql(message.from_user.id)
            await message.answer(
                "🙂Зареєструйтесь знову🙂", reply_markup=await start_admin_kb()
            )
        else:
            await db.delete_teacher_sql(message.from_user.id)
            await message.answer(
                "🙂Зареєструйтесь знову🙂", reply_markup=await start_all_kb()
            )
    elif not await db.student_exists_sql(
        message.from_user.id
    ) and not await db.teacher_exists_sql(message.from_user.id):
        if message.chat.type == "private":
            await message.answer(
                "🌚Ви і так не зареєстрованні\nНажміть кнопку реєстрації",
                reply_markup=await start_all_kb(),
            )
        else:
            await message.answer(
                "🌚Ви і так не зареєстрованні\nПерейдіть у бота та зареєструйтесь"
            )


# =========================== Дріб ===========================
@router.message(
    Text(text=student_text["fraction"], ignore_case=True)
)  # registration router
async def fraction(message: types.Message):
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
@router.message(
    Text(text=student_text["alert"], ignore_case=True)
)  # registration router
async def alert(message: types.Message):
    all_alerts, check = await alert_func()
    await message.answer(
        all_alerts + "\n" + "<a href='https://alerts.in.ua/'>Дані з сайту</a>",
        parse_mode="HTML",
        disable_web_page_preview=True,
    )


# ===========================Пустий хендлер============================
@router.message()
async def all_text(message: types.Message):
    db = await Database.setup()
    if await db.admin_exists_sql(message.from_user.id) and message.text == "Адмін 🔑":
        await message.answer("Адмінська частина", reply_markup=await admin_kb())
    else:
        if message.text == "Меню 👥":
            await menu(message)
