from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove
from handlers.menu import check_all, get_about_me

from handlers.menu import menu
from keyboards import *

router = Router()

#                            СТАРТ
@router.message(Command("start"), F.chat.type == "private")
async def start(message: types.Message):   
    await message.delete() 
    await menu(message)


@router.message(Command("delete_kb"))
async def delete_keyboard(message: types.Message):
    try:
        await message.delete()
    except:
        await message.answer("Бот повинен бути адміністратором❗️")
        return
    
    await message.answer("♻️Клавіатуру видалено♻️", 
                         reply_markup=ReplyKeyboardRemove())


@router.message(Command("version"))
async def versions(message: types.Message):
    try:
        await message.delete()
    except:
        await message.answer("Бот повинен бути адміністратором❗️")
        return
    
    version = ("🤖 Версія бота : release 2.0\n"
            "🐍 Версія Python : 3.11.2\n"
            "🤖 Версія Aiogram : 3.0.0b7\n")
    
    await message.answer(version, reply_markup=await hide_kb())

# Розклад 📚
@router.message(Command("schedule"))
async def schedule(message: types.Message):
    try:
        await message.delete()
    except:
        await message.answer("Бот повинен бути адміністратором❗️")
        return

    if not await check_all(message):
        await message.answer("Ви повинні бути зарєстровані❗️", reply_markup=await hide_kb())
        return

    await message.answer("Перегляд розкладу ⬇️", reply_markup=await schedule_kb(message.from_user.id))

@router.message(Command("applicant"))
async def for_applicant(message: types.Message):
    try:
        await message.delete()
    except:
        await message.answer("Бот повинен бути адміністратором❗️")
        return

    await message.answer("Інформація для абітурієнта 😵‍💫", reply_markup=await applicant_kb())

@router.message(Command("me"))
async def about_me(message: types.Message):
    try:
        await message.delete()
    except:
        await message.answer("Бот повинен бути адміністратором❗️")
        return
    
    user_id = message.from_user.id
    url = message.from_user.url
    check, text = await get_about_me(user_id, url)
    if not check:
        await message.answer("Зареєструйтесь у боті ❗️")

    await message.answer(text, 
                         parse_mode="HTML",
                         disable_web_page_preview=True,
                         reply_markup=await other_back_kb())
    
@router.message(Command("other"))
async def others(message: types.Message):
    try:
        await message.delete()
    except:
        await message.answer("Бот повинен бути адміністратором❗️")
        return
    
    await message.answer("Інша інформація 🤯", reply_markup=await other_kb())



""" список для BotFather
start - запуск / перезапуск бота
schedule - розклад
me - інформація про мене
other - Інші функції
applicant - Для абітурієнта
version - версія
delete_kb - видалити клавіатуру'
"""