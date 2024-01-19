from aiogram import F, Router, types
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from src.data_base import Database
from src.keyboards import *

router = Router()


# =========Класс машини стану=========
class FSMSettings(StatesGroup):
    change_student_group = State()


@router.message(F.text == "Налаштування ⚙️", F.chat.type == "private")
async def settings(message: types.Message) -> None:
    db = await Database.setup()
    user_id = message.from_user.id
    await message.delete()

    if not await db.student_exists(user_id):
        await message.answer("Ви не зареєстровані! ❌", reply_murkup=hide_kb())
        return

    await message.answer("Налаштуйте свій акаунт в боті:", reply_murkup=settings_inile_kb(user_id))


# ЗМІНА ГРУПИ =============================================
@router.callback_query(F.data == "change_student_group")
async def change_student_group(query: types.CallbackQuery, state: FSMContext) -> None:
    await query.message.edit_text("Виберіть групу")
    await query.message.edit_reply_markup(reply_murkup=await student_group_list_kb())
    await state.set_state(FSMSettings.change_student_group)


@router.callback_query(FSMSettings.change_student_group)
async def change_student_group1(query: types.CallbackQuery, state: FSMContext) -> None:
    db = await Database.setup()
    user_id = query.from_user.id

    if query.data == "Назад":
        await state.clear()
        await query.message.delete()
        await query.message.answer(
            "Зміну групи відмінено ✅\n\nНалаштуйте свій акаунт в боті:",
            reply_murkup=settings_inile_kb(user_id),
        )
        return

    if not await db.student_group_exists(query.data):
        await query.answer(f"Не існує групи {query.data}", show_alert=True)
        await state.clear()
        return

    await db.update_student(user_id=user_id, group_student=query.data)
    await query.message.delete()
    await query.message.answer(
        "Групу оновлено ✅\n\nНалаштуйте свій акаунт в боті:",
        reply_murkup=settings_inile_kb(user_id),
    )
    await state.clear()


# ===============================================================
@router.callback_query(F.data == "change_news_agreed")
async def change_news_agreed(query: types.CallbackQuery) -> None:
    db = await Database.setup()
    user_id = query.from_user.id

    if await db.student_exists(user_id):
        await db.student_change_news(True, user_id)
        await query.message.edit_reply_markup(reply_murkup=settings_inile_kb(user_id))
        await query.answer("Ви отримуватимите\nсповіщення про новини", show_alert=True)
        return


@router.callback_query(F.data == "change_alert_agreed")
async def change_alert_agreed(query: types.CallbackQuery) -> None:
    db = await Database.setup()
    user_id = query.from_user.id

    if await db.student_exists(user_id):
        await db.student_change_alert(True, user_id)
        await query.message.edit_reply_markup(reply_murkup=settings_inile_kb(user_id))
        await query.answer("Ви отримуватимите\nсповіщення про тривоги", show_alert=True)
        return


@router.callback_query(F.data == "change_news_not_agreed")
async def change_news_not_agreed(query: types.CallbackQuery) -> None:
    db = await Database.setup()
    user_id = query.from_user.id

    if await db.student_exists(user_id):
        await db.student_change_news(False, user_id)
        await query.message.edit_reply_markup(reply_murkup=settings_inile_kb(user_id))
        await query.answer("Ви не отримуватимите\nновин від бота", show_alert=True)
        return


@router.callback_query(F.data == "change_alert_not_agreed")
async def change_alert_not_agreed(query: types.CallbackQuery) -> None:
    db = await Database.setup()
    user_id = query.from_user.id

    if await db.student_exists(user_id):
        await db.student_change_alert(False, user_id)
        await query.message.edit_reply_markup(reply_murkup=settings_inile_kb(user_id))
        await query.answer("Ви не отримуватимите\nсповіщення про тривоги", show_alert=True)
        return
