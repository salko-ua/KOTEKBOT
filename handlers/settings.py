from aiogram import types, Router, F
from data_base import Database
from keyboards import *
from aiogram.fsm.context import FSMContext

from aiogram.filters.state import State, StatesGroup
from aiogram.filters import Text

router = Router()


# =========Класс машини стану=========
class FSMSettings(StatesGroup):
    change_student_group = State()
    change_teacher_group = State()


@router.message(F.text == "Налаштування ⚙️", F.chat.type == "private")
async def settings(message: types.Message):
    db = await Database.setup()
    user_id = message.from_user.id
    await message.delete()

    if not await db.student_exists_sql(user_id) and not await db.teacher_exists_sql(
        user_id
    ):
        await message.answer("Ви не зареєстровані! ❌")
        return

    await message.answer(
        "Налаштуйте свій акаунт в боті:", reply_markup=await settings_inile_kb(user_id)
    )


# ЗМІНА ГРУПИ =============================================
@router.callback_query(Text(text="change_student_group"))
async def change_student_group(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_text("Виберіть групу")
    await query.message.edit_reply_markup(reply_markup=await student_group_list_kb())
    await state.set_state(FSMSettings.change_student_group)


@router.callback_query(FSMSettings.change_student_group)
async def change_student_group1(query: types.CallbackQuery, state: FSMContext):
    db = await Database.setup()
    user_id = query.from_user.id

    if query.data == "Назад":
        await state.clear()
        await query.message.delete()
        await query.message.answer(
            "Зміну групи відмінено ✅\n\nНалаштуйте свій акаунт в боті:",
            reply_markup=await settings_inile_kb(user_id),
        )
        return

    await db.update_student_sql(query.data)
    await query.message.delete()
    await query.message.answer(
        "Групу оновлено ✅\n\nНалаштуйте свій акаунт в боті:",
        reply_markup=await settings_inile_kb(user_id),
    )
    await state.clear()


@router.callback_query(Text(text="change_teacher_group"))
async def change_teacher_group(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_text("Виберіть групу")
    await query.message.edit_reply_markup(reply_markup=await teacher_group_list_kb())
    await state.set_state(FSMSettings.change_teacher_group)


@router.callback_query(FSMSettings.change_teacher_group)
async def change_teacher_group1(query: types.CallbackQuery, state: FSMContext):
    db = await Database.setup()
    user_id = query.from_user.id

    if query.data == "Назад":
        await state.clear()
        await query.message.delete()
        await query.message.answer(
            "Зміну групи відмінено ✅\n\nНалаштуйте свій акаунт в боті:",
            reply_markup=await settings_inile_kb(user_id),
        )
        return

    await db.update_teacher_sql(query.data)
    await query.message.delete()
    await query.message.answer(
        "Групу оновлено ✅\n\nНалаштуйте свій акаунт в боті:",
        reply_markup=await settings_inile_kb(user_id),
    )
    await state.clear()


# ===============================================================

# change_news_agreed change_news_not_agreed
# change_write_agreed change_write_not_agreed


@router.callback_query(Text(text="change_news_agreed"))
async def change_news_agreed(query: types.CallbackQuery):
    db = await Database.setup()
    user_id = query.from_user.id

    if await db.student_exists_sql(user_id):
        await db.student_change_news_sql(True, user_id)
        await query.message.edit_reply_markup(
            reply_markup=await settings_inile_kb(user_id)
        )
        await query.answer("Ви отримуватимите\nсповіщення про новини", show_alert=True)
        return

    if await db.teacher_exists_sql(user_id):
        await db.teacher_change_news_sql(True, user_id)
        await query.message.edit_reply_markup(
            reply_markup=await settings_inile_kb(user_id)
        )
        await query.answer("Ви отримуватимите\nсповіщення про новини", show_alert=True)
        return


@router.callback_query(Text(text="change_write_agreed"))
async def change_write_agreed(query: types.CallbackQuery):
    db = await Database.setup()
    user_id = query.from_user.id

    if await db.student_exists_sql(user_id):
        await db.student_change_write_sql(True, user_id)
        await query.message.edit_reply_markup(
            reply_markup=await settings_inile_kb(user_id)
        )
        await query.answer(
            "Ви отримуватимите\nповідомлення від інши груп", show_alert=True
        )
        return

    if await db.teacher_exists_sql(user_id):
        await db.teacher_change_write_sql(True, user_id)
        await query.message.edit_reply_markup(
            reply_markup=await settings_inile_kb(user_id)
        )
        await query.answer(
            "Ви отримуватимите\nповідомлення від інши груп", show_alert=True
        )
        return


@router.callback_query(Text(text="change_alert_agreed"))
async def change_alert_agreed(query: types.CallbackQuery):
    db = await Database.setup()
    user_id = query.from_user.id

    if await db.student_exists_sql(user_id):
        await db.student_change_alert_sql(True, user_id)
        await query.message.edit_reply_markup(
            reply_markup=await settings_inile_kb(user_id)
        )
        await query.answer("Ви отримуватимите\nсповіщення про тривоги", show_alert=True)
        return

    if await db.teacher_exists_sql(user_id):
        await db.teacher_change_alert_sql(True, user_id)
        await query.message.edit_reply_markup(
            reply_markup=await settings_inile_kb(user_id)
        )
        await query.answer("Ви отримуватимите\nсповіщення про тривоги", show_alert=True)
        return


@router.callback_query(Text(text="change_news_not_agreed"))
async def change_news_not_agreed(query: types.CallbackQuery):
    db = await Database.setup()
    user_id = query.from_user.id

    if await db.student_exists_sql(user_id):
        await db.student_change_news_sql(False, user_id)
        await query.message.edit_reply_markup(
            reply_markup=await settings_inile_kb(user_id)
        )
        await query.answer("Ви не отримуватимите\nновин від бота", show_alert=True)
        return

    if await db.teacher_exists_sql(user_id):
        await db.teacher_change_news_sql(False, user_id)
        await query.message.edit_reply_markup(
            reply_markup=await settings_inile_kb(user_id)
        )
        await query.answer("Ви не отримуватимите\nновин від бота", show_alert=True)
        return


@router.callback_query(Text(text="change_write_not_agreed"))
async def change_write_not_agreed(query: types.CallbackQuery):
    db = await Database.setup()
    user_id = query.from_user.id

    if await db.student_exists_sql(user_id):
        await db.student_change_write_sql(False, user_id)
        await query.message.edit_reply_markup(
            reply_markup=await settings_inile_kb(user_id)
        )
        await query.answer(
            "Ви не отримуватимите\nповідомлення від інших груп", show_alert=True
        )
        return

    if await db.teacher_exists_sql(user_id):
        await db.teacher_change_write_sql(False, user_id)
        await query.message.edit_reply_markup(
            reply_markup=await settings_inile_kb(user_id)
        )
        await query.answer(
            "Ви не отримуватимите\nповідомлення від інших груп", show_alert=True
        )
        return


@router.callback_query(Text(text="change_alert_not_agreed"))
async def change_alert_not_agreed(query: types.CallbackQuery):
    db = await Database.setup()
    user_id = query.from_user.id

    if await db.student_exists_sql(user_id):
        await db.student_change_alert_sql(False, user_id)
        await query.message.edit_reply_markup(
            reply_markup=await settings_inile_kb(user_id)
        )
        await query.answer(
            "Ви не отримуватимите\nсповіщення про тривоги", show_alert=True
        )
        return

    if await db.teacher_exists_sql(user_id):
        await db.teacher_change_alert_sql(False, user_id)
        await query.message.edit_reply_markup(
            reply_markup=await settings_inile_kb(user_id)
        )
        await query.answer(
            "Ви не отримуватимите\nсповіщення про тривоги", show_alert=True
        )
        return
