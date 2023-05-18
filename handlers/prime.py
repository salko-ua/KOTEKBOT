from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from data_base import Database
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import BotBlocked
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards import *
from handlers.stats import stats_schedule_add
from create_bot import bot


# =========Класс машини стану=========
class FSMWrite(StatesGroup):
    text = State()
    group = State()
    teach = State()
    message_group = State()
    message_teach = State()

text_inline = InlineKeyboardButton("Змінити замітку", callback_data = "edit_text")
text_inline_kb = InlineKeyboardMarkup(row_width=1).add(text_inline)

cancle_inline = InlineKeyboardButton("Відмінити ❌", callback_data = "cancel")
cancle_inline_kb = InlineKeyboardMarkup(row_width=1).add(cancle_inline)



async def text_save(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_text("""
Тепер введіть текст який буде міститися
у замітках вашої групи

Наприклад :
Електронний щоденник: посилання на сайт

Чергування : посилання на сайт

Ви ж можете написати будь-що це лише приклад.""", reply_markup=cancle_inline_kb)
    await FSMWrite.text.set()
    

async def cancel(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_text("Редагування тексту успішно відмінено✅", reply_markup=text_inline_kb)
    await state.finish()


async def text_save1(message: types.Message, state: FSMContext):
    db = await Database.setup()
    await stats_schedule_add("Додати замітку 📝", 1)

    if await db.user_exists_sql(message.from_user.id):
        if len(message.text) <= 1:
            await message.answer("Текст надто короткий спробуй ще раз", reply_markup=text_inline_kb)
            await state.finish()
        else:
            text = message.text
            groups = await db.group_for_user_id(message.from_user.id)
            await db.add_text_sql(text, groups)
            await message.answer("Замітку успішно додано ✅", reply_markup=text_inline_kb)
            await state.finish()
    elif await db.teachers_exists_sql(message.from_user.id):
        if len(message.text) <= 1:
            await message.answer("Текст надто короткий спробуй ще раз", reply_markup=text_inline_kb)
            await state.finish()
        else:
            text = message.text
            groups = await db.see_group_for_teach_id(message.from_user.id)
            await db.add_text_sql(text, groups)
            await message.answer("Замітку успішно додано ✅", reply_markup=text_inline_kb)
            await state.finish()
    else:
        await message.answer("Ви не зареєстровані у групах")
        await state.finish()


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
                + "\n\nЩоб встановити нові\nнатисніть кнопку нижче", reply_markup=text_inline_kb
            )
        elif not boolean:
            await message.answer(
                "У вашої групи не додано ніякого тексту\nЩоб це зробити\nнатисніть кнопку нижче", 
                reply_markup=text_inline_kb
            )
    elif await db.teachers_exists_sql(message.from_user.id):
        groups = await db.see_group_for_teach_id(message.from_user.id)
        boolean, text = await db.see_text_sql(groups)
        if boolean:
            await message.answer(
                "Ваші замітки :\n\n"
                + text
                + "\n\nЩоб встановити нові\nнатисніть кнопку нижче",
                reply_markup=text_inline_kb
            )
        elif not boolean:
            await message.answer(
                "У вас не додано ніякого тексту\nЩоб це зробити\nнатисніть кнопку нижче", 
                reply_markup=text_inline_kb
            )
    else:
        await message.answer("Ви не зареєстровані")


async def write(message: types.Message):
    db = await Database.setup()
    await stats_schedule_add("Написати ✉️", 1)
    await message.delete()
    if await db.user_exists_sql(message.from_user.id):
        msg = await message.answer("Видалення клавіатури", reply_markup=types.ReplyKeyboardRemove())
        await msg.delete()
        await message.answer(
            "Щоб написати повідомлення іншій групі\nспочатку виберіть її ім'я нижче ⬇️",
            reply_markup = await inline_kb_group(),
        )
        await FSMWrite.group.set()
    elif await db.teachers_exists_sql(message.from_user.id):
        await message.answer(
            "Щоб написати повідомлення іншій групі\nспочатку виберіть її ім'я нижче ⬇️",
            reply_markup = await get_t_kb(),
        )
        await FSMWrite.teach.set()


async def write_group(query: types.CallbackQuery, state: FSMContext):
    db = await Database.setup()
    if query.data == "Назад":
        await state.finish()
        await query.message.delete_reply_markup()
        msg = await query.message.edit_text("Надсилання повідомлення відміненно ✅")
        await msg.delete()
        await query.message.answer("Надсилання повідомлення відміненно ✅", reply_markup=kb_client)

    else:
        group = await db.group_exists_sql(query.data)
        if group:
            await FSMWrite.message_group.set()
            await query.message.delete_reply_markup()
            msg = await query.message.edit_text(f"Напишіть повідомлення 📝")
            async with state.proxy() as data:
                data["group"] = query.data
                data["msg_id"] = msg.message_id
                data["chat_id"] = msg.chat.id


async def write_teach(message: types.Message, state: FSMContext):
    db = await Database.setup()
    teach = await db.teacher_name_exists_sql(message.text)
    if message.text == "Назад":
        await state.finish()
        await message.answer(
            "Надсилання повідомлення відміненно ✅", reply_markup=kb_client
        )
    else:
        if teach:
            async with state.proxy() as data:
                data["group"] = message.text
            await FSMWrite.message_teach.set()
            await message.answer(
                f"Напишіть повідомлення 📝", reply_markup=types.ReplyKeyboardRemove()
            )
        elif not teach:
            await message.answer(
                f"Немає викладача {message.text} ❌", reply_markup=kb_client
            )
            await state.finish()



async def write_group_message(message: types.Message, state: FSMContext):
    db = await Database.setup()

    async with state.proxy() as data:
        group = data["group"]
        msg_id = data["msg_id"]
        chat_id = data["chat_id"]
        all_user_their = await db.all_user_id_for_group_sql(group)
        group_user_writer = await db.group_for_user_id(message.from_user.id)
        all_user_us = await db.all_user_id_for_group_sql(group_user_writer)
        await bot.delete_message(chat_id, msg_id)
        await message.delete()
        if group == group_user_writer:
            for number in range(0, len(all_user_us)):
                    try:
                        await bot.send_message(
                            all_user_us[number][0],
                            f"Від нашої групи :\n" + message.text,
                        )
                    except:
                        pass
            await message.answer("Надісланно ✅", reply_markup=kb_client)
        else:
            if bool(len(all_user_their)):
                await bot.send_message(5963046063, f"{message.from_user.id} {group_user_writer} надіслав до {group}:\n{message.text}\n ")
                for number in range(0, len(all_user_us)):
                    try:
                        await bot.send_message(
                            all_user_us[number][0],
                            f"Ми до {group} :\n" + message.text,
                        )
                    except:
                        pass
                for number in range(0, len(all_user_their)):
                    try:
                        await bot.send_message(
                            all_user_their[number][0],
                            f"{group_user_writer} пише :\n" + message.text,
                        )
                    except:
                        pass
                await message.answer("Надісланно ✅", reply_markup=kb_client)
            elif bool(len(all_user_their)) == False:
                await message.answer(
                    f"Немає студентів у групі {group} ❌", reply_markup=kb_client
                )
    await state.finish()

async def write_teach_message(message: types.Message, state: FSMContext):
    db = await Database.setup()

    async with state.proxy() as data:
        group = data["group"]
        all_user = await db.all_teach_id_for_group_sql(group)
        group_user_writer = await db.group_for_teach_id(message.from_user.id)
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
                f"Немає зареєстрованого викладача за цим ім'ям {group} ❌", reply_markup=kb_client
            )
    await state.finish()


async def get_list():
    db = await Database.setup()
    list = await db.group_list_sql()
    return list

async def register_handler_stats(dp: Dispatcher):
    button_list = await get_list()
    dp.register_callback_query_handler(text_save, text = "edit_text", state=None)
    dp.register_callback_query_handler(cancel, text = "cancel", state=FSMWrite.text)
    dp.register_message_handler(text_save1, state=FSMWrite.text)
    dp.register_message_handler(see_text, commands=["text"])
    dp.register_message_handler(see_text, Text(ignore_case=True, equals="Замітки 📝"))
    dp.register_message_handler(write, Text(ignore_case=True, equals="Написати ✉️"), state=None)
    for text in button_list:
        dp.register_callback_query_handler(write_group, lambda c, t=text: c.data == t, state=FSMWrite.group)
    dp.register_callback_query_handler(write_group, text = "Назад", state=FSMWrite.group)
    dp.register_message_handler(write_teach, state=FSMWrite.teach)
    dp.register_message_handler(write_group_message, state=FSMWrite.message_group)
    dp.register_message_handler(write_teach_message, state=FSMWrite.message_teach)
