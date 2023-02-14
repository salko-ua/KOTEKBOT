from aiogram import types
from aiogram.dispatcher import Dispatcher
from keyboards import *
from data_base.controller_db import *
import asyncio

super_admin = 5963046063



#===========================Список груп============================
#@dp.message_handler(commands = ['admin'])
async def admin_kb(msg: types.Message):
    if await admin_exists_sql(msg.from_user.id) and msg.from_user.id == super_admin:
        await msg.answer("Клавіатура адміна", reply_markup=kb_admin)
    elif await admin_exists_sql(msg.from_user.id):
        await msg.answer("Клавіатура адміна", reply_markup=kb_admin)
    elif msg.from_user.id == super_admin:
        await msg.answer("Клавіатура адміна", reply_markup=sadmin_ad)
    
    
#@dp.message_handler(commands = ['sadmin'])
async def super_admin_kb(msg: types.Message):
    if msg.from_user.id == super_admin:
        await msg.answer("Клавіатура власника", reply_markup=sadmin)

#@dp.message_handler(commands = ['user'])
async def user_kb(msg: types.Message):
    if await user_exists_sql(msg.from_user.id) and msg.from_user.id == super_admin:
        await msg.answer("Клавіатура юзера", reply_markup=kb_client)
    elif await user_exists_sql(msg.from_user.id):
        await msg.answer("Клавіатура юзера", reply_markup=kb_client)
    elif msg.from_user.id == super_admin:
        await msg.answer("Клавіатура юзера", reply_markup=sadmin_cl)
    


#@dp.message_handler(commands = ['showuser'])
async def super_admin_showuser(msg: types.Message):
    if msg.from_user.id == super_admin:
        booled = await user_all_sql()
        if booled:
            await msg.answer("Немає користувачів")
        elif not booled:
            spisok = list_all_user.get()
            await msg.answer(spisok)
    else:
        dels = await msg.answer("У тебе немає прав, для перегляду бази данних")
        await asyncio.sleep(4)
        await msg.delete()
        await dels.delete()
             

#@dp.message_handler(commands = ['showgroupa'])
async def super_admin_groupa(msg: types.Message):
    if msg.from_user.id == super_admin:
        booled = await groupa_all_sql()
        if booled:
            await msg.answer("Немає груп в бд")
        elif not booled:
            spisok = list_all_groupa.get()
            await msg.answer(spisok)
    else:
        dels = await msg.answer("У тебе немає прав, для перегляду бази данних")
        await asyncio.sleep(4)
        await msg.delete()
        await dels.delete()
             

#@dp.message_handler(commands = ['showadmin'])
async def super_admin_admin(msg: types.Message):
    if msg.from_user.id == super_admin:
        booled = await admin_all_sql()
        if booled:
            await msg.answer("Немає адмінів в бд")
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
    dp.register_message_handler(admin_kb, commands = ['admin'])
    dp.register_message_handler(super_admin_kb, commands = ['sadmin'])
    dp.register_message_handler(user_kb, commands = ['user'])
    dp.register_message_handler(super_admin_showuser, commands = ['showuser'])
    dp.register_message_handler(super_admin_groupa, commands = ['showgroupa'])
    dp.register_message_handler(super_admin_admin, commands = ['showadmin'])
