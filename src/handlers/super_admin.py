from aiogram import F, Router, types
from src.keyboards import *
from src.data_base import Database
from src.utils import is_super_admin, password_for_admin

router = Router()


@router.message(F.text == "password")
async def password(message: types.Message) -> None:
    if not await is_super_admin(message):
        return

    await message.answer(f"PASSWORD : {await password_for_admin()}")


@router.message(F.text == "db")
async def send_file_db(message: types.Message) -> None:
    if not await is_super_admin(message):
        return

    file_path = types.FSInputFile("data/database.db")
    await message.bot.send_document(message.from_user.id, file_path)


@router.callback_query(F.data == "⬅️ Назад")
async def super_admin_back(query: types.CallbackQuery):
    if not await is_super_admin(query):
        return

    text = (
        f"панель керування ботом 🎛\n"
        f"• Розклад - налаштування розкладу\n"
        f"• Групи - налаштуванняя груп\n"
    )

    await query.message.edit_text(text=text, reply_markup=super_admin_kb())


@router.callback_query(F.data == "Розклад 📝")
async def choise_in_panel0(query: types.CallbackQuery):
    if not await is_super_admin(query):
        return

    text = (
        f"панель керування Розкладом 🎛\n"
        f"• Додати/Змінити розклад групі 🗓\n"
        f"• Додати/Змінити розклад дзвінків 🔔\n"
        f"• Видалити розклад групі 🗓\n"
        f"• Видалити розклад дзвінків 🔔\n"
    )

    await query.message.edit_text(text=text, reply_markup=super_admin_schedule())


@router.callback_query(F.data == "Групи 👥")
async def choise_in_panel1(query: types.CallbackQuery):
    if not await is_super_admin(query):
        return

    text = f"панель керування Розкладом 🎛\n" f"• Додати групу\n" f"• Видалити групу\n"

    await query.message.edit_text(text=text, reply_markup=super_admin_group())
