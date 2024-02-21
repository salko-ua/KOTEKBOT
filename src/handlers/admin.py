import asyncio
from typing import Any

from aiogram import Bot, F, Router
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.keyboards import *
from src.utils import menu


class FSMAdmin(StatesGroup):
    photo = State()
    text = State()
    mixed_photo = State()
    mixed_text = State()


router = Router()


# Сховати ❌ (Використовується скрізь)
@router.callback_query(F.data == "Сховати ❌")
async def hide_message(query: CallbackQuery):
    await query.message.delete()


# Клавіаура адміна
@router.message(F.text == "Адмін 🔑")
async def admin(message: Message) -> None:
    db = await Database.setup()
    if await db.admin_exists(message.from_user.id):
        await message.delete()
        await message.answer(text="Клавіатура адміна", reply_markup=admin_kb())


# ===========================Видалити акаунт============================
@router.message(F.text == "Видалити акаунт")
async def delete_admin(message: Message) -> None:
    db = await Database.setup()
    if not await db.admin_exists(message.from_user.id):
        await message.answer(text="Ви не адмін :D", reply_markup=start_all_kb())
        return

    await db.delete_admins(message.from_user.id)
    await menu(message)


# NOTIFY ALL USERS
@router.callback_query(F.data == "Викласти 🖼")
async def send_photo_news(query: CallbackQuery, state: FSMContext) -> None:
    db = await Database.setup()
    if not await db.admin_exists(query.from_user.id):
        return

    await query.message.edit_text("Надішліть фото 🖼")
    await query.message.edit_reply_markup(reply_markup=admin_back_kb())
    await state.set_state(FSMAdmin.photo)
    await state.update_data(query=query)


@router.callback_query(F.data == "Викласти 📝")
async def send_message_news(query: CallbackQuery, state: FSMContext) -> None:
    db = await Database.setup()
    if not await db.admin_exists(query.from_user.id):
        return

    await query.message.edit_text("Надішліть текст 📝")
    await query.message.edit_reply_markup(reply_markup=admin_back_kb())
    await state.set_state(FSMAdmin.text)
    await state.update_data(query=query)


@router.callback_query(F.data == "Викласти 🖼📝")
async def send_mixed_news(query: CallbackQuery, state: FSMContext) -> None:
    db = await Database.setup()
    if not await db.admin_exists(query.from_user.id):
        return

    await query.message.edit_text("Надішліть текст 📝")
    await query.message.edit_reply_markup(reply_markup=admin_back_kb())
    await state.set_state(FSMAdmin.mixed_text)
    await state.update_data(query=query)


@router.callback_query(FSMAdmin.photo, F.data == "Назад")
@router.callback_query(FSMAdmin.text, F.data == "Назад")
@router.callback_query(FSMAdmin.mixed_text, F.data == "Назад")
@router.callback_query(FSMAdmin.mixed_photo, F.data == "Назад")
async def back(query: CallbackQuery, state: FSMContext) -> None:
    await query.message.edit_text("Новину відмінено✅")
    await query.message.edit_reply_markup(reply_markup=admin_kb())
    await state.clear()
    return


@router.message(FSMAdmin.photo, F.photo)
async def send_photo_news1(message: Message, state: FSMContext) -> None:
    db = await Database.setup()
    data = await state.get_data()
    query: CallbackQuery = data["query"]
    photo = message.photo[0].file_id
    user_ids = await db.list_id_student_agreed_news()

    await state.clear()
    await message.delete()
    await query.message.delete()
    await asyncio.gather(
        *map(send_notification(bot=message.bot, what_send=1, text="", photo=photo), user_ids)
    )
    await message.answer(text="Надсилання закінчено!")


@router.message(FSMAdmin.text, F.text)
async def send_message_news1(message: Message, state: FSMContext) -> None:
    db = await Database.setup()
    text = message.text
    user_ids = await db.list_id_student_agreed_news()

    await state.clear()
    await asyncio.gather(
        *map(send_notification(bot=message.bot, what_send=2, text=text, photo=""), user_ids)
    )
    await message.answer(text="Надсилання закінчено!")


@router.message(FSMAdmin.mixed_text, F.text)
async def send_mixed_news1(message: Message, state: FSMContext) -> None:
    await message.answer(text="Надішліть фото 🖼", reply_markup=admin_back_kb())
    await state.update_data(text=message.text)
    await state.set_state(FSMAdmin.mixed_photo)


@router.message(FSMAdmin.mixed_photo, F.photo)
async def send_mixed_news2(message: Message, state: FSMContext) -> None:
    db = await Database.setup()
    data = await state.get_data()
    text = data["text"]
    photo = message.photo[0].file_id
    user_ids = await db.list_id_student_agreed_news()

    await state.clear()
    await asyncio.gather(
        *map(send_notification(bot=message.bot, what_send=3, text=text, photo=photo), user_ids)
    )
    await message.answer(text="Надсилання закінчено!")


def send_notification(bot: Bot, what_send: int, text: str, photo: str) -> Any:
    async def wrapped(user_id: int):
        try:
            if what_send == 1:
                await bot.send_photo(user_id, photo)
            elif what_send == 2:
                await bot.send_message(user_id, text)
            elif what_send == 3:
                await bot.send_photo(user_id, photo, caption=text)
        except Exception:
            await bot.send_message(chat_id=2138964363, text=f"{user_id} blocked bot")

    return wrapped
