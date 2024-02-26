from aiogram import F, Router, types
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from src.keyboards import *
from src.data_base import Database
from src.utils import is_super_admin, password_for_admin, get_current_date

router = Router()


class FSMSuperAdminPanel(StatesGroup):
    add_or_change_calls = State()


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
        f"Панель керування ботом 🎛\n"
        f"• Розклад - налаштування розкладу\n"
        f"• Групи - налаштуванняя груп\n"
    )

    await query.message.edit_text(text=text, reply_markup=super_admin_kb())


@router.callback_query(F.data == "Розклад 📝")
async def choise_in_panel0(query: types.CallbackQuery):
    if not await is_super_admin(query):
        return

    text = (
        f"Панель керування Розкладом 🎛\n"
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

    text = f"Панель керування Групами 🎛\n" f"• Додати групу 👥\n" f"• Видалити групу 👥\n"

    await query.message.edit_text(text=text, reply_markup=super_admin_group())


@router.callback_query(F.data == "Інше 📕")
async def choise_in_panel1(query: types.CallbackQuery):
    if not await is_super_admin(query):
        return

    text = (
        f"Панель керування Іншим 🎛\n"
        f"• Додати фото 🖼 - додайте фото у базу данних з її ім'ям. (calls - розклад дзвінків\n"
    )

    await query.message.edit_text(text=text, reply_markup=super_admin_group())


@router.callback_query(F.data == "Додати/Змінити 🔔")
async def add_or_change_calls1(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_text("Надішліть фото 🖼\nЗ увімкнутим стисненням", reply_markup=None)
    await state.set_state(FSMSuperAdminPanel.add_or_change_calls)
    await state.update_data(message=query.message)


@router.message(F.photo, FSMSuperAdminPanel.add_or_change_calls)
async def add_or_change_calls2(message: types.Message, state: FSMContext):
    db = await Database.setup()
    date = f"Зміненно: {await get_current_date()}"
    old_message: types.Message = (await state.get_data())["message"]

    await message.answer("Фото дзвінків зміненно ✅", reply_markup=super_admin_schedule())
    await old_message.delete()
    await message.delete()
    await state.clear()

    if await db.photo_exists("calls"):
        await db.update_photo(name_photo="calls", photo=message.photo[0].file_id, date_photo=date)
        return

    await db.add_photo(name_photo="calls", photo=message.photo[0].file_id, date_photo=date)
