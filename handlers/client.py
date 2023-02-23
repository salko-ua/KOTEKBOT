from aiogram import types
from aiogram.dispatcher import Dispatcher
from config import super_admin_admin, super_admin_ura
from keyboards import *
from data_base.controller_db import *
import datetime

#===========================Переглянути розклад============================
async def view_coupes(message: types.Message):
    if await user_exists_sql(message.from_user.id):
        ids = message.from_user.id
        if await see_rod_sql(str(ids)):
            await message.answer_photo(photka.get(),date_coupes.get())
        elif await see_rod_sql(str(ids)) == False:
            await message.answer('☹️Розкладу для вашої групи ще немає...☹️')
    elif await teachers_exists_sql(message.from_user.id):
        ids = message.from_user.id
        if await see_rod_t_sql(str(ids)):
            await message.answer_photo(photka_teachers.get(),date_coupes.get())
        elif await see_rod_t_sql(str(ids)) == False:
            await message.answer('☹️Розкладу для ваc ще немає...☹️')
    elif not await user_exists_sql(message.from_user.id) and not await teachers_exists_sql(message.from_user.id):
        await message.answer("❗️Нажміть кнопку реєстрації❗️", reply_markup= kb_start)

#===========================Змінити групу============================
async def view_calls(message: types.Message):
    if await user_exists_sql(message.from_user.id) or  message.from_user.id == super_admin_admin or super_admin_ura == message.from_user.id or await teachers_exists_sql(message.from_user.id):
        check = await see_calls_sql()
        if not check:
            await message.answer("☹️Розклад дзвінків ще не додано☹️")
        elif check:
            await see_calls_sql()
            await message.answer_photo(id_photka.get(),date_calls.get())
    elif not await user_exists_sql(message.from_user.id) and not await teachers_exists_sql(message.from_user.id):
        await message.answer("❗️Нажміть кнопку реєстрації❗️", reply_markup= kb_start)

#===========================Змінити групу============================
async def delete_user(message: types.Message):
    if await user_exists_sql(message.from_user.id):
        if await admin_exists_sql(message.from_user.id):
            await delete_users_sql(message.from_user.id)
            await message.answer("🙂Зареєструйтесь знову🙂", reply_markup=kb_start_admin)
        else:
            await delete_users_sql(message.from_user.id)
            await message.answer("🙂Зареєструйтесь знову🙂", reply_markup=kb_start)
    elif await teachers_exists_sql(message.from_user.id):
        if await admin_exists_sql(message.from_user.id):
            await delete_teachers_sql(message.from_user.id)
            await message.answer("🙂Зареєструйтесь знову🙂", reply_markup=kb_start_admin)
        else:
            await delete_teachers_sql(message.from_user.id)
            await message.answer("🙂Зареєструйтесь знову🙂", reply_markup=kb_start)
    elif not await user_exists_sql(message.from_user.id) and not await teachers_exists_sql(message.from_user.id):
        await message.answer("🌚Ви і так не зареєстрованні\nНажміть кнопку реєстрації", reply_markup=kb_start)

#=========================== Дріб ===========================
async def fraction(message: types.Message):
    today = datetime.date.today()
    week_number = today.isocalendar()[1]
    if week_number % 2 == 0:
        await message.answer("Цей тиждень - <b>знаменник</b> 🫡",parse_mode="HTML")
    elif week_number % 2 != 0:
        await message.answer("Цей тиждень - <b>чисельник</b> 🫡",parse_mode="HTML")


#===========================Пустий хендлер============================
#@dp.message_handler()
async def all_text(message: types.Message):
    if message.text == "Переглянути розклад пар" or message.text == "Переглянути розклад дзвінків" or message.text == "Змінити групу" or message.text == "розклад дзвінків" or message.text == "розклад пар":
        await message.answer("Бот оновився, оновлення завантажено ⬇️",reply_markup = kb_start_user)
    elif await admin_exists_sql(message.from_user.id) and message.text == "Адмін 🔑":
        await message.answer("Адмінська частина", reply_markup = kb_admin)
    elif message.text == "⬅️ Назад":
        await message.answer("⬇️Головне меню⬇️", reply_markup = kb_infs)
#    elif message.text == "Назад" and await admin_exists_sql(message.from_user.id):
#        await message.answer("Ваша клавіатура ⌨️",reply_markup=kb_admin)
#    elif message.text == "Назад" and await user_exists_sql(message.from_user.id):
#        await message.answer("Ваша клавіатура ⌨️",reply_markup=kb_client)
#    elif message.text == "Назад" and message.from_user.id == super_admin_admin or message.from_user.id == super_admin_ura:
#        await message.answer("Ваша клавіатура ⌨️", reply_markup=sadmin)
    


#===========================реєстратор============================
def register_handler_client(dp : Dispatcher):
        dp.register_message_handler(view_coupes,text = ["Розклад пар 🥱","Розклад занять 🥱"])
        dp.register_message_handler(view_calls,text = "Розклад дзвінків ⌚️")
        dp.register_message_handler(delete_user,text = ["Переєструватись 🤨"])
        dp.register_message_handler(fraction,text = ["Ч/З 🤨"])
        dp.register_message_handler(all_text)