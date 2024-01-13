import asyncio

from aiogram import F, Router
from aiogram.filters.state import State, StatesGroup
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import *
from create_bot import bot
from data_base import Database
from handlers.menu import menu
from keyboards import *


# =========Класс машини стану=========
class FSMAdmin(StatesGroup):
    # new news
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
async def admin(message: Message):
    db = await Database.setup()
    if await db.admin_exists_sql(message.from_user.id):
        await message.delete()
        await message.answer("Клавіатура адміна", reply_markup=await admin_kb())


# ===========================Видалити акаунт============================
@router.message(Text(text="Видалити акаунт", ignore_case=True))
async def delete_admin(message: Message):
    db = await Database.setup()
    if not await db.admin_exists_sql(message.from_user.id):
        await message.answer("Ви не адмін :D", reply_markup=await start_all_kb())
        return

    await db.delete_admins_sql(message.from_user.id)
    await menu(message)


# надсилання одного з варіантів
@router.callback_query(Text(text="Викласти 🖼", ignore_case=True))
async def send_photo_news(query: CallbackQuery, state: FSMContext):
    db = await Database.setup()

    if not await db.admin_exists_sql(query.from_user.id):
        return

    await query.message.edit_text("Надішліть фото 🖼")
    await query.message.edit_reply_markup(reply_markup=await admin_back_kb())
    await state.set_state(FSMAdmin.photo)
    await state.update_data(query=query)


@router.callback_query(Text(text="Викласти 📝", ignore_case=True))
async def send_message_news(query: CallbackQuery, state: FSMContext):
    db = await Database.setup()
    if not await db.admin_exists_sql(query.from_user.id):
        return

    await query.message.edit_text("Надішліть текст 📝")
    await query.message.edit_reply_markup(reply_markup=await admin_back_kb())
    await state.set_state(FSMAdmin.text)
    await state.update_data(query=query)


@router.callback_query(Text(text="Викласти 🖼📝", ignore_case=True))
async def send_mixed_news(query: CallbackQuery, state: FSMContext):
    db = await Database.setup()
    if not await db.admin_exists_sql(query.from_user.id):
        return

    await query.message.edit_text("Надішліть текст 📝")
    await query.message.edit_reply_markup(reply_markup=await admin_back_kb())
    await state.set_state(FSMAdmin.mixed_text)
    await state.update_data(query=query)


@router.callback_query(FSMAdmin.photo, F.data == "Назад")
@router.callback_query(FSMAdmin.text, F.data == "Назад")
@router.callback_query(FSMAdmin.mixed_text, F.data == "Назад")
@router.callback_query(FSMAdmin.mixed_photo, F.data == "Назад")
async def back(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text("Новину відмінено✅")
    await query.message.edit_reply_markup(reply_markup=await admin_kb())
    await state.clear()
    return


@router.message(FSMAdmin.photo, F.photo)
async def send_photo_news1(message: Message, state: FSMContext):
    db = await Database.setup()
    data = await state.get_data()
    query: CallbackQuery = data["query"]
    photo = message.photo[0].file_id
    user_ids = map(lambda e: e[0], await db.list_id_student_agreed_news_sql())
    teachers_ids = map(lambda e: e[0], await db.list_id_teacher_agreed_news_sql())

    # sending
    await state.clear()
    await message.delete()
    await query.message.delete()
    await asyncio.gather(*map(send_notification(1, None, photo), user_ids))
    await asyncio.gather(*map(send_notification(1, None, photo), teachers_ids))

    await message.answer("Надсилання закінчено!")


@router.message(FSMAdmin.text, F.text)
async def send_message_news1(message: Message, state: FSMContext):
    db = await Database.setup()
    text = message.text
    user_ids = map(lambda e: e[0], await db.list_id_student_agreed_news_sql())
    teachers_ids = map(lambda e: e[0], await db.list_id_teacher_agreed_news_sql())

    # sending
    await state.clear()
    await asyncio.gather(*map(send_notification(2, text, None), user_ids))
    await asyncio.gather(*map(send_notification(2, text, None), teachers_ids))

    await message.answer("Надсилання закінчено!")


@router.message(FSMAdmin.mixed_text, F.text)
async def send_mixed_news1(message: Message, state: FSMContext):
    await message.answer("Надішліть фото 🖼", reply_markup=await admin_back_kb())

    await state.update_data(text=message.text)
    await state.set_state(FSMAdmin.mixed_photo)


@router.message(FSMAdmin.mixed_photo, F.photo)
async def send_mixed_news2(message: Message, state: FSMContext):
    db = await Database.setup()
    data = await state.get_data()
    text = data["text"]
    photo = message.photo[0].file_id
    user_ids = map(lambda e: e[0], await db.list_id_student_agreed_news_sql())
    teachers_ids = map(lambda e: e[0], await db.list_id_teacher_agreed_news_sql())

    # sending
    await state.clear()
    await asyncio.gather(*map(send_notification(3, text, photo), user_ids))
    await asyncio.gather(*map(send_notification(3, text, photo), teachers_ids))

    await message.answer("Надсилання закінчено!")


# Функція надсилання
def send_notification(what_send: int, text: str, photo: str):
    async def wrapped(user_id: int):
        try:
            if what_send == 1:
                await bot.send_photo(user_id, photo)
            elif what_send == 2:
                await bot.send_message(user_id, text)
            elif what_send == 3:
                await bot.send_photo(user_id, photo, caption=text)
        except:
            pass

    return wrapped
