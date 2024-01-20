from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from src.config import SUPER_ADMIN
from src.handlers.reg import password_for_admin
from src.keyboards import *
from src.utils import get_current_date
from src.data_base import Database

router = Router()


class FSMSuperAdmin(StatesGroup):
    id_student_delete = State()
    # GROP MANAGMENT
    curse_group = State()
    curse_group_delete = State()
    curse_group_photo_delete = State()
    # SCHEDULE STUDENTS
    curse_group_rad = State()
    curse_group_rad_photo = State()
    # SCHEDULE CALLS
    id_photo = State()


async def is_super_admin(message: types.Message) -> bool:
    user_id = message.from_user.id
    if user_id in SUPER_ADMIN:
        return True
    else:
        return False


# ===========================Список груп============================ss


# Клавіаура власника
@router.message(Command("sadmin"))
async def super_admin(message: types.Message) -> None:
    if not await is_super_admin(message):
        return

    await message.answer("Клавіатура власника", reply_markup=super_admin_kb())


# Видалити студента за id
@router.message(F.text == "Видалити студента")
async def super_admin_delete_user(message: types.Message, state: FSMContext) -> None:
    if not await is_super_admin(message):
        return

    await message.answer("Введіть ID студента")
    await state.set_state(FSMSuperAdmin.id_student_delete)


@router.message(FSMSuperAdmin.id_student_delete)
async def super_admin_delete_user1(message: types.Message, state: FSMContext) -> None:
    db = await Database.setup()
    if not await is_super_admin(message):
        return

    exits = await db.student_exists(message.text)
    if exits:
        await db.delete_student(message.text)
        await message.answer("Студента видаленно")
        await state.clear()
    elif not exits:
        await message.answer("Немає користувача з таким ID")
        await state.clear()


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


# ===========================Додати розклад дзвінків============================
@router.message(F.text == "дзвінків ❇️")
async def add_calls(message: types.Message, state: FSMContext) -> None:
    if not await is_super_admin(message):
        return

    await message.answer("Завантажте фото", reply_markup=ReplyKeyboardRemove())
    await state.set_state(FSMSuperAdmin.id_photo)


@router.message(F.photo, FSMSuperAdmin.id_photo)
async def add_calls1(message: types.Message, state: FSMContext) -> None:
    db = await Database.setup()
    translation = await get_current_date()

    if not await is_super_admin(message):
        return

    await db.add_photo("calls", message.photo[0].file_id, "Зміненно: " + translation)
    await message.answer("Розклад дзвінків оновлено ✅", reply_markup=super_admin_kb())
    await state.clear()


# ===========================Видалити розклад дзвінків============================
@router.message(F.text == "дзвінків 🗑")
async def delete_calls(message: types.Message) -> None:
    db = await Database.setup()
    check = await db.delete_photo("calls")

    if not await is_super_admin(message):
        return

    if not check:
        await message.answer("Розкладу дзвінків ще немає 🔴", reply_markup=super_admin_kb())
        return

    await message.answer("Розклад дзвінків видалено 🗑", reply_markup=super_admin_kb())


# ===========================Видалити групу============================
@router.message(F.text == "групу 🗑")
async def delete_group(message: types.Message, state: FSMContext) -> None:
    if not await is_super_admin(message):
        return

    await state.set_state(FSMSuperAdmin.curse_group_delete)
    await message.answer("Виберіть групу ⬇️", reply_markup=await group_selection_student_kb())


@router.message(FSMSuperAdmin.curse_group_delete)
async def delete_group1(message: types.Message, state: FSMContext) -> None:
    db = await Database.setup()
    if not await is_super_admin(message):
        return

    if message.text == "Назад":
        await message.answer("Меню", reply_markup=super_admin_kb())
        await state.clear()
        return

    fullname = message.text
    if not await db.student_group_exists(fullname):
        await message.answer("Група з такою назвою немає", reply_markup=super_admin_kb())
        await state.clear()
        return

    if len(fullname) >= 3:
        await message.answer("❌ Ліміт 3 символи ", reply_markup=super_admin_kb())
        await state.clear()
        return

    if not await db.student_in_group_exists(fullname):
        await db.delete_student_group(fullname)
        await message.answer("Групу видалено ✅", reply_markup=super_admin_kb())
        await state.clear()
        return

    await db.delete_student_group(fullname)
    await db.delete_student_for_group(fullname)
    await message.answer("Групу видалено ✅", reply_markup=super_admin_kb())
    await state.clear()


