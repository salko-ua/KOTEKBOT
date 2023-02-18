from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardRemove
from config import super_admin
from keyboards import *
from data_base.controller_db import *


#===========================Переглянути розклад============================
#@dp.message_handler(text = "Переглянути розклад пар")
async def view_coupes(message: types.Message):
    if await user_exists_sql(message.from_user.id):
        ids = message.from_user.id
        
        if await see_rod_sql(str(ids)):
            await message.answer_photo(photka.get(),date_coupes.get())
        elif await see_rod_sql(str(ids)) == False:
            await message.answer('☹️Розкладу для вашої групи ще немає...☹️')  
    elif not await user_exists_sql(message.from_user.id):
        await message.answer("❗️Нажміть /start для регестрації❗️", reply_markup=ReplyKeyboardRemove())


#===========================Змінити групу============================
#@dp.message_handler(text = "Переглянути розклад дзвінків")
async def view_calls(message: types.Message):
    if await user_exists_sql(message.from_user.id) or super_admin == message.from_user.id:
        check = await see_calls_sql()
        if not check:
            await message.answer("☹️Розклад дзвінків ще не додано☹️")
        elif check:
            await see_calls_sql()
            await message.answer_photo(id_photka.get(),date_calls.get())
    elif not await user_exists_sql(message.from_user.id):
        await message.answer("❗️Нажміть /start для регестрації❗️", reply_markup=ReplyKeyboardRemove())


#===========================Змінити групу============================
#@dp.message_handler(text = "Змінити групу")
async def delete_user(message: types.Message):
    if await user_exists_sql(message.from_user.id):
        await delete_users_sql(message.from_user.id)
        await message.answer("Нажміть /start щоб вибрати іншу групу :D", reply_markup=ReplyKeyboardRemove())
    elif not await user_exists_sql(message.from_user.id):
        await message.answer("🌚Ви і так не зареєстрованні\nНажміть /start для регестрації", reply_markup=ReplyKeyboardRemove())

#===========================Пустий хендлер============================
#@dp.message_handler()
async def all_text(message: types.Message):
    if message.text == "Переглянути розклад пар" or message.text == "Переглянути розклад дзвінків":
        await message.answer("Бот оновився, ця клавіатура\nзастаріла натисніть /start\nдля оновлення")
    elif message.text == "Назад" and await admin_exists_sql(message.from_user.id):
        await message.answer("Ваша клавіатура ⌨️",reply_markup=kb_admin)
    elif message.text == "Назад" and await user_exists_sql(message.from_user.id):
        await message.answer("Ваша клавіатура ⌨️",reply_markup=kb_client)
    elif message.text == "Назад" and message.from_user.id == super_admin:
        await message.answer("Ваша клавіатура ⌨️", reply_markup=sadmin)
    


#===========================реєстратор============================
def register_handler_client(dp : Dispatcher):
        dp.register_message_handler(view_coupes,text = "Розклад пар")
        dp.register_message_handler(view_calls,text = "Розклад дзвінків")
        dp.register_message_handler(delete_user,text = "Змінити групу")
        dp.register_message_handler(all_text)