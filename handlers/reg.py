# import
import asyncache
import cachetools

# from import
from aiogram import types, Router, F
from data_base import Database
from random import choice
from keyboards import *

from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from handlers.menu import menu

from aiogram.filters import Text

from aiogram.filters.state import State, StatesGroup


router = Router()


# =========Класс машини стану=========
class FSMReg(StatesGroup):
    course_groupe_reg = State()
    teachers_reg = State()
    password_reg = State()
    reply_reg = State()


@asyncache.cached(cachetools.TTLCache(1, 120))
async def password_for_admin():
    password = ""
    for x in range(8):
        password += choice(list("1234567890ABCDEFGHIGKLMNOPQRSTUVYXWZ"))
    return password


@router.message(Text(text=["Реєстрація 📝", "Розклад 📅"], ignore_case=True))
# ===========================Реєстрація ⚙️============================
async def registration(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if await db.student_exists_sql(message.from_user.id):
        await message.answer("Ваша клавіатура ⌨️", reply_markup=await student_kb())

    elif await db.teacher_exists_sql(message.from_user.id):
        await message.answer("Ваша клавіатура ⌨️", reply_markup=await teacher_kb())

    elif await db.admin_exists_sql(message.from_user.id):
        await message.answer(
            "Виберіть тип акаунту ⬇️", reply_markup=await reg_choice_kb()
        )
        await state.set_state(FSMReg.reply_reg)
    else:
        await message.answer(
            "Виберіть тип акаунту ⬇️", reply_markup=await reg_choice_kb()
        )
        await state.set_state(FSMReg.reply_reg)


@router.message(FSMReg.reply_reg)
async def reg(message: types.Message, state: FSMContext):
    if message.text == "Меню 👥":
        await menu(message)
        await state.clear()
        return

    if message.text == "Адміністратор 🔐":
        await state.set_state(FSMReg.password_reg)
        await message.answer(
            "🔒 Введіть динамічний пароль 🔑", reply_markup=ReplyKeyboardRemove()
        )

    elif message.text == "Студент 👩‍🎓":
        await state.set_state(FSMReg.course_groupe_reg)
        await message.answer("⬇️ Виберіть групу", reply_markup=await reg_student_kb())

    elif message.text == "Викладач 👨‍🏫":
        await state.set_state(FSMReg.teachers_reg)
        await message.answer("⬇️ Виберіть нижче", reply_markup=await reg_teacher_kb())
    else:
        await message.answer(
            "☹️ Немає такої відповіді ☹️", reply_markup=await start_all_kb()
        )
        await state.clear()


@router.message(FSMReg.password_reg)
async def regAdmin(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if message.text == "Меню 👥":
        await menu(message)
        await state.clear()

    elif message.text == await password_for_admin():
        if await db.admin_exists_sql(message.from_user.id):
            await message.answer("Ви вже адмін", reply_markup=await start_admin_kb())
            await state.clear()
        else:
            username = message.from_user.username
            user_id = message.from_user.id
            await db.add_admin_sql(user_id, username)
            await message.answer(
                "✅ Реєстрація завершена ✅", reply_markup=await admin_kb()
            )
            await state.clear()
    else:
        await message.answer(
            "☹️ пароль неправильний ☹️", reply_markup=await start_all_kb()
        )
        await state.clear()


@router.message(FSMReg.course_groupe_reg)
async def regUser(message: types.Message, state: FSMContext):
    db = await Database.setup()
    group_student = message.text

    if message.text == "Меню 👥":
        await menu(message)
        await state.clear()

    elif await db.student_group_exists_sql(message.text):
        await db.add_student_sql(message.from_user.id, group_student)
        await state.clear()
        await message.answer(
            "✅ Реєстрація завершена ✅", reply_markup=await student_kb()
        )

    else:
        await message.answer(
            "☹️ Немає такої групи у списку☹️",
            reply_markup=await start_all_kb(),
        )
        await state.clear()


@router.message(FSMReg.teachers_reg)
async def regTeachers(message: types.Message, state: FSMContext):
    db = await Database.setup()
    user_id = message.from_user.id
    group_teacher = message.text

    if message.text == "Меню 👥":
        await menu(message)
        await state.clear()

    elif await db.teacher_group_exists_sql(message.text):
        await db.add_teacher_sql(user_id, group_teacher)
        await state.clear()
        await message.answer(
            "✅ Реєстрація завершена ✅", reply_markup=await teacher_kb()
        )

    else:
        await message.answer(
            "☹️ Немає такого вчителя у списку☹️", reply_markup=await start_all_kb()
        )
        await state.clear()
