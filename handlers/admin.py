from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import BotBlocked
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboards import (
    kb_admin,
    kb_all_or_one,
    get_kb,
    get_t_kb,
    kb_dont,
    kb_ys,
    kb_start,
    kb_start_admin,
    kb_start_user,
    kb_start,
)
import asyncio
from aiogram.types import ReplyKeyboardRemove
import datetime
from create_bot import bot
from translate import Translator
from config import super_admin_admin, super_admin_ura
from data_base import Database

translator = Translator(to_lang="uk")


# =========Класс машини стану=========
class FSMAdmin(StatesGroup):
    # GROP MANAGMENT
    curse_group = State()
    curse_group_delete = State()
    # TEACHERS MANAGMENT
    teachers_name = State()
    teachers_delete = State()
    # Розклад пар студ
    curse_group_rad = State()
    curse_group_rad_photo = State()
    # Розклад пар викдаж
    teachers_rad = State()
    teachers_rad_photo = State()
    # NEWS
    all_or_one = State()
    text_news = State()
    photo_news = State()
    namegroups = State()
    # Розклад дзвінків
    id_photo = State()
    type = State()


# ===========================Додавання викладача============================
async def add_teachers(message: types.Message):
    db = await Database.setup()
    if (
        await db.admin_exists_sql(message.from_user.id)
        or message.from_user.id == super_admin_admin
        or message.from_user.id == super_admin_ura
    ):
        await FSMAdmin.teachers_name.set()
        await message.answer(
            "Введіть ініціали Викладача\nПриклад : Назаров А.М",
            reply_markup=ReplyKeyboardRemove(),
        )

    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)


async def add_teachers1(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if (
        await db.admin_exists_sql(message.from_user.id)
        or message.from_user.id == super_admin_admin
        or message.from_user.id == super_admin_ura
    ):
        if message.text == "Назад":
            await message.answer("Меню", reply_markup=kb_admin)
            await state.finish()
        else:
            async with state.proxy() as data:
                data["teachers_name"] = message.text
            fullname = data["teachers_name"]
            if not await db.teachers_name_exists_sql(fullname):
                if len(fullname) <= 15:
                    await db.add_teachers_name_sql(message.from_user.id, fullname)
                    await message.answer("Вчителя додано", reply_markup=kb_admin)
                    await state.finish()
                else:
                    await message.answer(
                        "Ініціали вчителя не можуть перевищувати 15 символів",
                        reply_markup=kb_admin,
                    )
                    await state.finish()
            else:
                await message.answer(
                    "Вчитель з такою назвою вже є", reply_markup=kb_admin
                )
                await state.finish()
    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)
        await state.finish()


# ===========================Видалити викладача============================
async def delete_teachers(message: types.Message):
    db = await Database.setup()
    if (
        await db.admin_exists_sql(message.from_user.id)
        or message.from_user.id == super_admin_admin
        or message.from_user.id == super_admin_ura
    ):
        await FSMAdmin.teachers_delete.set()
        await message.answer(
            "Виберіть вчителя з наведених нижче", reply_markup=await get_t_kb()
        )

    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)


async def delete_teachers1(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if (
        await db.admin_exists_sql(message.from_user.id)
        or message.from_user.id == super_admin_admin
        or message.from_user.id == super_admin_ura
    ):
        if message.text == "Назад":
            await message.answer("Меню", reply_markup=kb_admin)
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
                            reply_markup=kb_admin,
                        )
                    elif not await db.teacher_name_exists_sql(fullname):
                        await db.delete_name_techers_sql(fullname)
                        await message.answer(
                            "викладача видалено", reply_markup=kb_admin
                        )
                    await state.finish()
                else:
                    await message.answer(
                        "Назва групи не може перевищувати три символи",
                        reply_markup=kb_admin,
                    )
                    await state.finish()
            elif not await db.teachers_name_exists_sql(fullname):
                await message.answer(
                    "Група з такою назвою немає", reply_markup=kb_admin
                )
                await state.finish()
    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)
        await state.finish()


