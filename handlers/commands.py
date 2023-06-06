# import
import asyncio

# from import
from keyboards import *
from aiogram import types
from data_base import Database

from handlers.menu import menu
from handlers.stats import stats_all
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardRemove

from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import (
    MessageToDeleteNotFound,
    MessageCantBeDeleted,
    BadRequest,
)


#                            СТАРТ
async def start(message: types.Message):
    db = await Database.setup()
    if not message.chat.type == "private":
        await message.answer(
            "❗️ Використовуй /start у @pedbot_bot",
            reply_markup=ReplyKeyboardRemove(),
        )
        return

    await menu(message)


# @dp.message_handler(commands=["delete_keyboards"])
async def delete_keyboard(message: types.Message):
    try:
        msg = await message.answer(
            "♻️Клавіатуру видалено♻️", reply_markup=ReplyKeyboardRemove()
        )
        await asyncio.sleep(4)
        await message.delete()
        await msg.delete()
    except (MessageToDeleteNotFound, MessageCantBeDeleted, BadRequest):
        await message.answer(
            "Помилка, я не можу автовидалити своє повідомлення, мені потрібні права адміна"
        )


# @dp.message_handler(commands=["version"])
async def versions(message: types.Message):
    try:
        version = (
            "Версія бота : release 1.11 \nВерсія Python : 3.11.1\nВерсія Aiogram : 2.25"
        )
        await message.answer(version)
    except (MessageToDeleteNotFound, MessageCantBeDeleted, BadRequest):
        await message.answer(
            "Помилка, я не можу автовидалити своє повідомлення, мені потрібні права адміна"
        )


# @dp.message_handler(commands=["info"])
async def donate(message: types.Message):
    version = """
Підтримати проєкт можна за:

💳 Monobank card : <code>5375411202975004</code>
💳 Monobank url : <a href='https://send.monobank.ua/jar/5uzN1NcwYA'>monobank</a>

❤️ Повернись живим : <a href='https://savelife.in.ua/'>сайт</a>

Кошти підуть на покращення бота 🇺🇦
"""
    await message.answer(version, reply_markup=url_card_kb, parse_mode="HTML", disable_web_page_preview=True)


# @dp.message_handler(commands=["help"])
async def help(message: types.Message):
    help = "Пишіть сюди : @botadmincat"
    await message.answer(help)


text = {
    "help": ["Допомога 🛠", "Допомога", "help"],
    "donate": ["Донат 🫡", "Донат", "donate"],
}


# ===========================реєстратор============================
def register_handler_commands(dp: Dispatcher):
    # start
    dp.register_message_handler(start, commands=["start"])
    # Команди
    dp.register_message_handler(help, Text(ignore_case=True, equals=text["help"]))
    dp.register_message_handler(help, commands=["help"])
    # Підтримка
    dp.register_message_handler(donate, Text(ignore_case=True, equals=text["donate"]))
    dp.register_message_handler(donate, commands=["donate"])
    # Видалення клавіатури
    dp.register_message_handler(delete_keyboard, commands=["delete_kb"])
    # Версія
    dp.register_message_handler(versions, commands=["version"])
    # Ститистика
    dp.register_message_handler(stats_all, commands=["stats"])


""" список для BotFather
start - запуск / перезапуск бота
text - замітки
stats - статистика
help - допомога
donate - підтримка проєкту
version - версія
delete_kb - видалити клавіатуру
"""
