import asyncio

from aiogram import F, Router, types
from aiogram.filters import Text
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from create_bot import bot
from data_base import Database
from keyboards import *

router = Router()


# =========Класс машини стану=========
class FSMWrite(StatesGroup):
    text = State()
    group = State()
    teach = State()
    message_group = State()
    message_teach = State()


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
@router.callback_query(F.data == "Написати ✉️")
async def write(query: types.CallbackQuery, state: FSMContext):
    db = await Database.setup()
    if not await db.student_exists_sql(query.from_user.id):
        await query.answer("Функція доступна тільки\nзареєстрованим студентам ❌")
        return

    if not await db.student_agreed_write_exsists_sql(query.from_user.id):
        text = (
            "Щоб користуватися цією функцією,\n"
            "вам необхідно увімкнути отримання\n"
            '"Повідомленнь від інших груп ✅"\n'
            "\n"
            "Для цього перейдіть в меню >\n"
            "Інше 📌/Налаштування ⚙️\n"
            "або натисніть /settings"
        )
        await query.answer(text)
        return

    await query.message.edit_text(
        "Щоб написати повідомлення іншій групі\nспочатку виберіть її ім'я нижче ⬇️"
    )
    await query.message.edit_reply_markup(reply_markup=await student_group_list_kb())
    await state.set_state(FSMWrite.group)


# ============= функція написати 2 етап | написання повідомлення
@router.callback_query(FSMWrite.group)
async def write_group(query: types.CallbackQuery, state: FSMContext):
    db = await Database.setup()
    group = await db.student_group_exists_sql(query.data)

    if query.data == "Назад":
        await state.clear()
        await query.answer("Надсилання відмінено ✅", show_alert=True)
        await query.message.delete()
        await query.message.answer(
            "Ваша клавіатура ⌨️", reply_markup=await student_kb()
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
        reply_markup=await prime_back_kb(),
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
        reply_markup=await student_group_list_kb(),
    )
    await state.set_state(FSMWrite.group)
