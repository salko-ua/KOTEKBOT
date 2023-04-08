# import
import asyncio

# from import
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.exceptions import (
    MessageToDeleteNotFound,
    MessageCantBeDeleted,
    BadRequest,
)
from aiogram.dispatcher.filters import Text
from keyboards import *
from data_base.controller_db import *
from handlers.stats import stats_schedule_add, stats_all


#                            СТАРТ
async def start(message: types.Message):
    if message.chat.type == "private":
        if await admin_exists_sql(message.from_user.id):
            await message.answer("Ви адмін", reply_markup=kb_start_admin)
        elif await user_exists_sql(message.from_user.id):
            await message.answer("⬇️ Клавіатура ⬇️", reply_markup=kb_start_user)
        elif await teachers_exists_sql(message.from_user.id):
            await message.answer("⬇️ Клавіатура ⬇️", reply_markup=kb_start_user)
        else:
            await message.answer("⬇️ Клавіатура ⬇️", reply_markup=kb_start)
    else:
        try:
            msg = await message.answer(
                "❗️Цю команду можна використовувати тільки в особистих повідомленнях\nПерейдіть до @pedbot_bot",
                reply_markup=ReplyKeyboardRemove(),
            )
            await asyncio.sleep(6)
            await message.delete()
            await msg.delete()
        except (MessageToDeleteNotFound, MessageCantBeDeleted, BadRequest):
            await message.answer(
                "Помилка, я не можу автовидалити своє повідомлення, мені потрібні права адміна"
            )


# @dp.message_handler(commands=["coupes"])
async def view_coupes_comm(message: types.Message):
    if await user_exists_sql(message.from_user.id):
        boolen, photo, date = await see_rod_sql(message.from_user.id)
        if boolen:
            try:
                await message.answer_photo(photo, date)
            except BadRequest:
                pass
        elif not boolen:
            try:
                msg = await message.answer("☹️ Розкладу для вашої групи ще немає... ☹️")
                await asyncio.sleep(4)
                await message.delete()
                await msg.delete()
            except (MessageToDeleteNotFound, MessageCantBeDeleted, BadRequest):
                await message.answer(
                    "Помилка, я не можу автовидалити своє повідомлення, мені потрібні права адміна"
                )
    else:
        if message.chat.type == "private":
            await message.answer(
                "❗️Зареєструйтесь❗️", reply_markup=ReplyKeyboardRemove()
            )
        else:
            try:
                msg = await message.answer(
                    "❗️Перейдіть до @pedbot_bot і зареєструйтесь",
                    reply_markup=ReplyKeyboardRemove(),
                )
                await asyncio.sleep(4)
                await message.delete()
                await msg.delete()
            except (MessageToDeleteNotFound, MessageCantBeDeleted, BadRequest):
                await message.answer(
                    "Помилка, я не можу автовидалити своє повідомлення, мені потрібні права адміна"
                )


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
            "Версія бота : release 1.7 \nВерсія Python : 3.11.1\nВерсія Aiogram : 2.24"
        )
        await message.answer(version)
    except (MessageToDeleteNotFound, MessageCantBeDeleted, BadRequest):
        await message.answer(
            "Помилка, я не можу автовидалити своє повідомлення, мені потрібні права адміна"
        )


# @dp.message_handler(commands=["info"])
async def donate(message: types.Message):
    await stats_schedule_add("Донат 🫡", 1)
    version = "Підтримати проєкт можна\nза номером карти : 5375411202975004\n\
або за посиланням : <a href='https://send.monobank.ua/jar/5uzN1NcwYA'>monobank</a>"
    await message.answer(version, parse_mode="HTML", disable_web_page_preview=True)


# @dp.message_handler(commands=["help"])
async def help(message: types.Message):
    await stats_schedule_add("Команди 🛠", 1)
    try:
        help = """❗️Команди з префіксом '/'
зручно використовувати в групах.

❓Щоб використовувати бота в групах:
1.Додайте його у свою групу.
2.Дайте права адміністратора.
3.Напишіть / і бот покаже всі доступні команди.
"""
        await message.answer(help)
    except (MessageToDeleteNotFound, MessageCantBeDeleted, BadRequest):
        pass


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
    # Розклад
    dp.register_message_handler(view_coupes_comm, commands=["coupes"])
    # Видалення клавіатури
    dp.register_message_handler(delete_keyboard, commands=["delete_keyboards"])
    # Версія
    dp.register_message_handler(versions, commands=["version"])
    # Ститистика
    dp.register_message_handler(stats_all, commands=["stats"])


""" список для BotFather
start - запуск / перезапуск бота
coupes - перегляд розкладу
text - ваш текст
stats - статистика
help - допомога
donate - підтримка проєкту
version - версія
delete_keyboards - видалити клавіатуру
"""
