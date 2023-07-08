import asyncio

from aiogram import F
from config import *
from keyboards import *
from create_bot import bot
from data_base import Database

from aiogram.types import Message
from handlers.menu import menu

from aiogram import Router
from aiogram.filters import Command
from aiogram.filters.text import Text

from aiogram.fsm.context import FSMContext

from aiogram.filters.state import State, StatesGroup


# =========Класс машини стану=========
class FSMAdmin(StatesGroup):
    # new news
    photo = State()
    text = State()
    mixed_photo = State()
    mixed_text = State()


router = Router()


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
@router.message(Text(text="Викласти 🖼", ignore_case=True))
async def send_photo_news(message: Message, state: FSMContext):
    db = await Database.setup()
    if not await db.admin_exists_sql(message.from_user.id):
        return

    await message.answer("Надішліть фото 🖼", reply_markup=await back_kb())
    await state.set_state(FSMAdmin.photo)


@router.message(Text(text="Викласти 📝", ignore_case=True))
async def send_message_news(message: Message, state: FSMContext):
    db = await Database.setup()
    if not await db.admin_exists_sql(message.from_user.id):
        return

    await message.answer("Надішліть текст 📝", reply_markup=await back_kb())
    await state.set_state(FSMAdmin.text)


@router.message(Text(text="Викласти 🖼📝", ignore_case=True))
async def send_mixed_news(message: Message, state: FSMContext):
    db = await Database.setup()
    if not await db.admin_exists_sql(message.from_user.id):
        return

    await message.answer("Надішліть текст 📝", reply_markup=await back_kb())
    await state.set_state(FSMAdmin.mixed_text)


@router.message(FSMAdmin.photo, F.photo | F.text)
async def send_photo_news1(message: Message, state: FSMContext):
    db = await Database.setup()
    if message.text == "Назад":
        await message.answer("Новину відмінено✅", reply_markup=await admin_kb())
        await state.clear()
        return

    if not await db.admin_exists_sql(message.from_user.id):
        return

    photo = message.photo[0].file_id
    text = None
    what_send = 1

    await message.answer("Надсилається..", reply_markup=await admin_kb())
    await state.clear()

    all_user_ids = map(lambda e: e[0], await db.list_id_student_agreed_news_sql())
    all_teachers_ids = map(lambda e: e[0], await db.list_id_teacher_agreed_news_sql())

    await asyncio.gather(*map(send_notification(what_send, text, photo), all_user_ids))
    await asyncio.gather(
        *map(send_notification(what_send, text, photo), all_teachers_ids)
    )
    await message.answer("Надсилання закінчено!")


@router.message(FSMAdmin.text, F.text)
async def send_message_news1(message: Message, state: FSMContext):
    db = await Database.setup()
    if message.text == "Назад":
        await message.answer("Новину відмінено✅", reply_markup=await admin_kb())
        await state.clear()
        return

    if not await db.admin_exists_sql(message.from_user.id):
        return

    photo = None
    text = message.text
    what_send = 2

    await message.answer("Надсилається..", reply_markup=await admin_kb())
    await state.clear()

    all_user_ids = map(lambda e: e[0], await db.list_id_student_agreed_news_sql())
    all_teachers_ids = map(lambda e: e[0], await db.list_id_teacher_agreed_news_sql())
    await asyncio.gather(*map(send_notification(what_send, text, photo), all_user_ids))
    await asyncio.gather(
        *map(send_notification(what_send, text, photo), all_teachers_ids)
    )
    await message.answer("Надсилання закінчено!")


@router.message(FSMAdmin.mixed_text, F.text)
async def send_mixed_news1(message: Message, state: FSMContext):
    db = await Database.setup()
    if message.text == "Назад":
        await message.answer("Новину відмінено✅", reply_markup=await admin_kb())
        await state.clear()
        return

    if not await db.admin_exists_sql(message.from_user.id):
        return

    await state.update_data(text=message.text)

    await message.answer("Надішліть фото 🖼", reply_markup=await back_kb())
    await state.set_state(FSMAdmin.mixed_photo)


@router.message(FSMAdmin.mixed_photo, F.photo | F.text)
async def send_mixed_news2(message: Message, state: FSMContext):
    db = await Database.setup()
    if message.text == "Назад":
        await message.answer("Новину відмінено✅", reply_markup=await admin_kb())
        await state.clear()
        return

    if not await db.admin_exists_sql(message.from_user.id):
        return

    data = await state.get_data()
    text = data["text"]
    photo = message.photo[0].file_id
    what_send = 3

    await message.answer("Надсилається..", reply_markup=await admin_kb())
    await state.clear()

    all_user_ids = map(lambda e: e[0], await db.list_id_student_agreed_news_sql())
    all_teachers_ids = map(lambda e: e[0], await db.list_id_teacher_agreed_news_sql())

    await asyncio.gather(*map(send_notification(what_send, text, photo), all_user_ids))
    await asyncio.gather(
        *map(send_notification(what_send, text, photo), all_teachers_ids)
    )
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
