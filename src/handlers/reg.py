import aiogram.types
from aiogram import F, Router, types
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from src.keyboards import *
from src.data_base import Database
from src.utils import password_for_admin

router = Router()


class FSMReg(StatesGroup):
    student_reg = State()
    password_reg = State()
    reply_reg = State()


@router.message(F.text == "Реєстрація 📝")
@router.message(F.text == "Студент 👨‍🎓")
@router.message(F.text == "Панель 📁")
# ===========================Реєстрація ⚙️============================
async def registration(message: types.Message, state: FSMContext) -> None:
    db = await Database.setup()
    await message.delete()

    if await db.student_exists(message.from_user.id):
        await message.answer(text="Ваша клавіатура ⌨️", reply_markup=student_kb())

    elif await db.admin_exists(message.from_user.id):
        await message.answer(text="Оберіть ⬇️", reply_markup=reg_choice_kb())
        await state.set_state(FSMReg.reply_reg)

    else:
        await message.answer(text="Оберіть ⬇️", reply_markup=reg_choice_kb())
        await state.set_state(FSMReg.reply_reg)


@router.callback_query(FSMReg.reply_reg)
async def reg(query: types.CallbackQuery, state: FSMContext) -> None:
    await state.update_data(id=query.message.message_id)

    if query.data == "Адміністратор 🔐":
        await state.set_state(FSMReg.password_reg)
        await query.message.edit_text("🔒 Введіть пароль 🔑")

    elif query.data == "Студент 👩‍🎓":
        await state.set_state(FSMReg.student_reg)
        message = await query.message.edit_text(
            "⬇️ Виберіть групу", reply_markup=await student_group_list_kb()
        )
        await state.update_data(message=message)


@router.message(FSMReg.password_reg)
async def reg_admin(message: types.Message, state: FSMContext) -> None:
    db = await Database.setup()
    data = await state.get_data()
    message_id = data["id"]

    username = message.from_user.username
    user_id = message.from_user.id
    chat_id = message.chat.id

    await message.delete()
    await message.bot.delete_message(message_id=message_id, chat_id=chat_id)

    if not message.text == password_for_admin():
        await message.answer(text="Пароль невірний ☹️")
        await state.clear()
        return

    if not await db.admin_exists(message.from_user.id):
        await db.add_admin(user_id, username)
        await message.answer(
            text="Реєстрація завершена ✅", reply_markup=start_admin_kb()
        )
        await state.clear()
        return

    await message.answer(text="Ви зареєстровані адміном ✅", reply_markup=hide_kb())
    await state.clear()


@router.callback_query(FSMReg.student_reg)
async def reg_student(query: types.CallbackQuery, state: FSMContext) -> None:
    db = await Database.setup()
    data = await state.get_data()
    message_id: aiogram.methods.edit_message_text.EditMessageText = data["message"]
    group_student = query.data

    await state.clear()

    if query.data == "Назад":
        await query.message.edit_text("Оберіть ⬇️")
        await query.message.edit_reply_markup(reply_markup=reg_choice_kb())
        await state.set_state(FSMReg.reply_reg)
        return

    if not await db.student_group_exists(group_student):
        await query.message.bot.delete_message(
            chat_id=query.message.chat.id, message_id=message_id.message_id
        )
        await query.answer(
            text=f"Групу {group_student} не знайдено",
            show_alert=True,
            reply_markup=start_student_kb(),
        )
        return

    await db.add_student(user_id=query.from_user.id, group_student=group_student)
    await query.message.answer(
        text="✅ Реєстрація завершена ✅", reply_markup=start_student_kb()
    )
    await query.message.delete()
