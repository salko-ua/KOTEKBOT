# import
import asyncio

# from import
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.exceptions import MessageIsTooLong
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import *
from data_base import Database
from config import super_admin_admin, super_admin_ura
from create_bot import bot
from handlers.reg import passwords
from aiogram.types import InputFile
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove
import datetime
from translate import Translator

class FSMSuperA(StatesGroup):
    group = State()
    id_student = State()
    id_teachers = State()
    id_student_delete = State()
    id_teachers_delete = State()
    # TEACHERS MANAGMENT
    teachers_name = State()
    teachers_delete = State()
    # GROP MANAGMENT
    curse_group = State()
    curse_group_delete = State()
    # Розклад пар студ
    curse_group_rad = State()
    curse_group_rad_photo = State()
    # Розклад пар викдаж
    teachers_rad = State()
    teachers_rad_photo = State()
    # Розклад дзвінків
    id_photo = State()
    type = State()


# ===========================Список груп============================
# Клавіаура адміна
async def admin_kb(msg: types.Message):
    db = await Database.setup()
    if (
        await db.admin_exists_sql(msg.from_user.id)
        or msg.from_user.id == super_admin_admin
        or msg.from_user.id == super_admin_ura
    ):
        await msg.answer("Клавіатура адміна", reply_markup=kb_admin)


# Клавіаура власника
async def super_admin_kb(msg: types.Message):
    if msg.from_user.id == super_admin_admin or msg.from_user.id == super_admin_ura:
        await msg.answer("Клавіатура власника", reply_markup=sadmin)



# Показати таблицю користувачів
async def super_admin_user(msg: types.Message):
    db = await Database.setup()
    if msg.from_user.id == super_admin_admin or msg.from_user.id == super_admin_ura:
        try:
            booled, data = await db.user_all_sql()
            if booled:
                await msg.answer("Немає користувачів")
            elif not booled:
                await msg.answer(data)
        except MessageIsTooLong:
            for x in range(0, len(data), 4096):
                await bot.send_message(msg.chat.id, data[x : x + 4096])
    else:
        dels = await msg.answer("У тебе немає прав, для перегляду бази данних")
        await asyncio.sleep(4)
        await msg.delete()
        await dels.delete()


# Показати таблицю викладачів
async def super_admin_teach(msg: types.Message):
    db = await Database.setup()
    if msg.from_user.id == super_admin_admin or msg.from_user.id == super_admin_ura:
        try:
            booled, data = await db.teach_all_sql()
            if booled:
                await msg.answer("Немає користувачів")
            elif not booled:
                await msg.answer(data)
        except MessageIsTooLong:
            for x in range(0, len(data), 4096):
                await bot.send_message(msg.chat.id, data[x : x + 4096])
    else:
        dels = await msg.answer("У тебе немає прав, для перегляду бази данних")
        await asyncio.sleep(4)
        await msg.delete()
        await dels.delete()


# Показати користувачів за групою
async def super_admin_user_for_group(msg: types.Message, state: FSMContext):
    if msg.from_user.id == super_admin_admin or msg.from_user.id == super_admin_ura:
        await msg.answer(
            "Введіть групу для перегляду таблиці за цією групою",
            reply_markup=await get_kb(),
        )
        await FSMSuperA.group.set()
    else:
        dels = await msg.answer("У тебе немає прав, для перегляду бази данних")
        await asyncio.sleep(4)
        await msg.delete()
        await dels.delete()


async def super_admin_user_for_group1(msg: types.Message, state: FSMContext):
    db = await Database.setup()
    if msg.from_user.id == super_admin_admin or msg.from_user.id == super_admin_ura:
        if msg.text == "Назад":
            await msg.answer("Меню", reply_markup=sadmin)
            await state.finish()
        else:
            if await db.group_exists_sql(msg.text):
                try:
                    booled, data = await db.user_for_group_sql(msg.text)
                    if booled:
                        await msg.answer("Немає користувачів", reply_markup=sadmin)
                        await state.finish()
                    elif not booled:
                        await msg.answer(data)
                        await msg.answer("Done!", reply_markup=sadmin)
                        await state.finish()
                except MessageIsTooLong:
                    for x in range(0, len(data), 4096):
                        await bot.send_message(msg.chat.id, data[x : x + 4096])
                        await msg.answer("Done!", reply_markup=sadmin)
                        await state.finish()
            else:
                await state.finish()
                dels = await msg.answer(
                    "☹️ Немає такої групи, звяжіться з адміністратором",
                    reply_markup=sadmin,
                )
                await asyncio.sleep(4)
                await msg.delete()
                await dels.delete()
    else:
        dels = await msg.answer("У тебе немає прав, для перегляду бази данних")
        await asyncio.sleep(4)
        await msg.delete()
        await dels.delete()