# ===========================Додавання групи============================
# @dp.message_handler(text="Додати групу", state=None)
async def add_group(message: types.Message):
    db = await Database.setup()
    if (
        await db.admin_exists_sql(message.from_user.id)
        or message.from_user.id == super_admin_admin
        or message.from_user.id == super_admin_ura
    ):
        await FSMAdmin.curse_group.set()
        await message.answer(
            "Введіть назву\nПриклад : 2Ц", reply_markup=ReplyKeyboardRemove()
        )

    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)


# @dp.message_handler(state=FSMAdmin.curse_group)
async def add_group1(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if (
        await db.admin_exists_sql(message.from_user.id)
        or message.from_user.id == super_admin_admin
        or message.from_user.id == super_admin_ura
    ):
        if message.text == "Назад":
            await message.answer("Меню", reply_markup=kb_admin)
            await state.finish()
        else:
            async with state.proxy() as data:
                data["curse_group"] = message.text
            fullname = data["curse_group"]
            if not await db.group_exists_sql(fullname):
                if len(fullname) <= 3:
                    await db.add_group_sql(message.from_user.id, fullname)
                    await message.answer("Групу додано", reply_markup=kb_admin)
                    await state.finish()
                else:
                    await message.answer(
                        "Назва групи не може перевищувати три символи",
                        reply_markup=kb_admin,
                    )
                    await state.finish()
            else:
                await message.answer(
                    "Група з такою назвою вже є", reply_markup=kb_admin
                )
                await state.finish()
    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)
        await state.finish()


# ===========================Додати розклад до курсу============================
# @dp.message_handler(text="Додати розклад до групи", state=None)
async def add_schedule_to_group(message: types.Message):
    db = await Database.setup()
    if (
        await db.admin_exists_sql(message.from_user.id)
        or message.from_user.id == super_admin_admin
        or message.from_user.id == super_admin_ura
    ):
        await FSMAdmin.curse_group_rad_photo.set()
        await message.answer("Киньте фото розкладу", reply_markup=ReplyKeyboardRemove())

    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)


# @dp.message_handler(content_types=['photo'],state=FSMAdmin.curse_group_rad_photo)
async def add_schedule_to_group1(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if (
        await db.admin_exists_sql(message.from_user.id)
        or message.from_user.id == super_admin_admin
        or message.from_user.id == super_admin_ura
    ):
        async with state.proxy() as data:
            data["curse_group_rad_photo"] = message.photo[0].file_id
        await FSMAdmin.curse_group_rad.set()
        await message.answer("До якої групи привязати", reply_markup=await get_kb())

    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)
        await state.finish()


# @dp.message_handler(state=FSMAdmin.curse_group_rad)
async def add_schedule_to_group2(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if (
        await db.admin_exists_sql(message.from_user.id)
        or message.from_user.id == super_admin_admin
        or message.from_user.id == super_admin_ura
    ):
        async with state.proxy() as data:
            data["curse_group_rad"] = message.text
        now = datetime.datetime.now()
        now = now.strftime("%d - %B, %A")
        translation = translator.translate(now)
        await db.group_photo_update_sql(
            data["curse_group_rad_photo"],
            data["curse_group_rad"],
            "Зміненно: " + translation,
        )
        await message.answer("Розклад успішно добавлено", reply_markup=kb_admin)
        await state.finish()
    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)
        await state.finish()


# ===========================Додати розклад викладачу============================
async def add_schedule_to_teacher(message: types.Message):
    db = await Database.setup()
    if (
        await db.admin_exists_sql(message.from_user.id)
        or message.from_user.id == super_admin_admin
        or message.from_user.id == super_admin_ura
    ):
        await FSMAdmin.teachers_rad_photo.set()
        await message.answer("Киньте фото розкладу", reply_markup=ReplyKeyboardRemove())

    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)


