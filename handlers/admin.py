from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import BotBlocked
from aiogram.dispatcher.filters.state import State, StatesGroup
from data_base.controller_db import *
from keyboards import kb_admin, kb_all_or_one ,get_kb , kb_dont, kb_ys
import asyncio
from aiogram.types import ReplyKeyboardRemove
import datetime
from create_bot import bot
from translate import Translator
from config import super_admin

translator = Translator(to_lang="uk")


#=========Класс машини стану=========
class FSMAdmin(StatesGroup):
    #GROP MANAGMENT
    curse_group = State()
    curse_group_delete = State()
    #Розклад пар
    curse_group_rad = State()
    curse_group_rad_photo = State()
    curse_group_rad_delete = State()
    #NEWS
    all_or_one = State()
    text_news = State()
    photo_news = State()
    namegroups = State()
    #Розклад дзвінків
    id_photo = State()
    type = State()


#===========================Додавання групи============================
#@dp.message_handler(text = "Додати групу", state=None)
async def add_group(message: types.Message):
    if await admin_exists_sql(message.from_user.id) or message.from_user.id == super_admin:
        await FSMAdmin.curse_group.set()
        await message.answer("Введіть назву\nПриклад : 2Ц" , reply_markup = ReplyKeyboardRemove())

    else:
        await message.answer("Ви не адмін :D /start")

#@dp.message_handler(state=FSMAdmin.curse_group)
async def add_group1(message: types.Message, state: FSMContext):
    if await admin_exists_sql(message.from_user.id) or message.from_user.id == super_admin:
        if message.text == "Назад":
            await state.finish()
        else:
            async with state.proxy() as data:
                data['curse_group'] = message.text
            fullname = data["curse_group"]
            if(not await group_exists_sql(fullname)):
                if len(fullname) <=3:
                    await add_group_sql(message.from_user.id, fullname)
                    await message.answer("Групу додано",reply_markup = kb_admin)
                    await state.finish()
                else:
                    await message.answer("Назва групи не може перевищувати три символи",reply_markup = kb_admin)
                    await state.finish()
            else:
                await message.answer("Група з такою назвою вже є",reply_markup = kb_admin)
                await state.finish()
    else:
        await message.answer("Ви не адмін :D /start")
        await state.finish()


#===========================Додати розклад до курсу============================
#@dp.message_handler(text = "Додати розклад до групи", state=None)
async def add_schedule_to_group(message: types.Message):
    if await admin_exists_sql(message.from_user.id) or message.from_user.id == super_admin:
        await FSMAdmin.curse_group_rad_photo.set()
        await message.answer("Киньте фото розкладу" , reply_markup = ReplyKeyboardRemove())

    else:
        await message.answer("Ви не адмін :D /start")

#@dp.message_handler(content_types=['photo'],state = FSMAdmin.curse_group_rad_photo)
async def add_schedule_to_group1(message: types.Message, state: FSMContext):
    if await admin_exists_sql(message.from_user.id) or message.from_user.id == super_admin:
        async with state.proxy() as data:
            data["curse_group_rad_photo"] = message.photo[0].file_id
        await clear_sql()
        await group_list_sql()
        await FSMAdmin.curse_group_rad.set()
        await message.answer("До якої групи привязати" , reply_markup = get_kb())

    else:
        await message.answer("Ви не адмін :D /start")

        await state.finish()

#@dp.message_handler(state = FSMAdmin.curse_group_rad)
async def add_schedule_to_group2(message: types.Message, state: FSMContext):
    if await admin_exists_sql(message.from_user.id) or message.from_user.id == super_admin:
        async with state.proxy() as data:
            data["curse_group_rad"] = message.text
        now = datetime.datetime.now()
        now = now.strftime("%d - %B, %A, %H:%M")
        translation = translator.translate(now)
        await group_photo_update_sql(data["curse_group_rad_photo"],data["curse_group_rad"],"Зміненно: "+translation)
        await message.answer('Розклад успішно добавлено',reply_markup=kb_admin)

        await state.finish()
    else:
        await message.answer("Ви не адмін :D /start")

        await state.finish()


#===========================Список груп============================
#@dp.message_handler(text ='Список груп')
async def list_group(message: types.Message):
    if await admin_exists_sql(message.from_user.id) or message.from_user.id == super_admin:
        await clear_sql()
        if await get_list_sql():
            await message.answer(f"Список груп наявних в базі даних : \n{get_list.get()}")

        elif not await get_list_sql():
            await message.answer(f"Немає жодної групи")

    else:
        await message.answer("Ви не адмін :D /start")

        
