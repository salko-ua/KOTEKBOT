from aiogram import F, Router, types
from aiogram.filters import Text
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from create_bot import bot
from keyboards import *

router = Router()


class FSMSDev(StatesGroup):
    text_error = State()
    text_response = State()
    text_request = State()


# ======================================================================================
async def get_text(type: str, message: types.Message = None):
    # Основний текст
    main_text = (
        "Це панель розробки бота 🤝\n\n"
        "У ній ви можете :\n"
        "   • Надіслати запит на участь"
        " у розробці цього бота.\n"
        "   • Надіслати відгук про бота"
        " ваші особисті рекомендації і тп.\n"
        "   • Надіслати інформацію про\n"
        " помилку та інші проблеми.\n\n"
        "Відгук і повідомлення про помилку\n"
        "надсилаються анонімно @botadmincat"
    )

    # Текст для надсилання помилки
    error_text = (
        "Опишіть вашу проблему/помилку.\n\n"
        "Також ви можете написати\n"
        "в особисті повідомлення\n"
        "до @botadmincat 🙃"
    )

    # Текст для запиту
    request_text = (
        "Ви можете надіслати запит\n"
        "на участь у розробці бота\n\n"
        "Для цього вам потрібно:\n"
        " • Навчатись у ВПК (будь - який курс)\n"
        " • Маєте бути @username\n"
        " • Знати:\n"
        "    обов'язково\n"
        "    - python (рівня джуна)\n"
        "    - aiogram v3х\n"
        "    - SQL запити (aiosqlite)\n"
        "    - Бути зареєстрованим(ою) на GitHub\n"
        "    - Трошки знати git\n"
        "    інші бібліотеки можна довчити згодом\n"
        " • Також можна допомогти з виправленням помилок у тексті.\n"
        "   Для цього знати те, що вище не треба.\n"
        " • Не бути малоросом 😃\n\n"
        'Після натискання "Підтвердити 🫡"\n'
        "ви повинні трошки розказати про себе."
    )

    if type == "main":
        return main_text
    elif type == "error":
        return error_text
    elif type == "request_t":
        return request_text
    elif type == "request_admin":
        # Структура запиту для адміна
        request_text_for_admin = (
            f"запит\n{message.from_user.first_name}\n"
            f"@{message.from_user.username}\n"
            f"{message.from_user.id}"
        )
        return request_text_for_admin


# ======================================================================================


# ======================================================================================
# main message
@router.callback_query(Text(text="Розробка 🧩", ignore_case=True))
async def join_development(query: types.CallbackQuery):
    await query.message.edit_text(await get_text("main"))
    await query.message.edit_reply_markup(reply_markup=await dev_kb())


# ======================================================================================


# ======================================================================================
# back
@router.callback_query(Text(text="back_dev"))
@router.callback_query(Text(text="back_dev"), FSMSDev.text_error)
@router.callback_query(Text(text="back_dev"), FSMSDev.text_response)
@router.callback_query(Text(text="back_dev"), FSMSDev.text_request)
async def join_development_query(query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await query.message.edit_text(await get_text("main"))
    await query.message.edit_reply_markup(reply_markup=await dev_kb())


# ======================================================================================


# ======================================================================================
# error
@router.callback_query(Text(text="error"))
async def error(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_text(await get_text("error"))
    await query.message.edit_reply_markup(reply_markup=await dev_back_kb())
    await state.set_state(FSMSDev.text_error)
    await state.update_data(query=query)


@router.message(F.text, FSMSDev.text_error)
async def error_text(message: types.Message, state: FSMContext):
    data = await state.get_data()
    query: types.CallbackQuery = data["query"]
    await message.delete()
    await state.clear()

    await query.message.edit_text(await get_text("main"))
    await query.message.edit_reply_markup(reply_markup=await dev_kb())
    await bot.send_message(
        chat_id=-1001873448980, message_thread_id=3, text=f"Помилка :\n{message.text}"
    )


# ======================================================================================


# ======================================================================================
# response
@router.callback_query(Text(text="response"))
async def response(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_text("Тепер можете написати відгук 🤝")
    await query.message.edit_reply_markup(reply_markup=await dev_back_kb())
    await state.set_state(FSMSDev.text_response)
    await state.update_data(query=query)


@router.message(F.text, FSMSDev.text_response)
async def response_text(message: types.Message, state: FSMContext):
    data = await state.get_data()
    query: types.CallbackQuery = data["query"]
    await message.delete()
    await state.clear()

    await query.message.edit_text(await get_text("main"))
    await query.message.edit_reply_markup(reply_markup=await dev_kb())
    await bot.send_message(
        chat_id=-1001873448980, message_thread_id=5, text=f"Відгук :\n{message.text}"
    )


# ======================================================================================


# ======================================================================================
# ЗАПИТ НА УЧАСТЬ
@router.callback_query(Text(text="request"))
async def request(query: types.CallbackQuery):
    await query.message.edit_text(await get_text("request_t"))
    await query.message.edit_reply_markup(reply_markup=await dev_choise_kb())


@router.callback_query(Text(text="okay"))
async def confirm_request(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_text("Тепер напишіть трішки про себе 🥳")
    await query.message.edit_reply_markup(reply_markup=await dev_back_kb())
    await state.set_state(FSMSDev.text_request)
    await state.update_data(query=query)


@router.message(F.text, FSMSDev.text_request)
async def send_request(message: types.Message, state: FSMContext):
    data = await state.get_data()
    query: types.CallbackQuery = data["query"]
    await message.delete()
    await state.clear()

    await bot.send_message(
        chat_id=-1001873448980,
        message_thread_id=8,
        text=f"{await get_text('request_admin', message)}\n{message.text}",
    )
    await query.message.edit_text(await get_text("main"))
    await query.message.edit_reply_markup(reply_markup=await dev_kb())
