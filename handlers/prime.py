import os
import random
import asyncio

from keyboards import *
from create_bot import bot
from aiogram import types, Router, F
from data_base import Database


from aiogram.fsm.context import FSMContext

from aiogram.filters import Text, Command

from aiogram.filters.state import State, StatesGroup

router = Router()


# =========Класс машини стану=========
class FSMWrite(StatesGroup):
    text = State()
    group = State()
    teach = State()
    message_group = State()
    message_teach = State()


# ======================================================================================
# Відмінна редагування тексту заміток
@router.callback_query(FSMWrite.text, Text(text="cancel"))
async def cancel(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_text(
        "Редагування тексту успішно відмінено✅", reply_markup=await text_inline_kb()
    )
    await state.clear()


# ======================================================================================


# ======================================================================================
# Редагування замітки
@router.callback_query(Text(text="edit_text"))
async def text_save(query: types.CallbackQuery, state: FSMContext):
    obj_msg = await query.message.edit_text(
        """
Тепер введіть текст який буде міститися
у замітках вашої групи

Наприклад :
Електронний щоденник: посилання на сайт

Чергування : посилання на сайт

Ви ж можете написати будь-що це лише приклад.""",
        reply_markup=await cancle_inline_kb(),
    )
    await state.set_state(FSMWrite.text)
    await state.update_data(message=obj_msg)


@router.message(FSMWrite.text)
async def text_save1(message: types.Message, state: FSMContext):
    db = await Database.setup()

    print("here")
    await message.delete()
    data = await state.get_data()
    data_message: types.Message = data["message"]
    await data_message.delete()
    print("here")

    if await db.student_exists_sql(message.from_user.id):
        if len(message.text) <= 1:
            await message.answer(
                "Текст надто короткий спробуй ще раз",
                reply_markup=await text_inline_kb(),
            )
            await state.clear()
        else:
            text = message.text
            groups = await db.group_for_student_id_sql(message.from_user.id)
            await db.add_text_sql(text, groups)
            await message.answer(
                "Замітки для вашої групи :\n\n"
                + text
                + "\n\nЩоб встановити нові\nнатисніть кнопку нижче",
                reply_markup=await text_inline_kb(),
            )
            await state.clear()
    elif await db.teacher_exists_sql(message.from_user.id):
        if len(message.text) <= 1:
            await message.answer(
                "Текст надто короткий спробуй ще раз",
                reply_markup=await text_inline_kb(),
            )
            await state.clear()
        else:
            text = message.text
            groups = await db.see_group_for_teach_id(message.from_user.id)
            await db.add_text_sql(text, groups)
            await message.answer(
                "Замітку успішно додано ✅", reply_markup=await text_inline_kb()
            )
            await state.clear()
    else:
        await message.answer("Ви не зареєстровані у групах")
        await state.clear()


# ======================================================================================


# ======================================================================================
# Перегляд замітки
@router.message(Command("text"))
@router.message(Text(text="Замітки 📝", ignore_case=True))
async def see_text(message: types.Message):
    db = await Database.setup()
    if await db.student_exists_sql(message.from_user.id):
        groups = await db.group_for_student_id_sql(message.from_user.id)
        boolean, text = await db.see_text_sql(groups)
        if boolean:
            await message.answer(
                "Замітки для вашої групи :\n\n"
                + text
                + "\n\nЩоб встановити нові\nнатисніть кнопку нижче",
                reply_markup=await text_inline_kb(),
            )
        elif not boolean:
            await message.answer(
                "У вашої групи не додано ніякого тексту\nЩоб це зробити\nнатисніть кнопку нижче",
                reply_markup=await text_inline_kb(),
            )
    elif await db.teacher_exists_sql(message.from_user.id):
        groups = await db.see_group_for_teach_id(message.from_user.id)
        boolean, text = await db.see_text_sql(groups)
        if boolean:
            await message.answer(
                "Ваші замітки :\n\n"
                + text
                + "\n\nЩоб встановити нові\nнатисніть кнопку нижче",
                reply_markup=await text_inline_kb(),
            )
        elif not boolean:
            await message.answer(
                "У вас не додано ніякого тексту\nЩоб це зробити\nнатисніть кнопку нижче",
                reply_markup=await text_inline_kb(),
            )
    else:
        await message.answer("Ви не зареєстровані")


# ======================================================================================


# ======================================================================================
# ============= отримання данних =============
async def get_user_data(message: types.Message, state: FSMContext):
    db = await Database.setup()
    msg_data = await state.get_data()
    group = msg_data["group"]
    msg_id = msg_data["msg_id"]
    chat_id = msg_data["chat_id"]

    group_user_writer = await db.group_for_student_id_sql(message.from_user.id)
    all_user_their = await db.list_id_student_agreed_write_sql(group)
    all_user_us = await db.list_id_student_agreed_write_sql(group_user_writer)
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


# ============= функція написати 1 етап | вибір групи
@router.message(Text(text="Написати ✉️", ignore_case=True))
async def write(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if not await db.student_exists_sql(message.from_user.id):
        await message.answer("Функція доступна тільки\nзареєстрованим студентам ❌")
        return

    if not await db.student_agreed_write_exsists_sql(message.from_user.id):
        await message.answer(
            """
Щоб користуватися цією функцією, 
вам необхідно увімкнути отримання 
"Повідомленнь від інших груп ✅" 

Для цього перйдіть в меню >
Інше 📌/Налаштування ⚙️
або натисніть /settings
        """
        )
        return

    await message.delete()

    msg = await message.answer("deletekb", reply_markup=types.ReplyKeyboardRemove())
    await msg.delete()

    await message.answer(
        "Щоб написати повідомлення іншій групі\nспочатку виберіть її ім'я нижче ⬇️",
        reply_markup=await inline_kb_student_group(),
    )
    await state.set_state(FSMWrite.group)


# ============= функція написати 2 етап | написання повідомлення
@router.callback_query(FSMWrite.group)
async def write_group(query: types.CallbackQuery, state: FSMContext):
    db = await Database.setup()
    group = await db.student_group_exists_sql(query.data)

    if query.data == "Назад":
        await state.clear()
        await query.message.delete()
        await query.message.answer(
            "Надсилання повідомлення відмінено ✅", reply_markup=await student_kb()
        )
        return

    if not group:
        await state.clear()
        await query.message.delete()
        await query.message.answer(
            "Такої групи не існує, спробуйте ще раз", reply_markup=await student_kb()
        )
        return

    await state.set_state(FSMWrite.message_group)
    await query.message.delete_reply_markup()
    message = await query.message.edit_text(
        f"Надішліть :\n • Текст 📝\n • Фото 🖼\n • Відео 📼\n • Стікер 💌\n • GIF 🪨",
        reply_markup=await back_inline_kb(),
    )
    await state.update_data(
        group=query.data, msg_id=message.message_id, chat_id=message.chat.id
    )


# ============= функція написати 3 етап | Надсилання повідомлення
# ============= надслання текстового повідомлення
@router.message(FSMWrite.message_group, F.text)
async def write_group_message_text(message: types.Message, state: FSMContext):
    group, group_user_writer, all_user_us, all_user_their = await get_user_data(
        message, state
    )
    text = message.text
    data = None

    if group == group_user_writer:
        all_user_us_ids = map(lambda e: e[0], all_user_us)
        groups = None
        await asyncio.gather(
            *map(send_notification(1, text, data, groups), all_user_us_ids)
        )
        await message.answer("Надісланно ✅", reply_markup=await student_kb())

    else:
        if bool(len(all_user_their)):
            all_user_us_id = map(lambda e: e[0], all_user_us)
            all_user_their_id = map(lambda e: e[0], all_user_their)
            groups = [group, group_user_writer]

            await asyncio.gather(
                *map(send_notification(2, text, data, groups), all_user_us_id)
            )
            await asyncio.gather(
                *map(send_notification(3, text, data, groups), all_user_their_id)
            )

            await message.answer("Надісланно ✅", reply_markup=await student_kb())

        elif bool(len(all_user_their)) == False:
            await message.answer(
                f"Немає студентів у групі {group} ❌", reply_markup=await student_kb()
            )
    await state.clear()


# ============= надслання фото повідомлення
@router.message(FSMWrite.message_group, F.photo)
async def write_group_message_photo(message: types.Message, state: FSMContext):
    group, group_user_writer, all_user_us, all_user_their = await get_user_data(
        message, state
    )
    text = None
    photo = message.photo[0].file_id

    if group == group_user_writer:
        all_user_us_ids = map(lambda e: e[0], all_user_us)
        groups = None
        await asyncio.gather(
            *map(send_notification(4, text, photo, groups), all_user_us_ids)
        )
        await message.answer("Надісланно ✅", reply_markup=await student_kb())

    else:
        if bool(len(all_user_their)):
            all_user_us_id = map(lambda e: e[0], all_user_us)
            all_user_their_id = map(lambda e: e[0], all_user_their)
            groups = [group, group_user_writer]

            await asyncio.gather(
                *map(send_notification(5, text, photo, groups), all_user_us_id)
            )
            await asyncio.gather(
                *map(send_notification(6, text, photo, groups), all_user_their_id)
            )

            await message.answer("Надісланно ✅", reply_markup=await student_kb())

        elif bool(len(all_user_their)) == False:
            await message.answer(
                f"Немає студентів у групі {group} ❌", reply_markup=await student_kb
            )
    await state.clear()


# ============= надслання стікер повідомлення
@router.message(FSMWrite.message_group, F.sticker)
async def write_group_message_sticker(message: types.Message, state: FSMContext):
    group, group_user_writer, all_user_us, all_user_their = await get_user_data(
        message, state
    )
    text = None
    sticker = message.sticker.file_id

    if group == group_user_writer:
        all_user_us_ids = map(lambda e: e[0], all_user_us)
        groups = None
        await asyncio.gather(
            *map(send_notification(7, text, sticker, groups), all_user_us_ids)
        )
        await message.answer("Надісланно ✅", reply_markup=await student_kb())

    else:
        if bool(len(all_user_their)):
            all_user_us_id = map(lambda e: e[0], all_user_us)
            all_user_their_id = map(lambda e: e[0], all_user_their)
            groups = [group, group_user_writer]

            await asyncio.gather(
                *map(send_notification(8, text, sticker, groups), all_user_us_id)
            )
            await asyncio.gather(
                *map(send_notification(9, text, sticker, groups), all_user_their_id)
            )

            await message.answer("Надісланно ✅", reply_markup=await student_kb())

        elif bool(len(all_user_their)) == False:
            await message.answer(
                f"Немає студентів у групі {group} ❌", reply_markup=await student_kb()
            )
    await state.clear()


# ============= надслання відео повідомлення
@router.message(FSMWrite.message_group, F.video)
async def write_group_message_video(message: types.Message, state: FSMContext):
    group, group_user_writer, all_user_us, all_user_their = await get_user_data(
        message, state
    )
    text = None
    video = message.video.file_id

    if group == group_user_writer:
        all_user_us_ids = map(lambda e: e[0], all_user_us)
        groups = None
        await asyncio.gather(
            *map(send_notification(10, text, video, groups), all_user_us_ids)
        )
        await message.answer("Надісланно ✅", reply_markup=await student_kb())

    else:
        if bool(len(all_user_their)):
            all_user_us_id = map(lambda e: e[0], all_user_us)
            all_user_their_id = map(lambda e: e[0], all_user_their)
            groups = [group, group_user_writer]

            await asyncio.gather(
                *map(send_notification(11, text, video, groups), all_user_us_id)
            )
            await asyncio.gather(
                *map(send_notification(12, text, video, groups), all_user_their_id)
            )

            await message.answer("Надісланно ✅", reply_markup=await student_kb())

        elif bool(len(all_user_their)) == False:
            await message.answer(
                f"Немає студентів у групі {group} ❌", reply_markup=await student_kb()
            )
    await state.clear()


# ============= надслання gif повідомлення
@router.message(FSMWrite.message_group, F.animation)
async def write_group_message_animation(message: types.Message, state: FSMContext):
    group, group_user_writer, all_user_us, all_user_their = await get_user_data(
        message, state
    )
    text = None
    animation = message.animation.file_id

    if group == group_user_writer:
        all_user_us_ids = map(lambda e: e[0], all_user_us)
        groups = None
        await asyncio.gather(
            *map(send_notification(13, text, animation, groups), all_user_us_ids)
        )
        await message.answer("Надісланно ✅", reply_markup=await student_kb())

    else:
        if bool(len(all_user_their)):
            all_user_us_id = map(lambda e: e[0], all_user_us)
            all_user_their_id = map(lambda e: e[0], all_user_their)
            groups = [group, group_user_writer]

            await asyncio.gather(
                *map(send_notification(14, text, animation, groups), all_user_us_id)
            )
            await asyncio.gather(
                *map(send_notification(15, text, animation, groups), all_user_their_id)
            )

            await message.answer("Надісланно ✅", reply_markup=await student_kb())

        elif bool(len(all_user_their)) == False:
            await message.answer(
                f"Немає студентів у групі {group} ❌", reply_markup=await student_kb()
            )
    await state.clear()


# Функція надсилання
def send_notification(what_send: int, text: str, file_id: str, groups: list):
    async def wrapped(user_id: int):
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
                await bot.send_photo(user_id, file_id, caption=f"Від нашої групи :")
            elif what_send == 5:
                await bot.send_photo(user_id, file_id, caption=f"Ми до {groups[0]} :")
            elif what_send == 6:
                await bot.send_photo(
                    user_id, file_id, caption=f"{groups[1]} надсилає :"
                )

            # STICKER
            elif what_send == 7:
                await bot.send_message(user_id, f"Від нашої групи :")
                await bot.send_sticker(user_id, file_id)
            elif what_send == 8:
                await bot.send_message(user_id, f"Ми до {groups[0]} :")
                await bot.send_sticker(user_id, file_id)
            elif what_send == 9:
                await bot.send_message(user_id, f"{groups[1]} надсилає :")
                await bot.send_sticker(user_id, file_id)

            # VIDEO
            elif what_send == 10:
                await bot.send_video(user_id, file_id, caption=f"Від нашої групи :")
            elif what_send == 11:
                await bot.send_video(user_id, file_id, caption=f"Ми до {groups[0]} :")
            elif what_send == 12:
                await bot.send_video(
                    user_id, file_id, caption=f"{groups[1]} надсилає :"
                )

            # ANIMATION
            elif what_send == 13:
                await bot.send_message(user_id, f"Від нашої групи :")
                await bot.send_animation(user_id, file_id)
            elif what_send == 14:
                await bot.send_message(user_id, f"Ми до {groups[0]} :")
                await bot.send_animation(user_id, file_id)
            elif what_send == 15:
                await bot.send_message(user_id, f"{groups[1]} надсилає :")
                await bot.send_animation(user_id, file_id)
        except:
            pass

    return wrapped


# ======================================================================================


# ======================================================================================
# ================= ВІДМІНА ДІЇ або ПОВЕРНЕННЯ НАЗАД
@router.callback_query(FSMWrite.message_group, Text(text="інша"))
async def back_write_group_message(query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await query.message.edit_text(
        "Щоб написати повідомлення іншій групі\nспочатку виберіть її ім'я нижче ⬇️",
        reply_markup=await inline_kb_student_group(),
    )
    await state.set_state(FSMWrite.group)


# ======================================================================================


# ======================================================================================
# ===========================Фото кота 🖼============================
async def choose_random_photo():
    folder_path = "cat/"
    file_list = os.listdir(folder_path)
    random_file = random.choice(file_list)
    file_path = os.path.join(folder_path, random_file)
    return file_path


@router.message(Text(text="Фото кота 🖼", ignore_case=True))
async def send_random_cat_photo(message: types.Message):
    try:
        photo_path = await choose_random_photo()
        file_path = types.FSInputFile(photo_path)
        await message.answer_photo(file_path)
    except:
        await message.answer("Фото кота ще не додано 😿")


# ======================================================================================
