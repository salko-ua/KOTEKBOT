import os
import random
import asyncio

from keyboards import *
from create_bot import bot
from aiogram import types
from data_base import Database

from handlers.stats import stats_schedule_add
from aiogram.dispatcher import Dispatcher, FSMContext

from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import RetryAfter

from aiogram.dispatcher.filters.state import State, StatesGroup





# =========Класс машини стану=========
class FSMWrite(StatesGroup):
    text = State()
    group = State()
    teach = State()
    message_group = State()
    message_teach = State()


async def get_list():
    db = await Database.setup()
    list = await db.group_list_sql()
    return list


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


#============= функція написати 1 етап | вибір групи
async def write(message: types.Message):
    db = await Database.setup()
    await stats_schedule_add("Написати ✉️", 1)
    if not await db.user_exists_sql(message.from_user.id):
        return
    
    await message.delete()
    msg = await message.answer("Видалення клавіатури", reply_markup=types.ReplyKeyboardRemove())
    await msg.delete()
    await message.answer(
        "Щоб написати повідомлення іншій групі\nспочатку виберіть її ім'я нижче ⬇️",
        reply_markup = await inline_kb_group())
    await FSMWrite.group.set()


#============= функція написати 2 етап | написання повідомлення
async def write_group(query: types.CallbackQuery, state: FSMContext):
    db = await Database.setup()
    group = await db.group_exists_sql(query.data)

    if not group:
        return
    
    await FSMWrite.message_group.set()
    await query.message.delete_reply_markup()
    msg = await query.message.edit_text(f"Надішліть :\n • Текст 📝\n • Фото 🖼\n • Відео 📼\n • Стікер 💌\n • GIF 🪨", reply_markup=inline_back)
    async with state.proxy() as data:
        data["group"] = query.data
        data["msg_id"] = msg.message_id
        data["chat_id"] = msg.chat.id


#============= функція написати 3 етап | Надсилання повідомлення

#============= отримання данних
async def get_data(message: types.Message, state: FSMContext):
    db = await Database.setup()
    async with state.proxy() as data:
        msg_id = data["msg_id"]
        chat_id = data["chat_id"]
        group = data["group"]
        group_user_writer = await db.group_for_user_id(message.from_user.id)
        all_user_their = await db.all_user_id_for_group_sql(group)
        all_user_us = await db.all_user_id_for_group_sql(group_user_writer)
        await bot.delete_message(chat_id, msg_id)
        await message.delete()
    """
    повертаю 
    групу якій пішуть
    групу яка написала
    список користувачів у групі якій пишуть
    список користувачів у групі яка пише
    """
    return group, group_user_writer, all_user_us, all_user_their



#============= надслання текстового повідомлення
async def write_group_message_text(message: types.Message, state: FSMContext):
    group, group_user_writer, all_user_us, all_user_their = await get_data(message, state)
    text = message.text
    data = None

    if group == group_user_writer:
        all_user_us_ids = map(lambda e: e[0], all_user_us)
        groups = None
        await asyncio.gather(*map(send_notification(1, text, data, groups), all_user_us_ids))
        await message.answer("Надісланно ✅", reply_markup=kb_client)

    else:
        if bool(len(all_user_their)):
            all_user_us_id = map(lambda e: e[0], all_user_us)
            all_user_their_id = map(lambda e: e[0], all_user_their)
            groups = [group, group_user_writer]

            await asyncio.gather(*map(send_notification(2, text, data, groups), all_user_us_id))
            await asyncio.gather(*map(send_notification(3, text, data, groups), all_user_their_id))

            await message.answer("Надісланно ✅", reply_markup=kb_client)

        elif bool(len(all_user_their)) == False:
            await message.answer(f"Немає студентів у групі {group} ❌", reply_markup=kb_client)
    await state.finish()

#============= надслання фото повідомлення
async def write_group_message_photo(message: types.Message, state: FSMContext):
    group, group_user_writer, all_user_us, all_user_their = await get_data(message, state)
    text = None
    photo = message.photo[0].file_id

    if group == group_user_writer:
        all_user_us_ids = map(lambda e: e[0], all_user_us)
        groups = None
        await asyncio.gather(*map(send_notification(4, text, photo, groups), all_user_us_ids))
        await message.answer("Надісланно ✅", reply_markup=kb_client)

    else:
        if bool(len(all_user_their)):
            all_user_us_id = map(lambda e: e[0], all_user_us)
            all_user_their_id = map(lambda e: e[0], all_user_their)
            groups = [group, group_user_writer]

            await asyncio.gather(*map(send_notification(5, text, photo, groups), all_user_us_id))
            await asyncio.gather(*map(send_notification(6, text, photo, groups), all_user_their_id))

            await message.answer("Надісланно ✅", reply_markup=kb_client)

        elif bool(len(all_user_their)) == False:
            await message.answer(f"Немає студентів у групі {group} ❌", reply_markup=kb_client)
    await state.finish()

