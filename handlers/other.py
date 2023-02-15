from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import *
from data_base.controller_db import *
import asyncio


#answer - повідомлення
#reply - повідомлення відповідь
#send_massage - повідомлення в лс
password = "KOTEKPED24&"
super_admin = 5963046063

#=========Класс машини стану=========
class FSMReg(StatesGroup):
    course_groupe_reg = State()
    password_reg = State()
    reply_reg = State()


#===========================Регестрація============================
#@dp.message_handler(commands=["start"],state=None)
async def start(message: types.Message): 
    await clear_sql()
    await group_list_sql()
    if(not await user_exists_sql(message.from_user.id)) and (not await admin_exists_sql(message.from_user.id)):
        if message.chat.type == "private":
            await message.answer("Регестрація\nВиберіть тип акаунту : ", reply_markup=kb_choice)
            await FSMReg.reply_reg.set()
        else:
            msg = await message.answer("Перейдіть в особисті повідомлення до бота @pedbot_bot\nі зареєструйтесь за командою /start")
            await asyncio.sleep(2)
            await message.delete()
            await msg.delete()
    elif await user_exists_sql(message.from_user.id):
        if message.chat.type == "private":
            await message.answer("Ваша клавіатура : ",reply_markup=kb_client)
        else:
            msg = await message.answer("Ви зареєстрованні")
            await asyncio.sleep(2)
            await message.delete()
            await msg.delete()
    elif await admin_exists_sql(message.from_user.id):
        if message.chat.type == "private":
            await message.answer("Ваша клавіатура : ", reply_markup=kb_admin)
        else:
            msg = await message.answer("Ви зареєстрованні")
            await asyncio.sleep(2)
            await message.delete()
            await msg.delete()
    elif await message.from_user.id == super_admin:
        if message.chat.type == "private":
            await message.answer("Ваша клавіатура : ", reply_markup=sadmin)
        else:
            msg = await message.answer("Ви зареєстрованні")
            await asyncio.sleep(2)
            await message.delete()
            await msg.delete()
    