# ===========================Додавання групи============================
@router.message(F.text == "групу ❇️")
async def add_group(message: types.Message, state: FSMContext) -> None:
    if not await is_super_admin(message):
        return

    await state.set_state(FSMSuperAdmin.curse_group)
    await message.answer("Введіть назву\nПриклад : 2Ц", reply_markup=ReplyKeyboardRemove())


@router.message(FSMSuperAdmin.curse_group)
async def add_group1(message: types.Message, state: FSMContext) -> None:
    db = await Database.setup()
    if not await is_super_admin(message):
        return

    if message.text == "Назад":
        await message.answer("Меню", reply_markup=super_admin_kb())
        await state.clear()
        return

    name = message.text
    if await db.student_group_exists(name):
        await message.answer("Група з такою назвою вже є", reply_markup=super_admin_kb())
        await state.clear()
        return

    if len(name) >= 3:
        await message.answer("❌ Ліміт 3 символи", reply_markup=super_admin_kb())
        await state.clear()
        return

    await db.add_student_group(name)
    await message.answer("Групу створено ✅", reply_markup=super_admin_kb())
    await state.clear()


# ===========================Додати розклад студентам============================
@router.message(F.text == "групі ❇️")
async def add_schedule_to_group(message: types.Message, state: FSMContext) -> None:
    if not await is_super_admin(message):
        return

    await state.set_state(FSMSuperAdmin.curse_group_rad_photo)
    await message.answer("Киньте фото розкладу", reply_markup=ReplyKeyboardRemove())


@router.message(F.photo, FSMSuperAdmin.curse_group_rad_photo)
async def add_schedule_to_group1(message: types.Message, state: FSMContext) -> None:
    if not await is_super_admin(message):
        return

    await state.update_data(curse_group_rad_photo=message.photo[0].file_id)
    await state.set_state(FSMSuperAdmin.curse_group_rad)
    await message.answer("До якої групи привязати", reply_markup=await group_selection_student_kb())


@router.message(FSMSuperAdmin.curse_group_rad)
async def add_schedule_to_group2(message: types.Message, state: FSMContext) -> None:
    db = await Database.setup()
    data = await state.get_data()
    translation = await get_current_date()

    if not await is_super_admin(message):
        return

    if message.text == "Назад":
        await message.answer("Клавіатура", reply_markup=super_admin_kb())
        await state.clear()
        return

    if not await db.student_group_exists(message.text):
        await message.answer("Немає такої групи ❌", reply_markup=super_admin_kb())
        await state.clear()
        return

    await db.student_group_photo_update(
        data["curse_group_rad_photo"], message.text, "Зміненно: " + translation
    )
    await message.answer("Розклад успішно додано ✅", reply_markup=super_admin_kb())
    await state.clear()


@router.message(F.text == "групу 🗑🖼")
async def delete_photo_group(message: types.Message, state: FSMContext) -> None:
    if not await is_super_admin(message):
        return

    await state.set_state(FSMSuperAdmin.curse_group_photo_delete)
    await message.answer("Виберіть групу ⬇️", reply_markup=await group_selection_student_kb())


@router.message(FSMSuperAdmin.curse_group_photo_delete)
async def delete_photo_group1(message: types.Message, state: FSMContext) -> None:
    db = await Database.setup()
    if not await is_super_admin(message):
        return

    if message.text == "Назад":
        await message.answer("Меню", reply_markup=super_admin_kb())
        await state.clear()
        return

    if not await db.student_group_exists(message.text):
        await message.answer("Групи з такою назвою немає", reply_markup=super_admin_kb())
        await state.clear()
        return

    await db.delete_student_group_photo(message.text)
    await message.answer("Розклад групі успішно видалено", reply_markup=super_admin_kb())