#============= надслання стікер повідомлення
async def write_group_message_sticker(message: types.Message, state: FSMContext):
    group, group_user_writer, all_user_us, all_user_their = await get_data(message, state)
    text = None
    sticker = message.sticker.file_id

    if group == group_user_writer:
        all_user_us_ids = map(lambda e: e[0], all_user_us)
        groups = None
        await asyncio.gather(*map(send_notification(7, text, sticker, groups), all_user_us_ids))
        await message.answer("Надісланно ✅", reply_markup=kb_client)

    else:
        if bool(len(all_user_their)):
            all_user_us_id = map(lambda e: e[0], all_user_us)
            all_user_their_id = map(lambda e: e[0], all_user_their)
            groups = [group, group_user_writer]

            await asyncio.gather(*map(send_notification(8, text, sticker, groups), all_user_us_id))
            await asyncio.gather(*map(send_notification(9, text, sticker, groups), all_user_their_id))

            await message.answer("Надісланно ✅", reply_markup=kb_client)

        elif bool(len(all_user_their)) == False:
            await message.answer(f"Немає студентів у групі {group} ❌", reply_markup=kb_client)
    await state.finish()

#============= надслання відео повідомлення
async def write_group_message_video(message: types.Message, state: FSMContext):
    group, group_user_writer, all_user_us, all_user_their = await get_data(message, state)
    text = None
    video = message.video.file_id

    if group == group_user_writer:
        all_user_us_ids = map(lambda e: e[0], all_user_us)
        groups = None
        await asyncio.gather(*map(send_notification(10, text, video, groups), all_user_us_ids))
        await message.answer("Надісланно ✅", reply_markup=kb_client)

    else:
        if bool(len(all_user_their)):
            all_user_us_id = map(lambda e: e[0], all_user_us)
            all_user_their_id = map(lambda e: e[0], all_user_their)
            groups = [group, group_user_writer]

            await asyncio.gather(*map(send_notification(11, text, video, groups), all_user_us_id))
            await asyncio.gather(*map(send_notification(12, text, video, groups), all_user_their_id))

            await message.answer("Надісланно ✅", reply_markup=kb_client)

        elif bool(len(all_user_their)) == False:
            await message.answer(f"Немає студентів у групі {group} ❌", reply_markup=kb_client)
    await state.finish()

#============= надслання gif повідомлення
async def write_group_message_animation(message: types.Message, state: FSMContext):
    group, group_user_writer, all_user_us, all_user_their = await get_data(message, state)
    text = None
    animation = message.animation.file_id

    if group == group_user_writer:
        all_user_us_ids = map(lambda e: e[0], all_user_us)
        groups = None
        await asyncio.gather(*map(send_notification(13, text, animation, groups), all_user_us_ids))
        await message.answer("Надісланно ✅", reply_markup=kb_client)

    else:
        if bool(len(all_user_their)):
            all_user_us_id = map(lambda e: e[0], all_user_us)
            all_user_their_id = map(lambda e: e[0], all_user_their)
            groups = [group, group_user_writer]

            await asyncio.gather(*map(send_notification(14, text, animation, groups), all_user_us_id))
            await asyncio.gather(*map(send_notification(15, text, animation, groups), all_user_their_id))

            await message.answer("Надісланно ✅", reply_markup=kb_client)

        elif bool(len(all_user_their)) == False:
            await message.answer(f"Немає студентів у групі {group} ❌", reply_markup=kb_client)
    await state.finish()

