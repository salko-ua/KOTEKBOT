# import
import datetime

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from config import SUPER_ADMIN
from create_bot import bot, translator
from data_base import Database
from handlers.reg import password_for_admin

# from import
from keyboards import *

router = Router()


class FSMSuperAdmin(StatesGroup):
    id_student_delete = State()
    id_teachers_delete = State()
    # TEACHERS MANAGMENT
    teachers_add = State()
    teachers_delete = State()
    # GROP MANAGMENT
    curse_group = State()
    curse_group_delete = State()
    curse_group_photo_delete = State()
    # SCHEDULE STUDENTS
    curse_group_rad = State()
    curse_group_rad_photo = State()
    # SCHEDULE TEACHERS
    teachers_rad = State()
    teachers_rad_photo = State()
    # SCHEDULE CALLS
    id_photo = State()


async def is_super_admin(message: types.Message):
    user_id = message.from_user.id
    if user_id in SUPER_ADMIN:
        return True
    else:
        return False


# ===========================Список груп============================ss


# Клавіаура власника
@router.message(Command("sadmin"))
async def super_admin(message: types.Message):
    if not await is_super_admin(message):
        return

    await message.answer("Клавіатура власника", reply_markup=await super_admin_kb())


# Видалити студента за id
@router.message(F.text == "Видалити студента")
async def super_admin_delete_user(message: types.Message, state: FSMContext):
    if not await is_super_admin(message):
        return

    await message.answer("Введіть ID студента")
    await state.set_state(FSMSuperAdmin.id_student_delete)


