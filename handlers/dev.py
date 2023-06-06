from keyboards import *
from aiogram import types
from create_bot import bot

from aiogram.dispatcher import Dispatcher, FSMContext

from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMSDev(StatesGroup):
    text_error = State()
    text_response = State()


async def get_text(type: str, query: types.CallbackQuery = None):
    # Основний текст
    main_text = f"""
Це панель розробки бота 🤝

У ній ви можете :
   • Надіслати запит на участь
 у розробці цього бота.
   • Надіслати відгук про бота
 ваші особисті рекомендації і тп.
   • Надіслати інформацію про 
 помилку та інші проблеми.

Відгук і повідомлення про помилку
надсилаються анонімно @botadmincat    
    """

    # Текст для надсилання помилки
    error_text = f"""
Опишіть вашу проблему/помилку.

Також ви можете написати 
в особисті повідомлення
до @botadmincat 🙃   
    """
    
    # Текст для запиту
    request_text = f"""
Ви можете надіслати запит
на участь у розробці бота

для цього вам потрібно 
 • Навчатись у ВПК (будь - який курс)
 • Має бути @username
 • Знати :
    обов'язково
    - python (рівня джуна)
    - aiogram v2.25
    - SQL запити (aiosqlite)
    - Бути зареєстрованим(ою)
    на GitHub 
    - Трошки знати git
    інші бібліотеки
    можна довчити згодом
 • Також можна допомогти
 з виправленням помилок у
 тексті. Для цього знати
 те що вище не треба.
 • Не бути малоросом 😃
    """
    # Структура запиту для адміна

    if type == 'main':
        return main_text
    elif type == 'error':
        return error_text
    elif type == 'request_t':
        return request_text
    elif type == "request_admin":
        request_text_for_admin = f"запит\n{query.from_user.first_name}\n@{query.from_user.username}\n{query.from_user.id}"
        return request_text_for_admin



# main message
async def join_development(message: types.Message):
    await message.answer(await get_text('main'),reply_markup=dev_inline_kb,)


async def join_development_query(query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await query.message.edit_text(await get_text('main'))
    await query.message.edit_reply_markup(reply_markup=dev_inline_kb)


# error
async def error(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_text(await get_text('error'))
    await query.message.edit_reply_markup(reply_markup=dev_back_inline_kb)
    await FSMSDev.text_error.set()
    async with state.proxy() as data:
        data["message_obj_error"] = query


async def error_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        message_q: types.CallbackQuery = data["message_obj_error"]
    await message_q.message.edit_text(await get_text('main'))
    await message_q.message.edit_reply_markup(reply_markup=dev_inline_kb)
    await bot.send_message(chat_id=-1001873448980, message_thread_id=3, text = f"Помилка :\n{message.text}")
    await message.delete()
    await state.finish()


# response
async def response(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_text("Тепер можете написати відгук 🤝")
    await query.message.edit_reply_markup(reply_markup=dev_back_inline_kb)
    await FSMSDev.text_response.set()
    async with state.proxy() as data:
        data["message_obj_response"] = query


async def response_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        message_q: types.CallbackQuery = data["message_obj_response"]
    await message_q.message.edit_text(await get_text('main'))
    await message_q.message.edit_reply_markup(reply_markup=dev_inline_kb)
    await bot.send_message(chat_id=-1001873448980, message_thread_id=5, text = f"Відгук :\n{message.text}")
    await message.delete()
    await state.finish()


# ЗАПИТ НА УЧАСТЬ
async def request(query: types.CallbackQuery):
    await query.message.edit_text(await get_text('request_t'))
    await query.message.edit_reply_markup(reply_markup=dev_request_inline_kb)


async def confirm(query: types.CallbackQuery):
    await bot.send_message(chat_id=-1001873448980, message_thread_id=8, text = await get_text('request_admin', query=query))
    await query.message.edit_text(await get_text('main'))
    await query.message.edit_reply_markup(reply_markup=dev_inline_kb)


# ===========================реєстратор============================
def register_handler_dev(dp: Dispatcher):
    dp.register_message_handler(join_development, text="Розробка 🧩")
    # реагувати в станах
    dp.register_callback_query_handler(join_development_query, text="back_dev")
    dp.register_callback_query_handler(join_development_query, text="back_dev", state=FSMSDev.text_error)
    dp.register_callback_query_handler(join_development_query, text="back_dev", state=FSMSDev.text_response)
    # всі callback
    dp.register_callback_query_handler(request, text="request")
    dp.register_callback_query_handler(confirm, text="okay")
    dp.register_callback_query_handler(error, text="error", state=None)
    dp.register_callback_query_handler(response, text="response", state=None)
    # повідомлення про помилку і відгук
    dp.register_message_handler(error_text, state=FSMSDev.text_error)
    dp.register_message_handler(response_text, state=FSMSDev.text_response)
