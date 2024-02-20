import os
import random
from datetime import datetime

from aiogram import types
from translate import Translator

from src.data_base import Database


async def get_current_date() -> str:
    translator = Translator(to_lang="uk")
    now = datetime.now()
    now = now.strftime("%d - %B, %A")
    return translator.translate(now)


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
    data = data[0]
    data_group = await check_user(user_id)

    message_text = (
        f"<b>👤 Ім'я: <a href='{url}'>{data[1]}</a> | {data[0]}</b>\n"
        f"<b>📅 Дата реєстації: {data[4]}</b>\n\n"
        f"<b>📊 Кількість взаємодій: {data[5]}</b>\n\n"
        f"<b>👨‍💼 Адмін:</b> {data_group[0]}\n\n"
        f"<b>👩‍🎓 Студент:</b> {data_group[1]}\n\n"
        f"<b>⌛️ Остання взаємодія з\n"
        f"ботом: {data[6]}</b>\n"
        f"(ця не враховується)\n"
    )
    return message_text


async def choose_random_photo() -> str:
    folder_path = "cat/"
    file_list = os.listdir(folder_path)
    random_file = random.choice(file_list)
    file_path = os.path.join(folder_path, random_file)
    return file_path
