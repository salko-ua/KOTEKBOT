# import
import asyncio

# from import
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import (
    MessageToDeleteNotFound,
    MessageCantBeDeleted,
    BadRequest,
)
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text, ChatTypeFilter
from keyboards import *
from random import randint as rd
from handlers.stats import stats_schedule_add
from data_base import Database

passwords = (
    str(rd(1, 9))
    + str(rd(1, 9))
    + str(rd(1, 9))
    + str(rd(1, 9))
    + str(rd(1, 9))
    + str(rd(1, 9))
    + str(rd(1, 9))
    + str(rd(1, 9))
)


# =========Класс машини стану=========
class FSMReg(StatesGroup):
    course_groupe_reg = State()
    teachers_reg = State()
    password_reg = State()
    reply_reg = State()


# ===========================Реєстрація ⚙️============================
async def registration(message: types.Message):
    db = await Database.setup()
    if message.text == "Розклад ⚙️":
        await stats_schedule_add("Розклад ⚙️", 1)
    if (
        (not await db.user_exists_sql(message.from_user.id))
        and (not await db.admin_exists_sql(message.from_user.id))
        and (not await db.teachers_exists_sql(message.from_user.id))
    ):
        if message.chat.type == "private":
            await message.answer(
                "🤔 Реєстрація 🤔\nВиберіть тип акаунту ⬇️", reply_markup=kb_choice
            )
            await FSMReg.reply_reg.set()
        else:
            try:
                msg = await message.answer(
                    "🤨 Перейдіть в особисті повідомлення до @pedbot_bot\nі зареєструйтесь за командою /start"
                )
                await asyncio.sleep(2)
                await message.delete()
                await msg.delete()
            except (MessageToDeleteNotFound, MessageCantBeDeleted, BadRequest):
                await message.answer(
                    "Помилка, я не можу автовидалити своє повідомлення, мені потрібні права адміна"
                )
    elif await db.user_exists_sql(message.from_user.id):
        if message.chat.type == "private":
            await message.answer("Ваша клавіатура ⌨️", reply_markup=kb_client)
        else:
            try:
                msg = await message.answer("⚠️ Ви зареєстрованні")
                await asyncio.sleep(2)
                await message.delete()
                await msg.delete()
            except (MessageToDeleteNotFound, MessageCantBeDeleted, BadRequest):
                await message.answer(
                    "Помилка, я не можу автовидалити своє повідомлення, мені потрібні права адміна"
                )
    elif await db.teachers_exists_sql(message.from_user.id):
        if message.chat.type == "private":
            await message.answer("Ваша клавіатура ⌨️", reply_markup=kb_teachers)
        else:
            try:
                msg = await message.answer("⚠️ Ви зареєстрованні")
                await asyncio.sleep(2)
                await message.delete()
                await msg.delete()
            except (MessageToDeleteNotFound, MessageCantBeDeleted, BadRequest):
                await message.answer(
                    "Помилка, я не можу автовидалити своє повідомлення, мені потрібні права адміна"
                )
    elif await db.admin_exists_sql(message.from_user.id):
        if message.chat.type == "private":
            await message.answer(
                "🤔 Реєстрація 🤔\nВиберіть тип акаунту ⬇️", reply_markup=kb_choice
            )
            await FSMReg.reply_reg.set()
        else:
            try:
                msg = await message.answer(
                    "🤨 Перейдіть в особисті повідомлення до @pedbot_bot\nі зареєструйтесь за командою /start"
                )
                await asyncio.sleep(2)
                await message.delete()
                await msg.delete()
            except (MessageToDeleteNotFound, MessageCantBeDeleted, BadRequest):
                await message.answer(
                    "Помилка, я не можу автовидалити своє повідомлення, мені потрібні права адміна"
                )