# ====================================


# Показати таблицю адмінів
async def super_admin_admins(msg: types.Message):
    db = await Database.setup()
    if msg.from_user.id == super_admin_admin or msg.from_user.id == super_admin_ura:
        booled, data = await db.admin_all_sql()
        if booled:
            await msg.answer("Немає адмінів")
        elif not booled:
            await msg.answer(data)
    else:
        dels = await msg.answer("У тебе немає прав, для перегляду бази данних")
        await asyncio.sleep(4)
        await msg.delete()
        await dels.delete()


# ========================================================================================


# Показати студента за id
async def super_admin_user_for_id(msg: types.Message, state: FSMContext):
    if msg.from_user.id == super_admin_admin or msg.from_user.id == super_admin_ura:
        await msg.answer("Введіть ID студента")
        await FSMSuperA.id_student.set()
    else:
        dels = await msg.answer("У тебе немає прав, для перегляду бази данних")
        await asyncio.sleep(4)
        await msg.delete()
        await dels.delete()


async def super_admin_user_for_id1(msg: types.Message, state: FSMContext):
    db = await Database.setup()
    if msg.from_user.id == super_admin_admin or msg.from_user.id == super_admin_ura:
        try:
            booled, text = await db.studen_for_id_sql(msg.text)
            if booled:
                await msg.answer("Немає студента")
                await state.finish()
            elif not booled:
                await msg.answer(text)
                await msg.answer("Done!")
                await state.finish()
        except MessageIsTooLong:
            for x in range(0, len(text), 4096):
                await bot.send_message(msg.chat.id, text[x : x + 4096])
                await msg.answer("Done!")
                await state.finish()
    else:
        dels = await msg.answer("У тебе немає прав, для перегляду бази данних")
        await asyncio.sleep(4)
        await msg.delete()
        await dels.delete()


# Показати викладача за id
async def super_admin_teach_for_id(msg: types.Message):
    db = await Database.setup()
    if msg.from_user.id == super_admin_admin or msg.from_user.id == super_admin_ura:
        await msg.answer("Введіть ID викладача")
        await FSMSuperA.id_teachers.set()
    else:
        dels = await msg.answer("У тебе немає прав, для перегляду бази данних")
        await asyncio.sleep(4)
        await msg.delete()
        await dels.delete()


async def super_admin_teach_for_id1(msg: types.Message, state: FSMContext):
    db = await Database.setup()
    if msg.from_user.id == super_admin_admin or msg.from_user.id == super_admin_ura:
        try:
            booled, text = await db.teach_for_id_sql(msg.text)
            if booled:
                await msg.answer("Немає викладача")
                await state.finish()
            elif not booled:
                await msg.answer(text)
                await msg.answer("Done!")
                await state.finish()
        except MessageIsTooLong:
            for x in range(0, len(text), 4096):
                await bot.send_message(msg.chat.id, text[x : x + 4096])
                await msg.answer("Done!")
                await state.finish()
    else:
        dels = await msg.answer("У тебе немає прав, для перегляду бази данних")
        await asyncio.sleep(4)
        await msg.delete()
        await dels.delete()


# Видалити користувача за id
async def super_admin_delete_user(msg: types.Message):
    if msg.from_user.id == super_admin_admin or msg.from_user.id == super_admin_ura:
        await msg.answer("Введіть ID студента")
        await FSMSuperA.id_student_delete.set()
    else:
        dels = await msg.answer("У тебе немає прав, для перегляду бази данних")
        await asyncio.sleep(4)
        await msg.delete()
        await dels.delete()


async def super_admin_delete_user1(msg: types.Message, state: FSMContext):
    db = await Database.setup()
    if msg.from_user.id == super_admin_admin or msg.from_user.id == super_admin_ura:
        exits = await db.user_exists_sql(msg.text)
        if exits:
            await db.delete_users_sql(msg.text)
            await msg.answer("Студента видаленно")
            await state.finish()
        elif not exits:
            await msg.answer("Немає користувача з таким ID")
            await state.finish()
    else:
        dels = await msg.answer("У тебе немає прав, для перегляду бази данних")
        await asyncio.sleep(4)
        await msg.delete()
        await dels.delete()


