# import
from random import choice

import asyncache
import cachetools

# from import
from aiogram import F, Router, types
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from src.data_base import Database
from src.keyboards import *

router = Router()


# =========Класс машини стану=========
class FSMReg(StatesGroup):
    student_reg = State()
    password_reg = State()
    reply_reg = State()


@asyncache.cached(cachetools.TTLCache(1, 120))
async def password_for_admin():
    password = ""
    for x in range(8):
        password += choice(list("1234567890ABCDEFGHIGKLMNOPQRSTUVYXWZ"))
    return password


@router.message(F.text == "Реєстрація 📝")
@router.message(F.text == "Студент 👨‍🎓")
@router.message(F.text == "Панель 📁")
# ===========================Реєстрація ⚙️============================
async def registration(message: types.Message, state: FSMContext) -> None:
    db = await Database.setup()
    await message.delete()

    if await db.student_exists(message.from_user.id):
        await message.answer("Ваша клавіатура ⌨️", reply_markup=await student_kb())

    elif await db.admin_exists(message.from_user.id):
        await message.answer("Оберіть ⬇️", reply_markup=await reg_choice_kb())
        await state.set_state(FSMReg.reply_reg)

    else:
        await message.answer("Оберіть ⬇️", reply_markup=await reg_choice_kb())
        await state.set_state(FSMReg.reply_reg)


@router.callback_query(FSMReg.reply_reg)
async def reg(query: types.CallbackQuery, state: FSMContext) -> None:
    await state.update_data(id=query.message.message_id)

    if query.data == "Адміністратор 🔐":
        await state.set_state(FSMReg.password_reg)
        await query.message.edit_text("🔒 Введіть пароль 🔑")

    elif query.data == "Студент 👩‍🎓":
        await state.set_state(FSMReg.student_reg)
        await query.message.edit_text(
            "⬇️ Виберіть групу", reply_markup=await student_group_list_kb()
        )


@router.message(FSMReg.password_reg)
async def regAdmin(message: types.Message, state: FSMContext) -> None:
    db = await Database.setup()
    data = await state.get_data()
    message_id = data["id"]

    username = message.from_user.username
    user_id = message.from_user.id
    chat_id = message.chat.id

    await message.delete()
    await message.bot.delete_message(message_id=message_id, chat_id=chat_id)

    if not message.text == await password_for_admin():
        await message.answer("Пароль невірний ☹️")
        await state.clear()
        return

    if not await db.admin_exists(message.from_user.id):
        await db.add_admin(user_id, username)
        await message.answer(
            "Реєстрація завершена ✅", reply_markup=await start_admin_kb()
        )
        await state.clear()
        return

    await message.answer("Ви зареєстровані адміном ✅", reply_markup=await hide_kb())
    await state.clear()


@router.callback_query(FSMReg.student_reg)
async def regStudent(query: types.CallbackQuery, state: FSMContext) -> None:
    db = await Database.setup()

    group_student = query.data

    await state.clear()

    if query.data == "Назад":
        await query.message.edit_text("Оберіть ⬇️")
        await query.message.edit_reply_markup(reply_markup=await reg_choice_kb())
        await state.set_state(FSMReg.reply_reg)
        return

    await db.add_student(user_id=query.from_user.id, group_student=group_student)
    await query.message.answer(
        "✅ Реєстрація завершена ✅", reply_markup=await start_student_kb()
    )
    await query.message.delete()