#@dp.message_handler(state=FSMReg.reply_reg)
async def reg(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.finish()
        await message.answer("Нажміть /start і увійдіть", reply_markup= ReplyKeyboardRemove())
    elif message.text == 'give admins':
        await FSMReg.password_reg.set()
        await message.answer("Введіть пароль", reply_markup=ReplyKeyboardRemove())
    elif message.text == "Студент":
        await FSMReg.course_groupe_reg.set()
        await message.answer("Введіть курс і групу з наведених нижче", reply_markup=get_kb())
    else:
        await state.finish()
        await message.answer("Немає такої відповіді\nНажміть /start і спробуйте ще раз", reply_markup= ReplyKeyboardRemove())
    
#@dp.message_handler(state=FSMReg.password_reg)
async def regAdmin(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.finish()
        await message.answer("Нажміть /start і увійдіть", reply_markup= ReplyKeyboardRemove())
    elif message.text == password:
        first_name = message.from_user.first_name
        username = message.from_user.username
        await add_admin_sql(message.from_user.id, first_name, username)
        await message.answer("Регестрація завершена", reply_markup=kb_admin)
        await state.finish()
    else:
        await message.answer("пароль неправильний, повторіть спробу написавши /start")
        await state.finish()

#@dp.message_handler(state=FSMReg.course_groupe_reg)
async def regUser(message: types.Message, state: FSMContext):
    first_name = message.from_user.first_name
    username = message.from_user.username
    groupe = message.text
    if message.text == 'Назад':
        await state.finish()
        await message.answer("Нажміть /start і увійдіть", reply_markup= ReplyKeyboardRemove())
    elif await group_exists_sql(message.text): 
        await add_user_sql(message.from_user.id, first_name, username, groupe)
        await state.finish()
        await message.answer("Регестрація завершена", reply_markup=kb_client)
    else:
        await message.answer("Немає такої групи, звяжіться з адміністратором\nдля того щоб її добавили \nІ повторіть спробу /start", reply_markup=ReplyKeyboardRemove())
        await state.finish()

#===========================Регестрація============================
#@dp.message_handler(commands=["count"])
async def count_user(message: types.Message):
    check = await count_user_sql()
    if check:
        await count_user_sql()
        msg = await message.answer(f"Кількість зареєстрованих людей : {count_us.get()}")
        await asyncio.sleep(4)
        await message.delete()
        await msg.delete()
    elif not check:
        msg = await message.answer(f"В боті незареєстровано нікого")
        await asyncio.sleep(4)
        await message.delete()
        await msg.delete()

#@dp.message_handler(commands=["countg"])
async def count_group(message: types.Message):
    check = await count_group_sql()
    if check:
        await count_group_sql()
        msg = await message.answer(f"Кількість груп : {count_gr.get()}")
        await asyncio.sleep(4)
        await message.delete()
        await msg.delete()
    elif not check:
        msg = await message.answer(f"Адміністратор ще не додав жодної групи")
        await asyncio.sleep(4)
        await message.delete()
        await msg.delete()

#===========================Список груп============================
#@dp.message_handler(commands=['list])
async def list_group_all(message: types.Message):
    await clear_sql()
    if await get_list_sql():
        msg = await message.answer(f"Список груп наявних в базі даних : \n{get_list.get()}")
        await asyncio.sleep(10)
        await message.delete()
        await msg.delete()
    elif not await get_list_sql():
        msg = await message.answer(f"Немає жодної групи")
        await asyncio.sleep(4)
        await message.delete()
        await msg.delete()

#@dp.message_handler(commands=["coupes"])
async def view_coupes_comm(message: types.Message):
    if await user_exists_sql(message.from_user.id):
        ids = message.from_user.id
        if message.chat.type == "private":
            if await see_rod_sql(str(ids)):
                msg = await message.answer_photo(photka.get(),date_coupes.get())
                await asyncio.sleep(15)
                await message.delete()
                await msg.delete()
            elif await see_rod_sql(str(ids)) == False:
                msg = await message.answer('Розкладу для вашої групи ще немає...')
                await asyncio.sleep(4)
                await message.delete()
                await msg.delete()
        else:
            if await see_rod_sql(str(ids)):
                msg = await message.answer_photo(photka.get(),date_coupes.get())
                await asyncio.sleep(15)
                await message.delete()
                await msg.delete()
            elif await see_rod_sql(str(ids)) == False:
                msg = await message.answer('Розкладу для вашої групи ще немає...')
                await asyncio.sleep(4)
                await message.delete()
                await msg.delete()
    elif await user_exists_sql(message.from_user.id):
        msg = await message.answer("Ви зареєстрованні адміном", reply_markup=ReplyKeyboardRemove())
        await asyncio.sleep(4)
        await message.delete()
        await msg.delete()
       
    else:
        msg = await message.answer("Перейдіть в особисті повідомлення до бота @pedbot_bot\nі зареєструйтесь за командою /start", reply_markup=ReplyKeyboardRemove())
        await asyncio.sleep(4)
        await message.delete()
        await msg.delete()

#@dp.message_handler(commands=["delete_keyboards"])
async def delete_keyboard(message: types.Message):
    msg = await message.answer("Клавіатуру видалено\n", reply_markup=ReplyKeyboardRemove())
    await asyncio.sleep(4)
    await message.delete()
    await msg.delete()

##@dp.message_handler(commands=["add_keyboards"])
#async def add_keyboard(message: types.Message):
#    if await admin_exists_sql(message.from_user.id):
#        await message.answer("Ваша клавіатура :",reply_markup=kb_admin)
#    elif await user_exists_sql(message.from_user.id):
#        await message.answer("Ваша клавіатура :",reply_markup=kb_client)
#    else:
#        msg = await message.answer("Нажміть /start для регестрації", reply_markup=ReplyKeyboardRemove())
#        await asyncio.sleep(4)
#        await message.delete()
#        await msg.delete()


#===========================реєстратор============================
def register_handler_other(dp : Dispatcher):
    dp.register_message_handler(start,commands=["start"])
    dp.register_message_handler(reg,state = FSMReg.reply_reg)
    dp.register_message_handler(regAdmin,state = FSMReg.password_reg)
    dp.register_message_handler(regUser,state = FSMReg.course_groupe_reg)
    dp.register_message_handler(count_user,commands=["count"])
    dp.register_message_handler(count_group,commands=["countg"])
    dp.register_message_handler(list_group_all,commands=["list"])
    dp.register_message_handler(view_coupes_comm,commands=["coupes"])
    dp.register_message_handler(delete_keyboard,commands=["delete_keyboards"])
    #dp.register_message_handler(add_keyboard,commands=["add_keyboards"])
    