# Видалити викладача за id
async def super_admin_delete_teach(msg: types.Message, state: FSMContext):
    if msg.from_user.id == super_admin_admin or msg.from_user.id == super_admin_ura:
        await msg.answer("Введіть ID викладача")
        await FSMSuperA.id_teachers_delete.set()
    else:
        dels = await msg.answer("У тебе немає прав, для перегляду бази данних")
        await asyncio.sleep(4)
        await msg.delete()
        await dels.delete()


async def super_admin_delete_teach1(msg: types.Message, state: FSMContext):
    db = await Database.setup()
    if msg.from_user.id == super_admin_admin or msg.from_user.id == super_admin_ura:
        exits = await db.teachers_exists_sql(msg.text)
        if exits:
            await db.delete_teach_for_id_sql(msg.text)
            await msg.answer("Викладача видаленно")
            await state.finish()
        elif not exits:
            await msg.answer("Немає викладача з таким ID")
            await state.finish()
    else:
        dels = await msg.answer("У тебе немає прав, для перегляду бази данних")
        await asyncio.sleep(4)
        await msg.delete()
        await dels.delete()


async def password(msg: types.Message):
    if msg.from_user.id == super_admin_admin or msg.from_user.id == super_admin_ura:
        await msg.answer(f"PASSWORD : {passwords}")
    else:
        dels = await msg.answer("У тебе немає прав, для перегляду бази данних")
        await asyncio.sleep(4)
        await msg.delete()
        await dels.delete()

async def send_file_db(msg: types.Message):
    if msg.from_user.id == super_admin_admin:
        s = InputFile("data/database.db")
        await bot.send_document(msg.from_user.id, s)

async def delete_stats(msg: types.Message):
    if msg.from_user.id == super_admin_admin:
        name = msg.text[2:]
        db = await Database.setup()
        await db.delete_stats_sql(name)

async def delete_month(message: types.Message):
    if message.from_user.id == super_admin_admin:
        db = await Database.setup()
        await db.delete_month_sql()

async def delete_week(message: types.Message):
    if message.from_user.id == super_admin_admin:
        db = await Database.setup()
        await db.delete_week_sql()

async def create_table(message: types.Message):
    if message.from_user.id == super_admin_admin:
        db = await Database.setup()
        await db.rcreate()


# ===========================Додавання викладача============================
async def add_teachers(message: types.Message):
    db = await Database.setup()
    if (message.from_user.id == super_admin_admin
        or message.from_user.id == super_admin_ura
    ):
        await FSMSuperA.teachers_name.set()
        await message.answer(
            "Введіть ініціали Викладача\nПриклад : Назаров А.М",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)


async def add_teachers1(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if (message.from_user.id == super_admin_admin or message.from_user.id == super_admin_ura):
        if message.text == "Назад":
            await message.answer("Меню", reply_markup=sadmin)
            await state.finish()
        else:
            async with state.proxy() as data:
                data["teachers_name"] = message.text
            fullname = data["teachers_name"]
            if not await db.teachers_name_exists_sql(fullname):
                if len(fullname) <= 15:
                    await db.add_teachers_name_sql(message.from_user.id, fullname)
                    await message.answer("Вчителя додано", reply_markup=sadmin)
                    await state.finish()
                else:
                    await message.answer(
                        "Ініціали вчителя не можуть перевищувати 15 символів",
                        reply_markup=sadmin,
                    )
                    await state.finish()
            else:
                await message.answer(
                    "Вчитель з такою назвою вже є", reply_markup=sadmin
                )
                await state.finish()
    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)
        await state.finish()


# ===========================Видалити викладача============================
async def delete_teachers(message: types.Message):
    db = await Database.setup()
    if (message.from_user.id == super_admin_admin or message.from_user.id == super_admin_ura):
        await FSMSuperA.teachers_delete.set()
        await message.answer(
            "Виберіть вчителя з наведених нижче", reply_markup=await get_t_kb()
        )

    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)


