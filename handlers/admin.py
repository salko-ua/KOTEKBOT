from aiogram.types import Message
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import BotBlocked, RetryAfter
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import *
import asyncio
from aiogram.types import ReplyKeyboardRemove
from create_bot import bot
from translate import Translator
from config import super_admin_admin, super_admin_ura
from data_base import Database

translator = Translator(to_lang="uk")

# =========Класс машини стану=========
class FSMAdmin(StatesGroup):
    #new news
    photo = State()
    text = State()
    mixed_photo = State()
    mixed_text = State()

# ===========================Видалити акаунт============================
# @dp.message_handler(text ='Видалити акаунт')
async def delete_admin(message: Message):
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

#надсилання одного з варіантів
async def send_photo_news(message: Message):
    db = await Database.setup()
    if await db.admin_exists_sql(message.from_user.id):
        await message.answer("Надішліть фото 🖼", reply_markup=ReplyKeyboardRemove())
        await FSMAdmin.photo.set()

async def send_message_news(message: Message):
    db = await Database.setup()
    if await db.admin_exists_sql(message.from_user.id):
        await message.answer("Надішліть текст 📝", reply_markup=ReplyKeyboardRemove())
        await FSMAdmin.text.set()

async def send_mixed_news(message: Message):
    db = await Database.setup()
    if await db.admin_exists_sql(message.from_user.id):
        await message.answer("Надішліть текст 📝", reply_markup=ReplyKeyboardRemove())
        await FSMAdmin.mixed_text.set()
    
#Другий етап
async def send_photo_news1(message: Message, state: FSMContext):
    db = await Database.setup()
    if await db.admin_exists_sql(message.from_user.id):
        photo = message.photo[0].file_id
        text = None
        what_send = 1

        await message.answer("Надсилається..", reply_markup=kb_admin)
        await state.finish()

        all_user_ids = map(lambda e: e[0], await db.all_user_id_sql())
        await asyncio.gather(*map(send_notification(what_send, text, photo), all_user_ids))
        await message.answer("Надсилання закінчено!")

async def send_message_news1(message: Message, state: FSMContext):
    db = await Database.setup()
    if await db.admin_exists_sql(message.from_user.id):
        photo = None
        text = message.text
        what_send = 2

        await message.answer("Надсилається..", reply_markup=kb_admin)
        await state.finish()

        all_user_ids = map(lambda e: e[0], await db.all_user_id_sql())
        await asyncio.gather(*map(send_notification(what_send, text, photo), all_user_ids))
        await message.answer("Надсилання закінчено!")

async def send_mixed_news1(message: Message, state: FSMContext):
    db = await Database.setup()
    if await db.admin_exists_sql(message.from_user.id):
        async with state.proxy() as data:
            data["text"] = message.text
        await message.answer("Надішліть фото 🖼")
        await FSMAdmin.mixed_photo.set()

#3 етап тільки для змішаної новини
async def send_mixed_news2(message: Message, state: FSMContext):
    db = await Database.setup()
    if await db.admin_exists_sql(message.from_user.id):
        async with state.proxy() as data:
            text = data["text"]
            photo = message.photo[0].file_id
            what_send = 3

        await message.answer("Надсилається..", reply_markup=kb_admin)
        await state.finish()

        all_user_ids = map(lambda e: e[0], await db.all_user_id_sql())
        await asyncio.gather(*map(send_notification(what_send, text, photo), all_user_ids))
        await message.answer("Надсилання закінчено!")

#Функція надсилання
def send_notification(what_send: int, text: str, photo: str):
    async def wrapped(user_id: int):
        db = await Database.setup()
        try:
            try:
                if what_send == 1:
                    await bot.send_photo(user_id, photo)
                elif what_send == 2:
                    await bot.send_message(user_id, text)
                elif what_send == 3:
                    await bot.send_photo(user_id, photo, text)
            except RetryAfter as ra:
                await asyncio.sleep(ra.timeout)
        except:
            pass
    
    return wrapped

# ===========================реєстратор============================
def register_handler_admin(dp: Dispatcher):
    # ===========================Викласти фото=============================
    dp.register_message_handler(send_photo_news, text="Викласти 🖼")
    dp.register_message_handler(send_photo_news1, content_types=["photo"], state=FSMAdmin.photo)
    # ===========================Викласти текст=============================
    dp.register_message_handler(send_message_news, text="Викласти 📝")
    dp.register_message_handler(send_message_news1, state=FSMAdmin.text)
    # ===========================Викласти фото і текст=============================
    dp.register_message_handler(send_mixed_news, text="Викласти 🖼📝")
    dp.register_message_handler(send_mixed_news1, state=FSMAdmin.mixed_text)
    dp.register_message_handler(send_mixed_news2, content_types=["photo"], state=FSMAdmin.mixed_photo)
    # ===========================Видалити акаунт=============================
    dp.register_message_handler(delete_admin, text="Видалити акаунт")
