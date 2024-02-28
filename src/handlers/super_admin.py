from aiogram import F, Router, types
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from src.keyboards import *
from src.data_base import Database
from src.utils import is_super_admin, password_for_admin, get_current_date, clear_all

router = Router()


class FSMSuperAdminPanel(StatesGroup):
    add_or_change_calls = State()
    add_or_change_schedule_name = State()
    add_or_change_schedule_photo = State()


@router.message(F.text == "password")
async def password(message: types.Message) -> None:
    if not await is_super_admin(message):
        return

    await message.answer(f"PASSWORD : {password_for_admin()}")


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
        f"• Групи - налаштування груп\n"
    )

    await query.message.edit_text(text=text, reply_markup=super_admin_kb())


@router.callback_query(F.data == "Розклад 📝")
async def choice_in_panel0(query: types.CallbackQuery):
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
async def choice_in_panel1(query: types.CallbackQuery):
    if not await is_super_admin(query):
        return

    text = f"Панель керування Групами 🎛\n" f"• Додати групу 👥\n" f"• Видалити групу 👥\n"

    await query.message.edit_text(text=text, reply_markup=super_admin_group())


@router.callback_query(F.data == "Інше 📕")
async def choice_in_panel1(query: types.CallbackQuery):
    if not await is_super_admin(query):
        return

    text = (
        f"Панель керування Іншим 🎛\n"
        f"• Додати фото 🖼 - додайте фото у базу данних з її ім'ям. (calls - розклад дзвінків\n"
    )

    await query.message.edit_text(text=text, reply_markup=super_admin_other())


@router.callback_query(F.data == "Додати/Змінити 🗓")
async def add_or_change_schedule1(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_text(
        "Виберіть групу зі списку ⬇️", reply_markup=await group_selection_student_kb()
    )
    await state.set_state(FSMSuperAdminPanel.add_or_change_schedule_name)


@router.callback_query(FSMSuperAdminPanel.add_or_change_schedule_name)
async def add_or_change_schedule_get_name_group(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_text(
        "Надішліть фото 🖼\nЗ увімкнутим стисненням та назвою групи у описі", reply_markup=None
    )
    await state.set_state(FSMSuperAdminPanel.add_or_change_schedule_photo)
    await state.update_data(name_group=query.data, message=query.message)


@router.message(F.photo, FSMSuperAdminPanel.add_or_change_schedule_photo)
async def add_or_change_schedule2(message: types.Message, state: FSMContext):
    db = await Database.setup()
    date = f"Змінено: {get_current_date()}"
    data = (await state.get_data())["name_group"]

    await message.answer("Фото групи змінено ✅", reply_markup=super_admin_schedule())
    await clear_all(message, state)
    print(data)
    await db.student_group_photo_update(data, message.photo[0].file_id, date)


@router.callback_query(F.data == "Додати/Змінити 🔔")
async def add_or_change_calls1(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_text("Надішліть фото 🖼\nЗ увімкнутим стисненням", reply_markup=None)
    await state.set_state(FSMSuperAdminPanel.add_or_change_calls)
    await state.update_data(message=query.message)


@router.message(F.photo, FSMSuperAdminPanel.add_or_change_calls)
async def add_or_change_calls2(message: types.Message, state: FSMContext):
    db = await Database.setup()
    date = f"Змінено: {get_current_date()}"

    await message.answer("Фото дзвінків змінено ✅", reply_markup=super_admin_schedule())
    await clear_all(message, state)

    if await db.photo_exists("calls"):
        await db.update_photo(name_photo="calls", photo=message.photo[0].file_id, date_photo=date)
        return

    await db.add_photo(name_photo="calls", photo=message.photo[0].file_id, date_photo=date)