async def delete_teachers1(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if (message.from_user.id == super_admin_admin or message.from_user.id == super_admin_ura):
        if message.text == "Назад":
            await message.answer("Меню", reply_markup=sadmin)
            await state.finish()
        elif message.text != "Назад":
            async with state.proxy() as data:
                data["teachers_delete"] = message.text
            fullname = data["teachers_delete"]
            if await db.teachers_name_exists_sql(fullname):
                if len(fullname) <= 15:
                    if await db.teacher_name_exists_sql(fullname):
                        await db.delete_name_techers_sql(fullname)
                        await db.delete_teachers_name_sql(fullname)
                        await message.answer(
                            "Групу видалено і всіх користувачів які були до неї підключенні",
                            reply_markup=sadmin,
                        )
                    elif not await db.teacher_name_exists_sql(fullname):
                        await db.delete_name_techers_sql(fullname)
                        await message.answer(
                            "викладача видалено", reply_markup=sadmin
                        )
                    await state.finish()
                else:
                    await message.answer(
                        "Назва групи не може перевищувати три символи",
                        reply_markup=sadmin,
                    )
                    await state.finish()
            elif not await db.teachers_name_exists_sql(fullname):
                await message.answer(
                    "Група з такою назвою немає", reply_markup=sadmin
                )
                await state.finish()
    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)
        await state.finish()

# ===========================Додати розклад дзвінків============================
# @dp.message_handler(text ="Додати розклад дзвінків", state=None)
async def add_calls(message: types.Message):
    db = await Database.setup()
    if (message.from_user.id == super_admin_admin or message.from_user.id == super_admin_ura):
        await message.answer("Завантажте фото", reply_markup=ReplyKeyboardRemove())
        await FSMSuperA.id_photo.set()
    elif message.text == "Назад":
        await message.answer("Ваша клавіатура : ", reply_markup=sadmin)
    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)


# @dp.message_handler(content_types=['photo'],state=FSMSuperA.id_photo)
async def add_calls1(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if (message.from_user.id == super_admin_admin or message.from_user.id == super_admin_ura):
        async with state.proxy() as data:
            data["id_photo"] = message.photo[0].file_id
            data["type"] = "calls"
        now = datetime.datetime.now()
        now = now.strftime("%d - %B, %A")
        translation = Translator.translate(now)
        await db.add_calls_sql(
            data["type"], data["id_photo"], "Зміненно: " + translation
        )
        await state.finish()
        await message.answer("Розклад дзвінків успішно оновлено", reply_markup=sadmin)

    elif message.text == "Назад":
        await message.answer("Ваша клавіатура : ", reply_markup=sadmin)

    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)


# ===========================Видалити розклад дзвінків============================
# @dp.message_handler(text ="Видалити розклад дзвінків")
async def delete_calls(message: types.Message):
    db = await Database.setup()
    if (message.from_user.id == super_admin_admin or message.from_user.id == super_admin_ura):
        check = await db.delete_calls_sql()
        if not check:
            await message.answer(
                "Розкладу дзвінків ще не додано", reply_markup=sadmin
            )
        elif check:
            await message.answer(
                "Розклад дзвінків успішно видалено", reply_markup=sadmin
            )
    elif message.text == "Назад":
        await message.answer("Ваша клавіатура : ", reply_markup=sadmin)
    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)

# ===========================Видалити групу============================
# @dp.message_handler(text ="Видалити групу", state=None)
async def delete_group(message: types.Message):
    db = await Database.setup()
    if (message.from_user.id == super_admin_admin or message.from_user.id == super_admin_ura):
        await FSMSuperA.curse_group_delete.set()
        await message.answer(
            "Виберіть групу з наведених нижче", reply_markup=await get_kb()
        )

    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)


# @dp.message_handler(state=FSMSuperA.curse_group_delete)
async def load_group(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if (message.from_user.id == super_admin_admin or message.from_user.id == super_admin_ura):
        if message.text == "Назад":
            await message.answer("Меню", reply_markup=sadmin)
            await state.finish()
        elif message.text != "Назад":
            async with state.proxy() as data:
                data["curse_group_delete"] = message.text
            fullname = data["curse_group_delete"]
            if await db.group_exists_sql(fullname):
                if len(fullname) <= 3:
                    if await db.user_group_exists_sql(fullname):
                        await db.delete_groups_sql(fullname)
                        await db.delete_user_groups_sql(fullname)
                        await message.answer(
                            "Групу видалено і всіх користувачів які були до неї підключенні",
                            reply_markup=sadmin,
                        )

                    elif not await db.user_group_exists_sql(fullname):
                        await db.delete_groups_sql(fullname)
                        await message.answer("Групу видалено", reply_markup=sadmin)
                    await state.finish()
                else:
                    await message.answer(
                        "Назва групи не може перевищувати три символи",
                        reply_markup=sadmin,
                    )
                    await state.finish()
            else:
                await message.answer(
                    "Група з такою назвою немає", reply_markup=sadmin
                )
                await state.finish()
    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)
        await state.finish()



