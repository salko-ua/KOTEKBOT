#import
import asyncio

#from import
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.exceptions import MessageIsTooLong
from keyboards import *
from data_base.controller_db import *
from config import super_admin
from create_bot import bot






#===========================Список груп============================
#Клавіаура адміна
async def admin_kb(msg: types.Message):
    if await admin_exists_sql(msg.from_user.id) or msg.from_user.id == super_admin:
        await msg.answer("Клавіатура адміна", reply_markup=kb_admin)

#Клавіаура власника
async def super_admin_kb(msg: types.Message):
    if msg.from_user.id == super_admin:
        await msg.answer("Клавіатура власника", reply_markup=sadmin)

#Клавіаура користувача
async def user_kb(msg: types.Message):
    if await user_exists_sql(msg.from_user.id) or msg.from_user.id == super_admin:
        await msg.answer("Клавіатура юзера", reply_markup=kb_client)


    


#Показати таблицю користувачів
async def super_admin_user(msg: types.Message):
    if msg.from_user.id == super_admin:
        try:
            booled = await user_all_sql()
            if booled:
                await msg.answer("Немає користувачів")
            elif not booled:
                spisok = list_all_user.get()
                await msg.answer(spisok)
        except MessageIsTooLong:
            await msg.answer("користувачв багато")
    else:
        dels = await msg.answer("У тебе немає прав, для перегляду бази данних")
        await asyncio.sleep(4)
        await msg.delete()
        await dels.delete()
             

#Показати таблицю груп
async def super_admin_groupa(msg: types.Message):
    if msg.from_user.id == super_admin:
        booled = await groupa_all_sql()
        if booled:
            await msg.answer("Немає груп")
        elif not booled:
            spisok = list_all_groupa.get()
            await msg.answer(spisok)
    else:
        dels = await msg.answer("У тебе немає прав, для перегляду бази данних")
        await asyncio.sleep(4)
        await msg.delete()
        await dels.delete()
             

#Показати таблицю адмінів
async def super_admin_admin(msg: types.Message):
    if msg.from_user.id == super_admin:
        booled = await admin_all_sql()
        if booled:
            await msg.answer("Немає адмінів")
        elif not booled:
            spisok = list_all_admin.get()
            await msg.answer(spisok)
    else:
        dels = await msg.answer("У тебе немає прав, для перегляду бази данних")
        await asyncio.sleep(4)
        await msg.delete()
        await dels.delete()
             


#===========================реєстратор============================
def register_handler_sadmin(dp : Dispatcher):
    dp.register_message_handler(admin_kb, text = 'адмін')
    dp.register_message_handler(super_admin_kb, text = 'власник')
    dp.register_message_handler(user_kb, text = 'студент')
    dp.register_message_handler(super_admin_user, text = 'Показати таблицю студентів')
    dp.register_message_handler(super_admin_groupa, text = 'Показати таблицю групи')
    dp.register_message_handler(super_admin_admin, text = 'Показати таблицю адмінів')
