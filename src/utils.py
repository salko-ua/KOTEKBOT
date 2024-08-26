import os
import random
import asyncache
import cachetools

from random import choice
from aiogram import types
from datetime import datetime
from aiogram.fsm.context import FSMContext

from src.keyboards import *
from src.data_base import Database
from src.config import SUPER_ADMIN


def get_current_date() -> str:
    return datetime.now().strftime("%d.%m.%Y")


@asyncache.cached(cachetools.TTLCache(1, 120))
def password_for_admin():
    password = ""
    for x in range(8):
        password += choice(list("1234567890ABCDEFGHIGKLMNOPQRSTUVYXWZ"))
    return password


async def is_super_admin(object_: types.Message | types.CallbackQuery) -> bool:
    user_id = object_.from_user.id
    if user_id in SUPER_ADMIN:
        return True
    else:
        return False


async def menu(message: types.Message) -> None:
    db = await Database.setup()
    if await db.admin_exists(message.from_user.id):
        await message.answer(text="⬇️Головне меню⬇️", reply_markup=start_admin_kb())
    elif await db.student_exists(message.from_user.id):
        await message.answer(text="⬇️Головне меню⬇️", reply_markup=start_student_kb())
    else:
        await message.answer(text="⬇️Головне меню⬇️", reply_markup=start_all_kb())


async def check_user(user_id: int) -> tuple[str, str]:
    db = await Database.setup()
    if await db.admin_exists(user_id):
        admin = "✅"
    else:
        admin = "❌"

    if await db.student_exists(user_id):
        student = await db.group_for_student_id(user_id)
    else:
        student = "❌"

    return admin, student


async def check_who(message: types.Message) -> bool:
    db = await Database.setup()
    user_id = message.from_user.id
    if await db.student_exists(user_id):
        return True
    if await db.admin_exists(user_id):
        return True

    return False


async def get_about_me(user_id, url) -> str:
    db = await Database.setup()

    data = await db.user_show_data(user_id)
    admin, student = await check_user(user_id)

    message_text = (
        f"<b>👤 Ім'я: <a href='{url}'>{data[1]}</a> | {data[0]}</b>\n"
        f"<b>📅 Дата реєстрації: {data[4]}</b>\n\n"
        f"<b>📊 Кількість взаємодій: {data[5]}</b>\n\n"
        f"<b>👨‍💼 Адмін:</b> {admin}\n\n"
        f"<b>👩‍🎓 Студент:</b> {student}\n\n"
        f"<b>⌛️ Остання взаємодія з\n"
        f"ботом: {data[6]}</b>\n"
        f"(ця не враховується)\n"
    )
    return message_text


async def clear_all(message: types.Message, state: FSMContext) -> None:
    old_message: types.Message = (await state.get_data())["message"]
    await message.delete()
    await old_message.delete()
    await state.clear()


# TODO: Move all photo to database
async def choose_random_photo() -> str:
    folder_path = "cat/"
    file_list = os.listdir(folder_path)
    random_file = random.choice(file_list)
    file_path = os.path.join(folder_path, random_file)
    return file_path