async def add_schedule_to_teacher1(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if (
        await db.admin_exists_sql(message.from_user.id)
        or message.from_user.id == super_admin_admin
        or message.from_user.id == super_admin_ura
    ):
        async with state.proxy() as data:
            data["teachers_rad_photo"] = message.photo[0].file_id
        await FSMAdmin.teachers_rad.set()
        await message.answer("До якої групи привязати", reply_markup=await get_t_kb())

    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)
        await state.finish()


async def add_schedule_to_teacher2(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if (
        await db.admin_exists_sql(message.from_user.id)
        or message.from_user.id == super_admin_admin
        or message.from_user.id == super_admin_ura
    ):
        async with state.proxy() as data:
            data["teachers_rad"] = message.text
        now = datetime.datetime.now()
        now = now.strftime("%d - %B, %A")
        translation = translator.translate(now)
        await db.teacher_photo_update_sql(
            data["teachers_rad_photo"], data["teachers_rad"], "Зміненно: " + translation
        )
        await message.answer("Розклад успішно добавлено", reply_markup=kb_admin)
        await state.finish()
    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)
        await state.finish()


# ===========================Видалити акаунт============================
# @dp.message_handler(text ='Видалити акаунт')
async def delete_admin(message: types.Message):
    db = await Database.setup()
    if (
        await db.admin_exists_sql(message.from_user.id)
        or message.from_user.id == super_admin_admin
        or message.from_user.id == super_admin_ura
    ):
        await db.delete_admins_sql(message.from_user.id)
        if await db.admin_exists_sql(message.from_user.id):
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start_admin)
        elif await db.user_exists_sql(message.from_user.id):
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start_user)
        elif await db.teachers_exists_sql(message.from_user.id):
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start_user)
        else:
            await message.answer("⬇️Головне меню⬇️", reply_markup=kb_start)
    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)


# ===========================Видалити групу============================
# @dp.message_handler(text ="Видалити групу", state=None)
async def delete_group(message: types.Message):
    db = await Database.setup()
    if (
        await db.admin_exists_sql(message.from_user.id)
        or message.from_user.id == super_admin_admin
        or message.from_user.id == super_admin_ura
    ):
        await FSMAdmin.curse_group_delete.set()
        await message.answer(
            "Виберіть групу з наведених нижче", reply_markup=await get_kb()
        )

    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)


# @dp.message_handler(state=FSMAdmin.curse_group_delete)
async def load_group(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if (
        await db.admin_exists_sql(message.from_user.id)
        or message.from_user.id == super_admin_admin
        or message.from_user.id == super_admin_ura
    ):
        if message.text == "Назад":
            await message.answer("Меню", reply_markup=kb_admin)
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
                            reply_markup=kb_admin,
                        )

                    elif not await db.user_group_exists_sql(fullname):
                        await db.delete_groups_sql(fullname)
                        await message.answer("Групу видалено", reply_markup=kb_admin)
                    await state.finish()
                else:
                    await message.answer(
                        "Назва групи не може перевищувати три символи",
                        reply_markup=kb_admin,
                    )
                    await state.finish()
            else:
                await message.answer(
                    "Група з такою назвою немає", reply_markup=kb_admin
                )
                await state.finish()
    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)
        await state.finish()


# ===========================Новина============================
# @dp.message_handler(text ="Викласти новину", state=None)
async def send_news(message: types.Message):
    db = await Database.setup()
    if (
        await db.admin_exists_sql(message.from_user.id)
        or message.from_user.id == super_admin_admin
        or message.from_user.id == super_admin_ura
    ):
        await message.answer(
            "Куди надіслати (одна група\всі групи)", reply_markup=kb_all_or_one
        )

        await FSMAdmin.all_or_one.set()
    elif message.text == "Назад":
        await message.answer("Ваша клавіатура : ", reply_markup=kb_admin)

    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)


