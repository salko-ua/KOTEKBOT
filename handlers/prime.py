from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from data_base import Database
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import BotBlocked
from keyboards import *
from handlers.stats import stats_schedule_add
from create_bot import bot


# =========Класс машини стану=========
class FSMWrite(StatesGroup):
    group = State()
    message = State()


async def text_save(message: types.Message):
    db = await Database.setup()
    await stats_schedule_add("Додати замітку 📝", 1)
    if await db.user_exists_sql(message.from_user.id):
        if len(message.text[7::]) < 2:
            await message.answer("текст закороткий")
        else:
            link = message.text[7::]
            groups = await db.group_for_user_id(message.from_user.id)
            await db.add_text_sql(link, groups)
            await message.answer("Успішно додано!")
    elif await db.teachers_exists_sql(message.from_user.id):
        if len(message.text[7::]) < 2:
            await message.answer("текст закороткий")
        else:
            link = message.text[7::]
            groups = await db.see_group_for_teach_id(message.from_user.id)
            await db.add_text_sql(link, groups)
            await message.answer("Успішно додано!")
    else:
        await message.answer("Ви не зареєстровані у групах")


async def see_text(message: types.Message):
    db = await Database.setup()
    await stats_schedule_add("Замітки 📝", 1)
    if await db.user_exists_sql(message.from_user.id):
        groups = await db.group_for_user_id(message.from_user.id)
        boolean, text = await db.see_text_sql(groups)
        if boolean:
            await message.answer(
                "Замітки для вашої групи :\n\n"
                + text
                + "\n\nЩоб встановити нові\nнапишіть 'додати *ваш текст*'"
            )
        elif not boolean:
            await message.answer(
                "У вашої групи не додано ніякого тесту\nЩоб це зробити напишіть \n'додати *ваш текст*'"
            )
    elif await db.teachers_exists_sql(message.from_user.id):
        groups = await db.see_group_for_teach_id(message.from_user.id)
        boolean, text = await db.see_text_sql(groups)
        if boolean:
            await message.answer(
                "Ваші замітки :\n\n"
                + text
                + "\n\nЩоб встановити нові\nнапишіть 'додати *ваш текст*'"
            )
        elif not boolean:
            await message.answer(
                "У вас не додано ніякого тесту\nЩоб це зробити напишіть \n'додати *ваш текст*'"
            )
    else:
        await message.answer("Ви не зареєстровані")


async def write(message: types.Message):
    db = await Database.setup()
    await stats_schedule_add("Написати ✉️", 1)
    if await db.user_exists_sql(message.from_user.id):
        await message.answer(
            "Щоб написати повідомлення іншій групі\nспочатку виберіть її ім'я нижче ⬇️",
            reply_markup=await get_kb(),
        )
        await FSMWrite.group.set()


async def write1(message: types.Message, state: FSMContext):
    db = await Database.setup()
    group = await db.group_exists_sql(message.text)
    if message.text == "Назад":
        await state.finish()
        await message.answer(
            "Надсилання повідомлення відміненно ✅", reply_markup=kb_client
        )
    else:
        if group:
            async with state.proxy() as data:
                data["group"] = message.text
            await FSMWrite.message.set()
            await message.answer(
                f"Напишіть повідомлення 📝", reply_markup=types.ReplyKeyboardRemove()
            )
        elif not group:
            await message.answer(
                f"Немає групи {message.text} ❌", reply_markup=kb_client
            )
            await state.finish()


async def write2(message: types.Message, state: FSMContext):
    db = await Database.setup()

    async with state.proxy() as data:
        group = data["group"]
        all_user = await db.all_user_id_for_group_sql(group)
        group_user_writer = await db.group_for_user_id(message.from_user.id)
        if bool(len(all_user)):
            for number in range(0, len(all_user)):
                try:
                    await bot.send_message(
                        all_user[number][0],
                        f"Повідомлення від {group_user_writer}\n" + message.text,
                    )
                except BotBlocked:
                    await db.delete_users_sql(all_user[number])
                    await bot.send_message(
                        5963046063, f"Видалено користувача {all_user[number]}"
                    )
            await message.answer("Повідомлення надісланно ✅", reply_markup=kb_client)
        elif bool(len(all_user)) == False:
            await message.answer(
                f"Немає студентів у групі {group} ❌", reply_markup=kb_client
            )
    await state.finish()


def register_handler_stats(dp: Dispatcher):
    dp.register_message_handler(text_save, Text(ignore_case=True, startswith="Додати"))
    dp.register_message_handler(see_text, commands=["text"])
    dp.register_message_handler(see_text, Text(ignore_case=True, equals="Замітки 📝"))
    dp.register_message_handler(write, Text(ignore_case=True, equals="Написати ✉️"))
    dp.register_message_handler(write1, state=FSMWrite.group)
    dp.register_message_handler(write2, state=FSMWrite.message)
