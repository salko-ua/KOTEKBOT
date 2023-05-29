# import
import asyncache
import cachetools

# from import
from aiogram import types
from data_base import Database
from random import choice
from keyboards import *

from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from handlers.stats import stats_schedule_add
from handlers.menu import menu

from aiogram.dispatcher.filters import Text, ChatTypeFilter

from aiogram.dispatcher.filters.state import State, StatesGroup


# =========Класс машини стану=========
class FSMReg(StatesGroup):
    course_groupe_reg = State()
    teachers_reg = State()
    password_reg = State()
    reply_reg = State()

@asyncache.cached(cachetools.TTLCache(1, 120))
async def password_for_admin():
    password = ""
    for x in range(8): 
        password = password + choice(list('1234567890ABCDEFGHIGKLMNOPQRSTUVYXWZ'))
    return password


# ===========================Реєстрація ⚙️============================
async def registration(message: types.Message):
    db = await Database.setup()
    if message.text == "Розклад ⚙️":
        await stats_schedule_add("Розклад ⚙️", 1)

    if await db.user_exists_sql(message.from_user.id):
        await message.answer("Ваша клавіатура ⌨️", reply_markup=kb_client)

    elif await db.teachers_exists_sql(message.from_user.id):
        await message.answer("Ваша клавіатура ⌨️", reply_markup=kb_teachers)

    elif await db.admin_exists_sql(message.from_user.id):
        await message.answer("Виберіть тип акаунту ⬇️", reply_markup=kb_choice)
        await FSMReg.reply_reg.set()

    else:
        await message.answer("Виберіть тип акаунту ⬇️", reply_markup=kb_choice)
        await FSMReg.reply_reg.set()

async def reg(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if message.text == "Меню 👥":
        await menu(message)
        await state.finish()

    elif message.text == "Адміністратор 🔐":
        await FSMReg.password_reg.set()
        await message.answer("🔒 Введіть пароль 🔑", reply_markup=ReplyKeyboardRemove())

    elif message.text == "Студент 👩‍🎓":
        await FSMReg.course_groupe_reg.set()
        await message.answer("⬇️ Введіть курс і групу з наведених нижче", reply_markup=await get_kb())

    elif message.text == "Викладач 👨‍🏫":
        await FSMReg.teachers_reg.set()
        await message.answer("⬇️ Введіть ініціали з наведених нижче", reply_markup=await get_t_kb())
    
    else:
        await message.answer("☹️ Немає такої відповіді ☹️")
    
    
async def regAdmin(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if message.text == "Меню 👥":
        await menu(message)
        await state.finish()
        
    elif message.text == await password_for_admin():
        if await db.admin_exists_sql(message.from_user.id):
            await message.answer("Ви вже адмін", reply_markup=kb_start_admin)
            await state.finish()
        else:
            first_name = message.from_user.first_name
            username = message.from_user.username
            user_id = message.from_user.id
            await db.add_admin_sql(user_id, first_name, username)
            await message.answer("✅ Реєстрація завершена ✅", reply_markup=kb_admin)
            await state.finish()
    else:
        await message.answer("☹️ пароль неправильний ☹️", reply_markup=kb_start)
        await state.finish()


async def regUser(message: types.Message, state: FSMContext):
    db = await Database.setup()
    first_name = message.from_user.first_name
    username = message.from_user.username
    groupe = message.text

    if message.text == "Меню 👥":
        await menu(message)
        await state.finish()

    elif await db.group_exists_sql(message.text):
        await db.add_user_sql(message.from_user.id, first_name, username, groupe)
        await state.finish()
        await message.answer("✅ Реєстрація завершена ✅", reply_markup=kb_client)

    else:
        await message.answer("☹️ Немає такої групи у списку☹️", reply_markup=kb_start,)
        await state.finish()


async def regTeachers(message: types.Message, state: FSMContext):
    db = await Database.setup()
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    username = message.from_user.username
    group_teacher = message.text

    if message.text == "Меню 👥":
        await menu(message)
        await state.finish()
        
    elif await db.teachers_name_exists_sql(message.text):
        await db.add_teachers_sql(user_id, first_name, username, group_teacher)
        await state.finish()
        await message.answer("✅ Реєстрація завершена ✅", reply_markup=kb_teachers)

    else:
        await message.answer("☹️ Немає такого вчителя у списку☹️",reply_markup=kb_start)
        await state.finish()


text = {
    "registration": [
        "Реєстрація ⚙️",
        "Розклад ⚙️",
        "Reg",
        "registration",
        "Реєстрація",
        "Розклад",
]}


# ===========================реєстратор============================
def register_handler_reg(dp: Dispatcher):
    # Реєстрація
    dp.register_message_handler(
        registration,
        Text(ignore_case=True, equals=text["registration"]),
        ChatTypeFilter("private"),
        state=None,)
    dp.register_message_handler(reg, state=FSMReg.reply_reg)
    dp.register_message_handler(regAdmin, state=FSMReg.password_reg)
    dp.register_message_handler(regUser, state=FSMReg.course_groupe_reg)
    dp.register_message_handler(regTeachers, state=FSMReg.teachers_reg)