# @dp.message_handler(state=FSMAdmin.all_or_one)
async def send_news1(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if message.text == "Назад":
        await message.answer("Ваша клавіатура : ", reply_markup=kb_admin)
        await state.finish()
    elif (
        await db.admin_exists_sql(message.from_user.id)
        or message.from_user.id == super_admin_admin
        or message.from_user.id == super_admin_ura
    ):
        if message.text == "Одна" or message.text == "Всі":
            async with state.proxy() as data:
                data["all_or_one"] = message.text
            await message.answer(
                "Введіть текст новини :", reply_markup=ReplyKeyboardRemove()
            )
            await FSMAdmin.text_news.set()
        else:
            await message.answer("Неправильне значення", reply_markup=kb_admin)
            await state.finish()
    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)
        await state.finish()


# @dp.message_handler(state=FSMAdmin.text_news)
async def send_news2(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if message.text == "Назад":
        await message.answer("Ваша клавіатура : ", reply_markup=kb_admin)

        await state.finish()
    elif (
        await db.admin_exists_sql(message.from_user.id)
        or message.from_user.id == super_admin_admin
        or message.from_user.id == super_admin_ura
    ):
        async with state.proxy() as data:
            data["text_news"] = message.text
        await FSMAdmin.photo_news.set()
        await message.answer(
            "Скиньте фото новини або натисніть \nкнопку [<b>не треба</b>]\nякщо новина без фото",
            reply_markup=kb_dont,
            parse_mode="HTML",
        )

    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)
        await state.finish()


# @dp.message_handler(state=FSMAdmin.photo_news)
async def send_news3(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if message.text == "Назад":
        await message.answer("Ваша клавіатура : ", reply_markup=kb_admin)
        await state.finish()
    elif (
        await db.admin_exists_sql(message.from_user.id)
        or message.from_user.id == super_admin_admin
        or message.from_user.id == super_admin_ura
    ):
        if message.text == "не треба":
            async with state.proxy() as data:
                data["photo_news"] = "a"
                if data["all_or_one"] == "Одна":
                    await FSMAdmin.namegroups.set()
                    await message.answer(
                        "Виберіть назву групи :", reply_markup=await get_kb()
                    )

                elif data["all_or_one"] == "Всі":
                    await FSMAdmin.namegroups.set()
                    await message.answer("Надсилати новину ?", reply_markup=kb_ys)
        else:
            await message.answer("Неправильне значення", reply_markup=kb_admin)
            await state.finish()

    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)
        await state.finish()


# @dp.message_handler(content_types=['photo'],state=FSMAdmin.photo_news)
async def send_news4(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if message.text == "Назад":
        await message.answer("Ваша клавіатура : ", reply_markup=kb_admin)

        await state.finish()
    elif (
        await db.admin_exists_sql(message.from_user.id)
        or message.from_user.id == super_admin_admin
        or message.from_user.id == super_admin_ura
    ):
        async with state.proxy() as data:
            if data["all_or_one"] == "Одна":
                async with state.proxy() as data:
                    data["photo_news"] = message.photo[0].file_id
                await FSMAdmin.namegroups.set()
                await message.answer(
                    "Виберіть назву групи :", reply_markup=await get_kb()
                )

            elif data["all_or_one"] == "Всі":
                async with state.proxy() as data:
                    data["photo_news"] = message.photo[0].file_id
                await FSMAdmin.namegroups.set()
                await message.answer("Підтвердити надсилання", reply_markup=kb_ys)

    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)
        await state.finish()


