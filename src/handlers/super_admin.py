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
    add_group_name = State()
    add_or_change_any_photo = State()
    delete_group_name = State()


@router.message(F.text.startswith("sql "))
async def sql(message: types.Message) -> None:
    if not await is_super_admin(message):
        return

    db = await Database.setup()
    await db.sql_request(message.text[4:])


@router.message(F.text.startwith("sql "))
async def sql(message: types.Message) -> None:
    if not await is_super_admin(message):
        return

    db = await Database.setup()
    await db.sql_request(message[4:])
    await message.answer("GOOD")


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

    text = (
        f"Панель керування Групами 🎛\n" f"• Додати групу 👥\n" f"• Видалити групу 👥\n"
    )

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
async def add_or_change_schedule_get_name_group(
    query: types.CallbackQuery, state: FSMContext
):
    await query.message.edit_text(
        "Надішліть фото 🖼\nЗ увімкнутим стисненням та назвою групи у описі",
        reply_markup=None,
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

    await db.student_group_photo_update(data, message.photo[0].file_id, date)


@router.callback_query(F.data == "Додати/Змінити 🔔")
async def add_or_change_calls1(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_text(
        "Надішліть фото 🖼\nЗ увімкнутим стисненням", reply_markup=None
    )
    await state.set_state(FSMSuperAdminPanel.add_or_change_calls)
    await state.update_data(message=query.message)


@router.message(F.photo, FSMSuperAdminPanel.add_or_change_calls)
async def add_or_change_calls2(message: types.Message, state: FSMContext):
    db = await Database.setup()
    date = f"Змінено: {get_current_date()}"

    await message.answer(
        "Фото дзвінків змінено ✅", reply_markup=super_admin_schedule()
    )
    await clear_all(message, state)

    if await db.photo_exists("calls"):
        await db.update_photo(
            name_photo="calls", photo=message.photo[0].file_id, date_photo=date
        )
        return

    await db.add_photo(
        name_photo="calls", photo=message.photo[0].file_id, date_photo=date
    )


@router.callback_query(F.data == "Додати фото 🖼")
async def add_photo(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_text(
        "Надішліть фото 🖼\nЗ увімкнутим стисненням", reply_markup=None
    )
    await state.set_state(FSMSuperAdminPanel.add_or_change_any_photo)
    await state.update_data(message=query.message)


@router.message(F.photo, FSMSuperAdminPanel.add_or_change_any_photo)
async def add_photo2(message: types.Message, state: FSMContext):
    await state.update_data(photo=message.photo[0].file_id)
    await message.answer(
        "Надайте назву фото за яким його можна буде змінювати", reply_markup=None
    )
    await state.update_data(message=message)


@router.message(F.text, FSMSuperAdminPanel.add_or_change_any_photo)
async def add_photo3(message: types.Message, state: FSMContext):
    db = await Database.setup()
    date = f"Змінено: {get_current_date()}"
    photo = (await state.get_data())["photo"]
    name_photo = message.text

    await clear_all(message, state)

    await message.answer(
        "Фото додано но бази данних✅", reply_markup=super_admin_other()
    )

    if await db.photo_exists(name_photo):
        await db.update_photo(name_photo=name_photo, photo=photo, date_photo=date)
        return

    await db.add_photo(name_photo=name_photo, photo=photo, date_photo=date)


# Обробник для кнопки "Додати 👥"


@router.callback_query(F.data == "Додати 👥")
async def add_student(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_text("Введіть назву групи ⬇️", reply_markup=None)
    await state.set_state(FSMSuperAdminPanel.add_group_name)


@router.message(F.text, FSMSuperAdminPanel.add_group_name)
async def add_student2(message: types.Message, state: FSMContext):
    db = await Database.setup()
    user_message = message.text

    await db.add_student_group(user_message)

    await message.answer("Група додана ✅", reply_markup=super_admin_back_kb())
    await state.clear()


# Обробник для кнопки "Видалити 👥"
@router.callback_query(F.data == "Видалити 👥")
async def delete_student(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_text(
        "Виберіть групу зі списку нижче ⬇️",
        reply_markup=await group_selection_student_kb(),
    )

    await state.set_state(FSMSuperAdminPanel.delete_group_name)


@router.callback_query(F.data, FSMSuperAdminPanel.delete_group_name)
async def delete_student_group_callback(query: types.CallbackQuery, state: FSMContext):
    db = await Database.setup()
    group_name = query.data
    print(query.data)
    if query.data == "admin_back_kb":
        await query.message.edit_text(f"Сало лох", reply_markup=super_admin_back_kb())
        await state.clear()
        return

    await db.delete_student_group(group_name)

    await query.message.edit_text(
        f"Група {group_name} видалена ✅", reply_markup=super_admin_back_kb()
    )
    await state.clear()