@router.message(FSMSuperAdmin.id_student_delete)
async def super_admin_delete_user1(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if not await is_super_admin(message):
        return

    exits = await db.student_exists_sql(message.text)
    if exits:
        await db.delete_student_sql(message.text)
        await message.answer("Студента видаленно")
        await state.clear()
    elif not exits:
        await message.answer("Немає користувача з таким ID")
        await state.clear()


# Видалити викладача за id
@router.message(F.text == "Видалити викладача")
async def super_admin_delete_teach(message: types.Message, state: FSMContext):
    if not await is_super_admin(message):
        return

    await message.answer("Введіть ID викладача")
    await state.set_state(FSMSuperAdmin.id_teachers_delete)


@router.message(FSMSuperAdmin.id_teachers_delete)
async def super_admin_delete_teach1(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if not await is_super_admin(message):
        return

    exits = await db.teacher_exists_sql(message.text)
    if exits:
        await db.delete_teacher_sql(message.text)
        await message.answer("Викладача видаленно")
        await state.clear()
    elif not exits:
        await message.answer("Немає викладача з таким ID")
        await state.clear()


@router.message(F.text == "password")
async def password(message: types.Message):
    if not await is_super_admin(message):
        return

    await message.answer(f"PASSWORD : {await password_for_admin()}")


@router.message(F.text == "db")
async def send_file_db(message: types.Message):
    if not await is_super_admin(message):
        return

    file_path = types.FSInputFile("data/database.db")
    await bot.send_document(message.from_user.id, file_path)


# ===========================Додавання викладача============================
@router.message(F.text == "викладача ❇️")
async def add_teachers(message: types.Message, state: FSMContext):
    if not await is_super_admin(message):
        return

    await state.set_state(FSMSuperAdmin.teachers_add)
    await message.answer(
        "Введіть ініціали Викладача\nПриклад : Назаров А.М",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(FSMSuperAdmin.teachers_add)
async def add_teachers1(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if not await is_super_admin(message):
        return

    if message.text == "Назад":
        await message.answer("Меню", reply_markup=await super_admin_kb())
        await state.clear()
        return

    name = message.text
    if await db.teacher_group_exists_sql(message.text):
        await message.answer("Вчитель вже існує ❌", reply_markup=await super_admin_kb())
        await state.clear()
        return

    if len(name) >= 15:
        await message.answer(
            "Ліміт 15 символів ❌",
            reply_markup=await super_admin_kb(),
        )
        await state.clear()
        return

    await db.add_teacher_group_sql(name)
    await message.answer(
        "Групу для вчителя створено ✅", reply_markup=await super_admin_kb()
    )
    await state.clear()


# ===========================Видалити викладача============================
@router.message(F.text == "викладача 🗑")
async def delete_teachers(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if not await is_super_admin(message):
        return

    await state.set_state(FSMSuperAdmin.teachers_delete)
    await message.answer(
        "Виберіть вчителя ⬇️", reply_markup=await group_selection_teacher_kb()
    )


@router.message(FSMSuperAdmin.teachers_delete)
async def delete_teachers1(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if not await is_super_admin(message):
        return

    if message.text == "Назад":
        await message.answer("Меню", reply_markup=await super_admin_kb())
        await state.clear()
        return

    name = message.text
    if not await db.teacher_group_exists_sql(name):
        await message.answer("Немає викладача  ❌", reply_markup=await super_admin_kb())
        await state.clear()
        return

    if len(name) >= 15:
        await message.answer("Ім'я < 15 букв", reply_markup=await super_admin_kb())
        await state.clear()
        return

    if not await db.teacher_for_group_exists_sql(name):
        await db.delete_name_techers_sql(name)
        await message.answer("Успішно видалено ✅", reply_markup=await super_admin_kb())
        await state.clear()
        return

    await db.delete_name_techers_sql(name)
    await db.delete_teacher_name_sql(name)
    await message.answer("Успішно видалено ✅", reply_markup=await super_admin_kb())
    await state.clear()


# ===========================Додати розклад дзвінків============================
@router.message(F.text == "дзвінків ❇️")
async def add_calls(message: types.Message, state: FSMContext):
    if not await is_super_admin(message):
        return

    await message.answer("Завантажте фото", reply_markup=ReplyKeyboardRemove())
    await state.set_state(FSMSuperAdmin.id_photo)


@router.message(F.photo, FSMSuperAdmin.id_photo)
async def add_calls1(message: types.Message, state: FSMContext):
    db = await Database.setup()
    now = datetime.datetime.now()
    now = now.strftime("%d - %B, %A")
    translation = translator.translate(now)

    if not await is_super_admin(message):
        return

    await db.add_photo_sql(
        "calls", message.photo[0].file_id, "Зміненно: " + translation
    )
    await message.answer(
        "Розклад дзвінків оновлено ✅", reply_markup=await super_admin_kb()
    )
    await state.clear()


# ===========================Видалити розклад дзвінків============================
@router.message(F.text == "дзвінків 🗑")
async def delete_calls(message: types.Message):
    db = await Database.setup()
    check = await db.delete_photo_sql("calls")

    if not await is_super_admin(message):
        return

    if not check:
        await message.answer(
            "Розкладу дзвінків ще немає 🔴", reply_markup=await super_admin_kb()
        )
        return

    await message.answer(
        "Розклад дзвінків видалено 🗑", reply_markup=await super_admin_kb()
    )


# ===========================Видалити групу============================
@router.message(F.text == "групу 🗑")
async def delete_group(message: types.Message, state: FSMContext):
    if not await is_super_admin(message):
        return

    await state.set_state(FSMSuperAdmin.curse_group_delete)
    await message.answer(
        "Виберіть групу ⬇️", reply_markup=await group_selection_student_kb()
    )


@router.message(FSMSuperAdmin.curse_group_delete)
async def delete_group1(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if not await is_super_admin(message):
        return

    if message.text == "Назад":
        await message.answer("Меню", reply_markup=await super_admin_kb())
        await state.clear()
        return

    fullname = message.text
    if not await db.student_exists_sql(fullname):
        await message.answer(
            "Група з такою назвою немає", reply_markup=await super_admin_kb()
        )
        await state.clear()
        return

    if len(fullname) >= 3:
        await message.answer("❌ Ліміт 3 символи ", reply_markup=await super_admin_kb())
        await state.clear()
        return

    if not await db.student_in_group_exists_sql(fullname):
        await db.delete_student_group_sql(fullname)
        await message.answer("Групу видалено ✅", reply_markup=await super_admin_kb())
        await state.clear()
        return

    await db.delete_student_group_sql(fullname)
    await db.delete_student_for_group_sql(fullname)
    await message.answer("Групу видалено ✅", reply_markup=await super_admin_kb())
    await state.clear()


# ===========================Додавання групи============================
@router.message(F.text == "групу ❇️")
async def add_group(message: types.Message, state: FSMContext):
    if not await is_super_admin(message):
        return

    await state.set_state(FSMSuperAdmin.curse_group)
    await message.answer(
        "Введіть назву\nПриклад : 2Ц", reply_markup=ReplyKeyboardRemove()
    )


@router.message(FSMSuperAdmin.curse_group)
async def add_group1(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if not await is_super_admin(message):
        return

    if message.text == "Назад":
        await message.answer("Меню", reply_markup=await super_admin_kb())
        await state.clear()
        return

    name = message.text
    if await db.student_group_exists_sql(name):
        await message.answer(
            "Група з такою назвою вже є", reply_markup=await super_admin_kb()
        )
        await state.clear()
        return

    if len(name) >= 3:
        await message.answer(
            "❌ Ліміт 3 символи",
            reply_markup=await super_admin_kb(),
        )
        await state.clear()
        return

    await db.add_student_group_sql(name)
    await message.answer("Групу створено ✅", reply_markup=await super_admin_kb())
    await state.clear()


# ===========================Додати розклад студентам============================
@router.message(F.text == "групі ❇️")
async def add_schedule_to_group(message: types.Message, state: FSMContext):
    if not await is_super_admin(message):
        return

    await state.set_state(FSMSuperAdmin.curse_group_rad_photo)
    await message.answer("Киньте фото розкладу", reply_markup=ReplyKeyboardRemove())


@router.message(F.photo, FSMSuperAdmin.curse_group_rad_photo)
async def add_schedule_to_group1(message: types.Message, state: FSMContext):
    if not await is_super_admin(message):
        return

    await state.update_data(curse_group_rad_photo=message.photo[0].file_id)
    await state.set_state(FSMSuperAdmin.curse_group_rad)
    await message.answer(
        "До якої групи привязати", reply_markup=await group_selection_student_kb()
    )


@router.message(FSMSuperAdmin.curse_group_rad)
async def add_schedule_to_group2(message: types.Message, state: FSMContext):
    db = await Database.setup()
    data = await state.get_data()
    now = datetime.datetime.now()
    now = now.strftime("%d - %B, %A")
    translation = translator.translate(now)

    if not await is_super_admin(message):
        return

    if message.text == "Назад":
        await message.answer("Клавіатура", reply_markup=await super_admin_kb())
        await state.clear()
        return

    if not await db.student_group_exists_sql(message.text):
        await message.answer("Немає такої групи ❌", reply_markup=await super_admin_kb())
        await state.clear()
        return

    await db.student_group_photo_update_sql(
        data["curse_group_rad_photo"],
        message.text,
        "Зміненно: " + translation,
    )
    await message.answer(
        "Розклад успішно додано ✅", reply_markup=await super_admin_kb()
    )
    await state.clear()


# ===========================Додати розклад викладачу============================
@router.message(F.text == "викладачу ❇️")
async def add_schedule_to_teacher(message: types.Message, state: FSMContext):
    if not await is_super_admin(message):
        return

    await state.set_state(FSMSuperAdmin.teachers_rad_photo)
    await message.answer("Киньте фото розкладу", reply_markup=ReplyKeyboardRemove())


@router.message(F.photo, FSMSuperAdmin.teachers_rad_photo)
async def add_schedule_to_teacher1(message: types.Message, state: FSMContext):
    if not await is_super_admin(message):
        return

    await state.update_data(teachers_rad_photo=message.photo[0].file_id)
    await state.set_state(FSMSuperAdmin.teachers_rad)
    await message.answer(
        "До якої групи привязати", reply_markup=await group_selection_teacher_kb()
    )


@router.message(FSMSuperAdmin.teachers_rad)
async def add_schedule_to_teacher2(message: types.Message, state: FSMContext):
    db = await Database.setup()
    data = await state.get_data()
    now = datetime.datetime.now().strftime("%d - %B, %A")
    translation = translator.translate(now)

    if not await is_super_admin(message):
        return

    if message.text == "Назад":
        await message.answer("Клавіатура", reply_markup=await super_admin_kb())
        await state.clear()
        return

    if not await db.teacher_group_exists_sql(message.text):
        await message.answer("Немає такої групи ❌", reply_markup=await super_admin_kb())
        await state.clear()
        return

    await db.teacher_group_photo_update_sql(
        data["teachers_rad_photo"], message.text, "Зміненно: " + translation
    )
    await message.answer(
        "Розклад успішно додано ✅", reply_markup=await super_admin_kb()
    )
    await state.clear()


@router.message(F.text == "групу 🗑🖼")
async def delete_photo_group(message: types.Message, state: FSMContext):
    if not await is_super_admin(message):
        return

    await state.set_state(FSMSuperAdmin.curse_group_photo_delete)
    await message.answer(
        "Виберіть групу ⬇️", reply_markup=await group_selection_student_kb()
    )


@router.message(FSMSuperAdmin.curse_group_photo_delete)
async def delete_photo_group1(message: types.Message, state: FSMContext):
    db = await Database.setup()
    if not await is_super_admin(message):
        return

    if message.text == "Назад":
        await message.answer("Меню", reply_markup=await super_admin_kb())
        await state.clear()
        return

    if not await db.student_group_exists_sql(message.text):
        await message.answer(
            "Групи з такою назвою немає", reply_markup=await super_admin_kb()
        )
        await state.clear()
        return

    await db.delete_student_group_photo_sql(message.text)
    await message.answer(
        "Розклад групі успішно видалено", reply_markup=await super_admin_kb()
    )