# @dp.message_handler(state=FSMAdmin.namegroups)
async def send_news5(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if message.text == "Назад":
        await message.answer("Ваша клавіатура : ", reply_markup=kb_admin)
        await state.finish()
    elif (
        await db.admin_exists_sql(message.from_user.id)
        or message.from_user.id == super_admin_admin
        or message.from_user.id == super_admin_ura
    ):
        async with state.proxy() as data:
            data["namegroups"] = message.text
        if data["all_or_one"] == "Одна":
            try:
                h = await db.id_from_group_exists_sql(data["namegroups"])
                error = h[0][0]
                new = []
                for i in range(0, len(h)):
                    new.append(h[i][0])
                if len(data["photo_news"]) > 3:
                    texts = data["text_news"]
                    photo = data["photo_news"]
                    for all_id in range(0, len(new)):
                        try:
                            await bot.send_photo(new[all_id], photo, texts)
                        except BotBlocked:
                            await asyncio.sleep(0.5)
                    await message.answer("Готово!", reply_markup=kb_admin)
                    await state.finish()
                elif len(data["photo_news"]) == 1:
                    for all_ids in range(0, len(new)):
                        try:
                            await bot.send_message(new[all_ids], data["text_news"])
                        except BotBlocked:
                            await asyncio.sleep(0.5)
                    await message.answer("Готово!", reply_markup=kb_admin)
                    await state.finish()
            except IndexError:
                await message.answer(
                    "немає жодної людини підключенної до цієї групи",
                    reply_markup=kb_admin,
                )
                await state.finish()

        if data["all_or_one"] == "Всі":
            all_users = await db.all_user_id_sql()
            rest = []
            for i in range(0, len(all_users)):
                rest.append(all_users[i][0])
            async with state.proxy() as data:
                if len(data["photo_news"]) > 3:
                    texts = data["text_news"]
                    photo = data["photo_news"]
                    for all_id in range(0, len(rest)):
                        try:
                            await bot.send_photo(rest[all_id], photo, texts)
                        except BotBlocked:
                            await db.delete_users_sql(rest[all_id])
                            await bot.send_message(
                                5963046063, f"Видалено користувача {rest[all_id]}"
                            )
                            await asyncio.sleep(0.5)
                    await message.answer("Готово!", reply_markup=kb_admin)
                    await state.finish()
                elif len(data["photo_news"]) == 1:
                    for all_ids in range(0, len(rest)):
                        try:
                            await bot.send_message(
                                rest[all_ids],
                                data["text_news"],
                                reply_markup=kb_start_user,
                            )
                        except BotBlocked:
                            await db.delete_users_sql(rest[all_ids])
                            await bot.send_message(
                                5963046063, f"Видалено користувача {rest[all_ids]}"
                            )
                            await asyncio.sleep(0.5)
                    await message.answer("Готово!", reply_markup=kb_admin)
                    await state.finish()
    elif message.text == "Назад":
        await message.answer("Ваша клавіатура : ", reply_markup=kb_admin)
        await state.finish()
    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)
        await state.finish()


# ===========================Додати розклад дзвінків============================
# @dp.message_handler(text ="Додати розклад дзвінків", state=None)
async def add_calls(message: types.Message):
    db = await Database.setup()
    if (
        await db.admin_exists_sql(message.from_user.id)
        or message.from_user.id == super_admin_admin
        or message.from_user.id == super_admin_ura
    ):
        await message.answer("Завантажте фото", reply_markup=ReplyKeyboardRemove())
        await FSMAdmin.id_photo.set()
    elif message.text == "Назад":
        await message.answer("Ваша клавіатура : ", reply_markup=kb_admin)
    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)


# @dp.message_handler(content_types=['photo'],state=FSMAdmin.id_photo)
async def add_calls1(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if (
        await db.admin_exists_sql(message.from_user.id)
        or message.from_user.id == super_admin_admin
        or message.from_user.id == super_admin_ura
    ):
        async with state.proxy() as data:
            data["id_photo"] = message.photo[0].file_id
            data["type"] = "calls"
        now = datetime.datetime.now()
        now = now.strftime("%d - %B, %A")
        translation = translator.translate(now)
        await db.add_calls_sql(
            data["type"], data["id_photo"], "Зміненно: " + translation
        )
        await state.finish()
        await message.answer("Розклад дзвінків успішно оновлено", reply_markup=kb_admin)

    elif message.text == "Назад":
        await message.answer("Ваша клавіатура : ", reply_markup=kb_admin)

    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)


