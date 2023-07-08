# import
import asyncio

# from import
from keyboards import *
from aiogram import types, F, Router
from data_base import Database

from handlers.menu import menu
from aiogram.types import ReplyKeyboardRemove

from aiogram.filters import Command, Text

from handlers.user import user_update_db

router = Router()

text = {
    "help": ["Допомога 🛠", "Допомога", "help"],
    "donate": ["Донат 🫡", "Донат", "donate"],
}


#                            СТАРТ
@router.message(Command("start"))
async def start(message: types.Message):
    db = await Database.setup()
    if not message.chat.type == "private":
        await message.answer(
            "❗️ Використовуй /start у @pedbot_bot",
        )
        return

    await menu(message)


@router.message(Command("delete_kb"))
async def delete_keyboard(message: types.Message):
    await message.answer("♻️Клавіатуру видалено♻️", reply_markup=ReplyKeyboardRemove())


@router.message(Command("version"))
async def versions(message: types.Message):
    version = (
        "Версія бота : release 2.0 \nВерсія Python : 3.11.2\nВерсія Aiogram : 3.0.0b7"
    )
    await message.answer(version)


@router.message(Command("donate"))
@router.message(Text(text=text["donate"], ignore_case=True))
async def donate(message: types.Message):
    text = """
Підтримати проєкт можна за:

💳 Monobank card : <code>5375411202975004</code>
💳 Monobank url : <a href='https://send.monobank.ua/jar/5uzN1NcwYA'>monobank</a>

❤️ Повернись живим : <a href='https://savelife.in.ua/'>сайт</a>

Кошти підуть на оплату хостингу та покращення бота 🌚
"""
    await message.answer(
        text,
        reply_markup=await url_card_kb(),
        parse_mode="HTML",
        disable_web_page_preview=True,
    )


@router.message(Command("help"))
@router.message(Text(text=text["help"], ignore_case=True))
async def help(message: types.Message):
    help = "Пишіть сюди : @botadmincat"
    await message.answer(help)


""" список для BotFather
start - запуск / перезапуск бота
text - замітки
stats - статистика
help - допомога
donate - підтримка проєкту
version - версія
delete_kb - видалити клавіатуру
"""