# ===========================Додавання групи============================
# @dp.message_handler(text="Додати групу", state=None)
async def add_group(message: types.Message):
    db = await Database.setup()
    if (message.from_user.id == super_admin_admin or message.from_user.id == super_admin_ura):
        await FSMSuperA.curse_group.set()
        await message.answer(
            "Введіть назву\nПриклад : 2Ц", reply_markup=ReplyKeyboardRemove()
        )

    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)


# @dp.message_handler(state=FSMSuperA.curse_group)
async def add_group1(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if (message.from_user.id == super_admin_admin or message.from_user.id == super_admin_ura):
        if message.text == "Назад":
            await message.answer("Меню", reply_markup=sadmin)
            await state.finish()
        else:
            async with state.proxy() as data:
                data["curse_group"] = message.text
            fullname = data["curse_group"]
            if not await db.group_exists_sql(fullname):
                if len(fullname) <= 3:
                    await db.add_group_sql(message.from_user.id, fullname)
                    await message.answer("Групу додано", reply_markup=sadmin)
                    await state.finish()
                else:
                    await message.answer(
                        "Назва групи не може перевищувати три символи",
                        reply_markup=sadmin,
                    )
                    await state.finish()
            else:
                await message.answer(
                    "Група з такою назвою вже є", reply_markup=sadmin
                )
                await state.finish()
    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)
        await state.finish()


# ===========================Додати розклад до курсу============================
# @dp.message_handler(text="Додати розклад до групи", state=None)
async def add_schedule_to_group(message: types.Message):
    db = await Database.setup()
    if (message.from_user.id == super_admin_admin or message.from_user.id == super_admin_ura):
        await FSMSuperA.curse_group_rad_photo.set()
        await message.answer("Киньте фото розкладу", reply_markup=ReplyKeyboardRemove())

    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)


# @dp.message_handler(content_types=['photo'],state=FSMSuperA.curse_group_rad_photo)
async def add_schedule_to_group1(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if (message.from_user.id == super_admin_admin or message.from_user.id == super_admin_ura):
        async with state.proxy() as data:
            data["curse_group_rad_photo"] = message.photo[0].file_id
        await FSMSuperA.curse_group_rad.set()
        await message.answer("До якої групи привязати", reply_markup=await get_kb())

    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)
        await state.finish()


# @dp.message_handler(state=FSMSuperA.curse_group_rad)
async def add_schedule_to_group2(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if (message.from_user.id == super_admin_admin or message.from_user.id == super_admin_ura):
        async with state.proxy() as data:
            data["curse_group_rad"] = message.text
        now = datetime.datetime.now()
        now = now.strftime("%d - %B, %A")
        translation = Translator.translate(now)
        await db.group_photo_update_sql(
            data["curse_group_rad_photo"],
            data["curse_group_rad"],
            "Зміненно: " + translation,
        )
        await message.answer("Розклад успішно добавлено", reply_markup=sadmin)
        await state.finish()
    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)
        await state.finish()


# ===========================Додати розклад викладачу============================
async def add_schedule_to_teacher(message: types.Message):
    db = await Database.setup()
    if (message.from_user.id == super_admin_admin or message.from_user.id == super_admin_ura):
        await FSMSuperA.teachers_rad_photo.set()
        await message.answer("Киньте фото розкладу", reply_markup=ReplyKeyboardRemove())

    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)


async def add_schedule_to_teacher1(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if (message.from_user.id == super_admin_admin or message.from_user.id == super_admin_ura):
        async with state.proxy() as data:
            data["teachers_rad_photo"] = message.photo[0].file_id
        await FSMSuperA.teachers_rad.set()
        await message.answer("До якої групи привязати", reply_markup=await get_t_kb())

    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)
        await state.finish()