# ===========================Видалити розклад дзвінків============================
# @dp.message_handler(text ="Видалити розклад дзвінків")
async def delete_calls(message: types.Message):
    db = await Database.setup()
    if (
        await db.admin_exists_sql(message.from_user.id)
        or message.from_user.id == super_admin_admin
        or message.from_user.id == super_admin_ura
    ):
        check = await db.delete_calls_sql()
        if not check:
            await message.answer(
                "Розкладу дзвінків ще не додано", reply_markup=kb_admin
            )
        elif check:
            await message.answer(
                "Розклад дзвінків успішно видалено", reply_markup=kb_admin
            )
    elif message.text == "Назад":
        await message.answer("Ваша клавіатура : ", reply_markup=kb_admin)
    else:
        await message.answer("Ви не адмін :D", reply_markup=kb_start)


# ===========================реєстратор============================
def register_handler_admin(dp: Dispatcher):
    # ===========================Додати викладача=============================
    dp.register_message_handler(add_teachers, text="викладача ❇️", state=None)
    dp.register_message_handler(add_teachers1, state=FSMAdmin.teachers_name)
    # ===========================Видалити викладача==============================
    dp.register_message_handler(delete_teachers, text="викладача 🗑", state=None)
    dp.register_message_handler(delete_teachers1, state=FSMAdmin.teachers_delete)
    # ===========================Додавання групи=============================
    dp.register_message_handler(add_group, text="групу ❇️", state=None)
    dp.register_message_handler(add_group1, state=FSMAdmin.curse_group)
    # ===========================Видалити групу==============================
    dp.register_message_handler(delete_group, text="групу 🗑", state=None)
    dp.register_message_handler(load_group, state=FSMAdmin.curse_group_delete)
    # ===========================Додати розклад до курсу=====================
    dp.register_message_handler(add_schedule_to_group, text="групі ❇️", state=None)
    dp.register_message_handler(
        add_schedule_to_group1,
        content_types=["photo"],
        state=FSMAdmin.curse_group_rad_photo,
    )
    dp.register_message_handler(add_schedule_to_group2, state=FSMAdmin.curse_group_rad)
    # ===========================Додати розклад викладачу=====================
    dp.register_message_handler(
        add_schedule_to_teacher, text="викладачу ❇️", state=None
    )
    dp.register_message_handler(
        add_schedule_to_teacher1,
        content_types=["photo"],
        state=FSMAdmin.teachers_rad_photo,
    )
    dp.register_message_handler(add_schedule_to_teacher2, state=FSMAdmin.teachers_rad)
    # ===========================Видалити акаунт=============================
    dp.register_message_handler(delete_admin, text="Видалити акаунт")
    # ===========================Новина======================================
    dp.register_message_handler(send_news, text="Викласти новину", state=None)
    dp.register_message_handler(send_news1, state=FSMAdmin.all_or_one)
    dp.register_message_handler(send_news2, state=FSMAdmin.text_news)
    dp.register_message_handler(send_news3, state=FSMAdmin.photo_news)
    dp.register_message_handler(
        send_news4, content_types=["photo"], state=FSMAdmin.photo_news
    )
    dp.register_message_handler(send_news5, state=FSMAdmin.namegroups)
    # ===========================Додати розклад дзвінків======================
    dp.register_message_handler(add_calls, text="дзвінків ❇️", state=None)
    dp.register_message_handler(
        add_calls1, content_types=["photo"], state=FSMAdmin.id_photo
    )
    # ===========================Видалити розклад дзвінків============================
    dp.register_message_handler(delete_calls, text="дзвінків 🗑")
