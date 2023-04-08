from aiogram import types
from aiogram.dispatcher import Dispatcher
from data_base.controller_db import *
from aiogram.dispatcher.filters import Text

async def text_save(message: types.Message):
    if await user_exists_sql(message.from_user.id):
        if message.text[7::] < 2:
            await message.answer("текст закороткий")
        else:
            link = message.text[7::]
            groups = await see_group_for_user_id(message.from_user.id)
            await add_text_sql(link, groups)
            await message.answer("Успішно додано!")
    elif await teachers_exists_sql(message.from_user.id):
        if message.text[7::] < 2:
            await message.answer("текст закороткий")
        else:
            link = message.text[7::]
            groups = await see_group_for_teach_id(message.from_user.id)
            await add_text_sql(link, groups)
            await message.answer("Успішно додано!")
    else:
        await message.answer("Ви не зареєстровані у групах")

async def see_text(message: types.Message):
    if await user_exists_sql(message.from_user.id):
        groups = await see_group_for_user_id(message.from_user.id)
        boolean, text = await see_text_sql(groups)
        if boolean:
            await message.answer(text)
        elif not boolean:
            await message.answer("У вашої групи не додано ніякого тесту\nЩоб це зробити напишіть 'додати ваш текст'")
    elif await teachers_exists_sql(message.from_user.id):
        groups = await see_group_for_teach_id(message.from_user.id)
        boolean, text = await see_text_sql(groups)
        if boolean:
            await message.answer(text)
        elif not boolean:
            await message.answer("У вас не додано ніякого тесту\nЩоб це зробити напишіть 'додати ваш текст'")
    else:
        await message.answer("Ви не зареєстровані")

def register_handler_stats(dp: Dispatcher):
    dp.register_message_handler(text_save, Text(ignore_case=True, startswith="додати"))
    dp.register_message_handler(see_text, commands=['text'])
    