async def add_schedule_to_teacher2(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if (message.from_user.id == super_admin_admin or message.from_user.id == super_admin_ura):
        async with state.proxy() as data:
            data["teachers_rad"] = message.text
        now = datetime.datetime.now()
        now = now.strftime("%d - %B, %A")
        translation = Translator.translate(now)
        await db.teacher_photo_update_sql(
            data["teachers_rad_photo"], data["teachers_rad"], "Зміненно: " + translation
        )
        await message.answer("Розклад успішно добавлено", reply_markup=sadmin)
        await state.finish()
    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)
        await state.finish()











# ===========================реєстратор============================
def register_handler_sadmin(dp: Dispatcher):
    dp.register_message_handler(password, text="p")
    dp.register_message_handler(admin_kb, text="Адмін 🔑")
    dp.register_message_handler(super_admin_kb, text="власник")
    dp.register_message_handler(super_admin_user, text="таблиця студентів")
    dp.register_message_handler(super_admin_teach, text="таблиця викладачів")
    dp.register_message_handler(super_admin_admins, text="таблиця адмінів")
    dp.register_message_handler(send_file_db, text="db")
    dp.register_message_handler(delete_stats, Text(startswith="d"))
    dp.register_message_handler(delete_month, commands=["mouth"])
    dp.register_message_handler(delete_week, commands=["week"])
    dp.register_message_handler(create_table, commands=["update"])


    dp.register_message_handler(
        super_admin_user_for_group, text="таблиця за групою", state=None
    )
    dp.register_message_handler(super_admin_user_for_group1, state=FSMSuperA.group)

    dp.register_message_handler(
        super_admin_user_for_id, text="Студент за ID", state=None
    )
    dp.register_message_handler(super_admin_user_for_id1, state=FSMSuperA.id_student)

    dp.register_message_handler(
        super_admin_teach_for_id, text="Викладач за ID", state=None
    )
    dp.register_message_handler(super_admin_teach_for_id1, state=FSMSuperA.id_teachers)

    dp.register_message_handler(
        super_admin_delete_user, text="Видалити студента", state=None
    )
    dp.register_message_handler(
        super_admin_delete_user1, state=FSMSuperA.id_student_delete
    )

    dp.register_message_handler(
        super_admin_delete_teach, text="Видалити викладача", state=None
    )
    dp.register_message_handler(
        super_admin_delete_teach1, state=FSMSuperA.id_teachers_delete
    )

    # ===========================Додати викладача=============================
    dp.register_message_handler(add_teachers, text="викладача ❇️", state=None)
    dp.register_message_handler(add_teachers1, state=FSMSuperA.teachers_name)

    # ===========================Видалити викладача==============================
    dp.register_message_handler(delete_teachers, text="викладача 🗑", state=None)
    dp.register_message_handler(delete_teachers1, state=FSMSuperA.teachers_delete)

    # ===========================Додавання групи=============================
    dp.register_message_handler(add_group, text="групу ❇️", state=None)
    dp.register_message_handler(add_group1, state=FSMSuperA.curse_group)
    # ===========================Видалити групу==============================
    dp.register_message_handler(delete_group, text="групу 🗑", state=None)
    dp.register_message_handler(load_group, state=FSMSuperA.curse_group_delete)
    # ===========================Додати розклад до курсу=====================
    dp.register_message_handler(add_schedule_to_group, text="групі ❇️", state=None)
    dp.register_message_handler(
        add_schedule_to_group1,
        content_types=["photo"],
        state=FSMSuperA.curse_group_rad_photo,
    )
    dp.register_message_handler(add_schedule_to_group2, state=FSMSuperA.curse_group_rad)
    # ===========================Додати розклад викладачу=====================
    dp.register_message_handler(
        add_schedule_to_teacher, text="викладачу ❇️", state=None
    )
    dp.register_message_handler(
        add_schedule_to_teacher1,
        content_types=["photo"],
        state=FSMSuperA.teachers_rad_photo,
    )
    dp.register_message_handler(add_schedule_to_teacher2, state=FSMSuperA.teachers_rad)

    # ===========================Додати розклад дзвінків======================
    dp.register_message_handler(add_calls, text="дзвінків ❇️", state=None)
    dp.register_message_handler(
        add_calls1, content_types=["photo"], state=FSMSuperA.id_photo
    )
    # ===========================Видалити розклад дзвінків============================
    dp.register_message_handler(delete_calls, text="дзвінків 🗑")