def send_notification(what_send: int, text: str, file_id: str, groups: list):
    async def wrapped(user_id: int):
        try:
            try:
                # TEXT
                if what_send == 1:
                    await bot.send_message(user_id, f"Від нашої групи :\n" + text)
                elif what_send == 2:
                    await bot.send_message(user_id, f"Ми до {groups[0]} :\n" + text)
                elif what_send == 3:
                    await bot.send_message(user_id, f"{groups[1]} пише :\n" + text)

                # PHOTO
                elif what_send == 4:
                    await bot.send_photo(user_id, file_id, f"Від нашої групи.")
                elif what_send == 5:
                    await bot.send_photo(user_id, file_id, f"Ми до {groups[0]} :")
                elif what_send == 6:
                    await bot.send_photo(user_id, file_id, f"{groups[1]} надсилає :")

                # SRICKER
                elif what_send == 7:
                    await bot.send_message(user_id, file_id, f"Від нашої групи.")
                    await bot.send_sticker(user_id, file_id)
                elif what_send == 8:
                    await bot.send_message(user_id, f"Ми до {groups[0]} :")
                    await bot.send_sticker(user_id, file_id)
                elif what_send == 9:
                    await bot.send_message(user_id, f"{groups[1]} надсилає :")
                    await bot.send_sticker(user_id, file_id)

                # VIDEO
                elif what_send == 10:
                    await bot.send_message(user_id, file_id, f"Від нашої групи.")
                    await bot.send_video(user_id, file_id)
                elif what_send == 11:
                    await bot.send_message(user_id, f"Ми до {groups[0]} :")
                    await bot.send_video(user_id, file_id)
                elif what_send == 12:
                    await bot.send_message(user_id, f"{groups[1]} надсилає :")
                    await bot.send_video(user_id, file_id)

                # ANIMATION
                elif what_send == 13:
                    await bot.send_message(user_id, f"Від нашої групи.")
                    await bot.send_animation(user_id, file_id)
                elif what_send == 14:
                    await bot.send_message(user_id, f"Ми до {groups[0]} :")
                    await bot.send_animation(user_id, file_id)
                elif what_send == 15:
                    await bot.send_message(user_id, f"{groups[1]} надсилає :")
                    await bot.send_animation(user_id, file_id)
            except RetryAfter as ra:
                await asyncio.sleep(ra.timeout)
        except:
            pass
    
    return wrapped


#================= ВІДМІНА ДІЇ або ПОВЕРНЕННЯ НАЗАД
async def back_write_group(query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await query.message.delete()
    await query.message.answer("Надсилання повідомлення відміненно ✅", reply_markup=kb_client)

async def back_write_group_message(query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await query.message.edit_text(
        "Щоб написати повідомлення іншій групі\nспочатку виберіть її ім'я нижче ⬇️",
        reply_markup = await inline_kb_group())
    await FSMWrite.group.set()
#==============================


# ===========================Фото кота 🖼============================
async def choose_random_photo():
    folder_path = 'E:\KOTEKBOT\photo'
    file_list = os.listdir(folder_path)
    random_file = random.choice(file_list)
    file_path = os.path.join(folder_path, random_file)
    return file_path

async def send_random_cat_photo(message: types.Message):
    await stats_schedule_add("Фото кота 🖼", 1)
    photo_path = await choose_random_photo()
    with open(photo_path, 'rb') as photo:
        await message.answer_photo(photo)


async def register_handler_stats(dp: Dispatcher):
    dp.register_callback_query_handler(text_save, text = "edit_text", state=None)
    dp.register_callback_query_handler(cancel, text = "cancel", state=FSMWrite.text)
    dp.register_message_handler(text_save1, state=FSMWrite.text)
    dp.register_message_handler(see_text, commands=["text"])
    dp.register_message_handler(send_random_cat_photo, text = "Фото кота 🖼")
    dp.register_message_handler(see_text, Text(ignore_case=True, equals="Замітки 📝"))
    dp.register_message_handler(write, Text(ignore_case=True, equals="Написати ✉️"), state=None)

    # Cкасувати вибір групи
    dp.register_callback_query_handler(back_write_group, text = "Назад", state=FSMWrite.group)
    # Вибрав групу
    for text in await get_list():
        dp.register_callback_query_handler(write_group, lambda c, t=text: c.data == t, state=FSMWrite.group)

    # Повернутись до вибору групи
    dp.register_callback_query_handler(back_write_group_message, text = "інша", state=FSMWrite.message_group) 
    # Надіслав повідомлення
    dp.register_message_handler(write_group_message_text, content_types=["text"], state=FSMWrite.message_group)
    dp.register_message_handler(write_group_message_photo, content_types=["photo"],state=FSMWrite.message_group)
    dp.register_message_handler(write_group_message_sticker, content_types=["sticker"],state=FSMWrite.message_group)
    dp.register_message_handler(write_group_message_video, content_types=["video"],state=FSMWrite.message_group) 
    dp.register_message_handler(write_group_message_animation, content_types=["animation"],state=FSMWrite.message_group) 