#===========================Видалити акаунт============================
#@dp.message_handler(text ='Видалити акаунт')
async def delete_admin(message: types.Message):
    if await admin_exists_sql(message.from_user.id) or message.from_user.id == super_admin:
        await delete_admins_sql(message.from_user.id)
        await message.answer("Акаунт видалено \nНажміть /start для регестрації", reply_markup = ReplyKeyboardRemove())

    else:
        await message.answer("Ви не адмін :D /start", reply_markup = ReplyKeyboardRemove())


#===========================Видалити групу============================
#@dp.message_handler(text ="Видалити групу", state=None)
async def delete_group(message: types.Message):
    await clear_sql()
    await group_list_sql()
    if await admin_exists_sql(message.from_user.id) or message.from_user.id == super_admin:
        await FSMAdmin.curse_group_delete.set()
        await message.answer("Виберіть групу з наведених нижче",reply_markup=get_kb())

    else:
        await message.answer("Ви не адмін :D /start", reply_markup = ReplyKeyboardRemove())
      
#@dp.message_handler(state=FSMAdmin.curse_group_delete)
async def load_group(message: types.Message, state: FSMContext):
    if await admin_exists_sql(message.from_user.id) or message.from_user.id == super_admin:
        if message.text == "Назад":
            await state.finish()
        else:
            async with state.proxy() as data:
                data['curse_group_delete'] = message.text
            fullname = data["curse_group_delete"]
            if(await group_exists_sql(fullname)):
                if len(fullname) <=3:
                    if await user_group_exists_sql(fullname):
                        await delete_groups_sql(fullname)
                        await delete_user_groups_sql(fullname)
                        await message.answer("Групу видалено і всіх користувачів які були до неї підключенні",reply_markup = kb_admin)

                    elif not await user_group_exists_sql(fullname):
                        await delete_groups_sql(fullname)
                        await message.answer("Групу видалено",reply_markup = kb_admin)

                    await state.finish()
                else:
                    await message.answer("Назва групи не може перевищувати три символи",reply_markup = kb_admin)

            else:
                await message.answer("Група з такою назвою немає",reply_markup = kb_admin)
                 
                await state.finish()
    else:
        await message.answer("Ви не адмін :D /start")

        await state.finish()


#===========================Новина============================
#@dp.message_handler(text ="Викласти новину", state=None)
async def send_news(message: types.Message):
    if await admin_exists_sql(message.from_user.id) or message.from_user.id == super_admin:
        await message.answer("Куди надіслати (одна група\всі групи)",reply_markup = kb_all_or_one)

        await FSMAdmin.all_or_one.set()
    elif message.text == "Назад":
        await message.answer("Ваша клавіатура : ", reply_markup = kb_admin)

    else:
        await message.answer("Ви не адмін :D /start", reply_markup = ReplyKeyboardRemove())