async def reg(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if message.text == "Назад":
        await state.finish()
        if await db.admin_exists_sql(message.from_user.id):
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start_admin)
        elif await db.user_exists_sql(message.from_user.id):
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start_user)
        elif await db.teachers_exists_sql(message.from_user.id):
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start_user)
        else:
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start)
    elif message.text == "Адміністратор 🔐":
        await FSMReg.password_reg.set()
        await message.answer("🔒 Введіть пароль 🔑", reply_markup=ReplyKeyboardRemove())
    elif message.text == "Студент 👩‍🎓":
        await FSMReg.course_groupe_reg.set()
        await message.answer(
            "⬇️ Введіть курс і групу з наведених нижче", reply_markup=await get_kb()
        )
    elif message.text == "Викладач 👨‍🏫":
        await FSMReg.teachers_reg.set()
        await message.answer(
            "⬇️ Введіть ініціали з наведених нижче", reply_markup=await get_t_kb()
        )
    else:
        await message.answer("☹️ Немає такої відповіді ☹️", reply_markup=kb_start)
        await state.finish()


async def regAdmin(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if message.text == "Назад":
        await state.finish()
        if await db.admin_exists_sql(message.from_user.id):
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start_admin)
        elif await db.user_exists_sql(message.from_user.id):
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start_user)
        elif await db.teachers_exists_sql(message.from_user.id):
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start_user)
        else:
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start)
    elif message.text == passwords:
        if await db.admin_exists_sql(message.from_user.id):
            await message.answer("Ви вже адмін", reply_markup=kb_start_admin)
            await state.finish()
        else:
            first_name = message.from_user.first_name
            username = message.from_user.username
            await db.add_admin_sql(message.from_user.id, first_name, username)
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
    if message.text == "Назад":
        await state.finish()
        if await db.admin_exists_sql(message.from_user.id):
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start_admin)
        elif await db.user_exists_sql(message.from_user.id):
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start_user)
        elif await db.teachers_exists_sql(message.from_user.id):
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start_user)
        else:
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start)
    elif await db.group_exists_sql(message.text):
        await db.add_user_sql(message.from_user.id, first_name, username, groupe)
        await state.finish()
        await message.answer("✅ Реєстрація завершена ✅", reply_markup=kb_client)
    else:
        await message.answer(
            "☹️ Немає такої групи, звяжіться з адміністратором\nдля того щоб її додали \nІ повторіть спробу",
            reply_markup=kb_start,
        )
        await state.finish()


async def regTeachers(message: types.Message, state: FSMContext):
    db = await Database.setup()
    first_name = message.from_user.first_name
    username = message.from_user.username
    teachers_name = message.text
    if message.text == "Назад":
        await state.finish()
        if await db.admin_exists_sql(message.from_user.id):
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start_admin)
        elif await db.user_exists_sql(message.from_user.id):
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start_user)
        elif await db.teachers_exists_sql(message.from_user.id):
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start_user)
        else:
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start)
    elif await db.teachers_name_exists_sql(message.text):
        await db.add_teachers_sql(
            message.from_user.id, first_name, username, teachers_name
        )
        await state.finish()
        await message.answer("✅ Реєстрація завершена ✅", reply_markup=kb_teachers)
    else:
        await message.answer(
            "☹️ Немає такого вчителя, звяжіться з адміністратором\nдля того щоб його додали \nІ повторіть спробу",
            reply_markup=kb_start,
        )
        await state.finish()


text = {
    "registration": [
        "Реєстрація ⚙️",
        "Розклад ⚙️",
        "Reg",
        "registration",
        "Реєстрація",
        "Розклад",
    ],
}


# ===========================реєстратор============================
def register_handler_reg(dp: Dispatcher):
    # Реєстрація
    dp.register_message_handler(
        registration,
        Text(ignore_case=True, equals=text["registration"]),
        ChatTypeFilter("private"),
        state=None,
    )
    dp.register_message_handler(reg, state=FSMReg.reply_reg)
    dp.register_message_handler(regAdmin, state=FSMReg.password_reg)
    dp.register_message_handler(regUser, state=FSMReg.course_groupe_reg)
    dp.register_message_handler(regTeachers, state=FSMReg.teachers_reg)
