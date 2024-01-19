from aiogram import F, Router, types
from aiogram.filters import Command

from src.handlers.menu import check_all, menu
from src.keyboards import *

router = Router()


@router.message(Command("start"), F.chat.type == "private")
async def start(message: types.Message) -> None:
    await message.delete()
    await menu(message)


@router.message(Command("version"))
async def versions(message: types.Message) -> None:
    try:
        await message.delete()
    except:
        await message.answer("Бот повинен бути адміністратором❗️")
        return

    version = (
        "🤖 Версія бота : release 2.0\n"
        "🐍 Версія Python : 3.11.2\n"
        "🤖 Версія Aiogram : 3.0.0b7\n"
    )

    await message.answer(version, reply_markup=await hide_kb())


@router.message(Command("schedule"))
async def schedule(message: types.Message) -> None:
    try:
        await message.delete()
    except:
        await message.answer("Бот повинен бути адміністратором❗️")
        return

    if not await check_all(message):
        await message.answer(
            "Ви повинні бути зарєстровані❗️", reply_markup=await hide_kb()
        )
        return

    await message.answer(
        "Перегляд розкладу ⬇️",
        reply_markup=await schedule_kb(message.from_user.id),
    )


@router.message(Command("applicant"))
async def for_applicant(message: types.Message) -> None:
    try:
        await message.delete()
    except:
        await message.answer("Бот повинен бути адміністратором❗️")
        return

    await message.answer(
        "Інформація для абітурієнта 😵‍💫", reply_markup=await applicant_kb()
    )


""" список для BotFather
start - запуск / перезапуск бота
schedule - розклад
applicant - Для абітурієнта
version - версія
"""
