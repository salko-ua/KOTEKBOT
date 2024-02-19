from aiogram import Router, types
from aiogram.filters import Command

from src.handlers.menu import check_who, menu
from src.keyboards import *

router = Router()


@router.message(Command("start"))
async def start(message: types.Message) -> None:
    await message.delete()
    await menu(message)


@router.message(Command("version"))
async def versions(message: types.Message) -> None:
    await message.delete()

    version = (
        "🤖 Версія бота : release 2.1\n" "🐍 Версія Python : 3.12.1\n" "🤖 Версія Aiogram : 3.4.1\n"
    )

    await message.answer(version, reply_markup=hide_kb())


@router.message(Command("schedule"))
async def schedule(message: types.Message) -> None:
    telegram_id = message.from_user.id
    await message.delete()

    if not await check_who(message):
        await message.answer(text="Ви повинні бути зарєстровані❗️", reply_markup=hide_kb())
        return

    await message.answer(text="Перегляд розкладу ⬇️", reply_markup=await schedule_kb(telegram_id))


@router.message(Command("applicant"))
async def for_applicant(message: types.Message) -> None:
    await message.delete()
    await message.answer(text="Інформація для абітурієнта 😵‍💫", reply_markup=applicant_kb())


""" список для BotFather
start - запуск / перезапуск бота
schedule - розклад
applicant - Для абітурієнта
version - версія
"""