#@dp.message_handler(state = FSMAdmin.all_or_one)
async def send_news1(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await message.answer("Ваша клавіатура : ", reply_markup = kb_admin)

        await state.finish()
    elif await admin_exists_sql(message.from_user.id) or message.from_user.id == super_admin:
        async with state.proxy() as data:
            data['all_or_one'] = message.text
        await message.answer("Введіть текст новини :",reply_markup=ReplyKeyboardRemove())

        await FSMAdmin.text_news.set()
    else:
        await message.answer("Ви не адмін :D /start", reply_markup = ReplyKeyboardRemove())

        await state.finish()

#@dp.message_handler(state = FSMAdmin.text_news)
async def send_news2(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await message.answer("Ваша клавіатура : ", reply_markup = kb_admin)

        await state.finish()
    elif await admin_exists_sql(message.from_user.id) or message.from_user.id == super_admin:
        async with state.proxy() as data:
                data['text_news'] = message.text
        await FSMAdmin.photo_news.set()
        await message.answer("Скиньте фото новини або натисніть кнопку (не треба) якщо новина без фото)", reply_markup=kb_dont)

    else:
        await message.answer("Ви не адмін :D /start", reply_markup = ReplyKeyboardRemove())

        await state.finish()

#@dp.message_handler(state = FSMAdmin.photo_news)
async def send_news3(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await message.answer("Ваша клавіатура : ", reply_markup = kb_admin)

        await state.finish()
    elif await admin_exists_sql(message.from_user.id) or message.from_user.id == super_admin:
        if message.text == "не треба":
            async with state.proxy() as data:
                data['photo_news'] = "a"
                if data['all_or_one'] == "Одна":
                    await clear_sql()
                    await group_list_sql()
                    await FSMAdmin.namegroups.set()
                    await message.answer("Виберіть назву групи :", reply_markup = get_kb())

                elif data["all_or_one"] == "Всі":
                    await FSMAdmin.namegroups.set()
                    await message.answer("Надсилати новину ?", reply_markup = kb_ys)


    else:
        await message.answer("Ви не адмін :D /start", reply_markup = ReplyKeyboardRemove())

        await state.finish()

#@dp.message_handler(content_types=['photo'],state = FSMAdmin.photo_news)
async def send_news4(message: types.Message, state: FSMContext):
        if message.text == "Назад":
            await message.answer("Ваша клавіатура : ", reply_markup = kb_admin)

            await state.finish()
        elif await admin_exists_sql(message.from_user.id) or message.from_user.id == super_admin:
            async with state.proxy() as data:
                if data['all_or_one'] == 'Одна':
                    async with state.proxy() as data:
                            data['photo_news'] = message.photo[0].file_id
                    await FSMAdmin.namegroups.set()
                    await clear_sql()
                    await group_list_sql()
                    await message.answer("Виберіть назву групи :", reply_markup = get_kb())

                elif data['all_or_one'] == 'Всі':
                    async with state.proxy() as data:
                            data['photo_news'] = message.photo[0].file_id
                    await FSMAdmin.namegroups.set()
                    await message.answer("Підтвердити надсилання", reply_markup=kb_ys)

        else:
            await message.answer("Ви не адмін :D /start", reply_markup = ReplyKeyboardRemove())

            await state.finish()

#@dp.message_handler(state = FSMAdmin.namegroups)
async def send_news5(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await message.answer("Ваша клавіатура : ", reply_markup = kb_admin)
        await state.finish()
    elif await admin_exists_sql(message.from_user.id) or message.from_user.id == super_admin:
        async with state.proxy() as data:
            data['namegroups'] = message.text
        if data['all_or_one'] == 'Одна':
            try:
                h = await id_from_group_exists_sql(data["namegroups"])
                error = h[0][0]
                new = []
                for i in range(0,len(h)):
                    new.append(h[i][0])
                if len(data['photo_news']) > 3:
                    texts = data["text_news"]
                    photo = data["photo_news"]
                    for all_id in range(0,len(new)):
                        try:
                            await bot.send_photo(new[all_id],photo,texts)
                        except BotBlocked:
                            await asyncio.sleep(0.5)
                    await message.answer("Готово!",reply_markup=kb_admin)
                    await state.finish()   
                elif len(data["photo_news"]) == 1:
                    for all_ids in range(0,len(new)):
                        try:
                            await bot.send_message(new[all_ids], data['text_news'])
                        except BotBlocked:
                            await asyncio.sleep(0.5)
                    await message.answer("Готово!",reply_markup=kb_admin)   
                    await state.finish()     
            except IndexError:
                await message.answer("немає жодної людини підключенної до цієї групи",reply_markup=kb_admin)
                await state.finish()    
                 
        if data['all_or_one'] == 'Всі':
            await all_user_id_sql()
            lis = all_user.get()
            rest = []
            for i in range(0,len(lis)):
                rest.append(lis[i][0])
            #print(rest)
            async with state.proxy() as data:
                if len(data['photo_news']) > 3:
                    texts = data["text_news"]
                    photo = data["photo_news"]
                    for all_id in range(0,len(rest)):
                        try:
                            await bot.send_photo(rest[all_id],photo,texts)
                        except BotBlocked:
                            await asyncio.sleep(0.5)
                    await message.answer("Готово!",reply_markup=kb_admin)
                    await state.finish()
                elif len(data["photo_news"]) == 1:
                    for all_ids in range(0,len(rest)):
                        try:
                            await bot.send_message(rest[all_ids], data['text_news'])
                        except BotBlocked:
                            await asyncio.sleep(0.5)
                    await message.answer("Готово!",reply_markup=kb_admin)
                    await state.finish()
    elif message.text == "Назад":
        await message.answer("Ваша клавіатура : ", reply_markup = kb_admin)

        await state.finish()
    else:
        await message.answer("Ви не адмін :D /start", reply_markup = ReplyKeyboardRemove())

        await state.finish()


#===========================Додати розклад дзвінків============================
#@dp.message_handler(text ="Додати розклад дзвінків", state=None)
async def add_calls(message: types.Message):
    if await admin_exists_sql(message.from_user.id) or message.from_user.id == super_admin:
        await message.answer("Завантажте фото", reply_markup = ReplyKeyboardRemove())

        await FSMAdmin.id_photo.set()
    elif message.text == "Назад":
        await message.answer("Ваша клавіатура : ", reply_markup = kb_admin)

    else:
        await message.answer("Ви не адмін :D /start", reply_markup = ReplyKeyboardRemove())

#@dp.message_handler(content_types=['photo'],state = FSMAdmin.id_photo)
async def add_calls1(message: types.Message, state: FSMContext):
    if await admin_exists_sql(message.from_user.id) or message.from_user.id == super_admin:
        async with state.proxy() as data:
            data["id_photo"] = message.photo[0].file_id
            data["type"] = "calls"
        now = datetime.datetime.now()
        now = now.strftime("%d - %B, %A, %H:%M")
        translation = translator.translate(now)
        await add_calls_sql(data["type"],data["id_photo"],"Зміненно: "+translation)
        await state.finish()
        await message.answer("Розклад дзвінків успішно оновлено",reply_markup=kb_admin)

    elif message.text == "Назад":
        await message.answer("Ваша клавіатура : ", reply_markup = kb_admin)

    else:
        await message.answer("Ви не адмін :D /start", reply_markup = ReplyKeyboardRemove())


#===========================Видалити розклад дзвінків============================
#@dp.message_handler(text ="Видалити розклад дзвінків")
async def delete_calls(message: types.Message):
    if await admin_exists_sql(message.from_user.id) or message.from_user.id == super_admin:
        check = await delete_calls_sql()
        if(not check):
            await message.answer("Розкладу дзвінків ще не додано", reply_markup = kb_admin)

        elif check:
            await message.answer("Розклад дзвінків успішно видалено", reply_markup = kb_admin)

    elif message.text == "Назад":
        await message.answer("Ваша клавіатура : ", reply_markup = kb_admin)

    else:
        await message.answer("Ви не адмін :D /start", reply_markup = ReplyKeyboardRemove())


#===========================реєстратор============================
def register_handler_admin(dp : Dispatcher):
    #===========================Додавання групи=============================
    dp.register_message_handler(add_group,text = "Додати групу", state=None)
    dp.register_message_handler(add_group1, state=FSMAdmin.curse_group)
    #===========================Додати розклад до курсу=====================
    dp.register_message_handler(add_schedule_to_group,text = "Додати розклад до групи", state=None)
    dp.register_message_handler(add_schedule_to_group1, content_types=['photo'],state = FSMAdmin.curse_group_rad_photo)
    dp.register_message_handler(add_schedule_to_group2, state = FSMAdmin.curse_group_rad)
    #===========================Список груп=================================
    dp.register_message_handler(list_group, text ='Список груп')
    #===========================Видалити акаунт=============================
    dp.register_message_handler(delete_admin,text ='Видалити акаунт')
    #===========================Видалити групу==============================
    dp.register_message_handler(delete_group, text ="Видалити групу",state=None)
    dp.register_message_handler(load_group, state=FSMAdmin.curse_group_delete)
    #===========================Новина======================================
    dp.register_message_handler(send_news,text ="Викласти новину",state=None)
    dp.register_message_handler(send_news1, state=FSMAdmin.all_or_one)
    dp.register_message_handler(send_news2, state=FSMAdmin.text_news)
    dp.register_message_handler(send_news3, state=FSMAdmin.photo_news)
    dp.register_message_handler(send_news4, content_types=['photo'],state=FSMAdmin.photo_news)
    dp.register_message_handler(send_news5, state=FSMAdmin.namegroups)
    #===========================Додати розклад дзвінків======================
    dp.register_message_handler(add_calls,text ="Додати розклад дзвінків",state=None)
    dp.register_message_handler(add_calls1,content_types=['photo'],state = FSMAdmin.id_photo)
    #===========================Видалити розклад дзвінків============================
    dp.register_message_handler(delete_calls,text ="Видалити розклад дзвінків")