from aiogram import types
from aiogram.dispatcher import Dispatcher
from data_base.controller_db import *
from aiogram.dispatcher.filters import Text
from handlers.stats import stats_schedule_add
from asyncio import sleep

async def text_save(message: types.Message):
    await stats_schedule_add("Додати замітку 📝", 1)
    if await user_exists_sql(message.from_user.id):
        if len(message.text[7::]) < 2:
            await message.answer("текст закороткий")
        else:
            link = message.text[7::]
            groups = await see_group_for_user_id(message.from_user.id)
            await add_text_sql(link, groups)
            await message.answer("Успішно додано!")
    elif await teachers_exists_sql(message.from_user.id):
        if len(message.text[7::]) < 2:
            await message.answer("текст закороткий")
        else:
            link = message.text[7::]
            groups = await see_group_for_teach_id(message.from_user.id)
            await add_text_sql(link, groups)
            await message.answer("Успішно додано!")
    else:
        await message.answer("Ви не зареєстровані у групах")

async def see_text(message: types.Message):
    await stats_schedule_add("Замітки 📝", 1)
    if await user_exists_sql(message.from_user.id):
        groups = await see_group_for_user_id(message.from_user.id)
        boolean, text = await see_text_sql(groups)
        if boolean:
            await message.answer("Замітки для вашої групи :\n\n"+text+"\n\nЩоб встановити нові\nнапишіть 'додати *ваш текст*'")
        elif not boolean:
            await message.answer("У вашої групи не додано ніякого тесту\nЩоб це зробити напишіть \n'додати *ваш текст*'")
    elif await teachers_exists_sql(message.from_user.id):
        groups = await see_group_for_teach_id(message.from_user.id)
        boolean, text = await see_text_sql(groups)
        if boolean:
            await message.answer("Ваші замітки :\n\n"+text+"\n\nЩоб встановити нові\nнапишіть 'додати *ваш текст*'")
        elif not boolean:
            await message.answer("У вас не додано ніякого тесту\nЩоб це зробити напишіть \n'додати *ваш текст*'")
    else:
        await message.answer("Ви не зареєстровані")

async def any(message: types.Message):
    await stats_schedule_add("Щось буде 🤔", -1)
    finish_error = "Що це"
    finish = "Що це"
    start = ""
    typing_symbol = "▒"
    msg = await message.answer("_")
    while start != finish_error:
        await msg.edit_text(start+typing_symbol)
        await sleep(0.001)
        start = start + finish[0]
        finish = finish[1:]
        await msg.edit_text(start)
        await sleep(0.001)
        

def register_handler_stats(dp: Dispatcher):
    dp.register_message_handler(text_save, Text(ignore_case=True, startswith="Додати"))
    dp.register_message_handler(see_text, commands=['text'])
    dp.register_message_handler(see_text, Text(ignore_case=True, equals="Замітки 📝"))
    dp.register_message_handler(any, Text(ignore_case=True, equals="Щось буде 🤔"))