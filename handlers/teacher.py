import datetime

from aiogram import F, Router, types
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from config import SUPER_ADMIN
from data_base import Database
from keyboards import *
from task.alarm import alert_func


class FSMTeacher(StatesGroup):
    name_gpoup = State()


router = Router()

# ===========================Переглянути розклад============================
@router.callback_query(F.data == "Розклад занять 👀")  # registration router
async def view_coupes_teacher(query: types.CallbackQuery):
    db = await Database.setup()
    if not await db.teacher_exists_sql(query.from_user.id):
        await query.answer("Ви не зареєстровані ❌", show_alert=True)
        return
    
    boolen, photo, date = await db.see_rod_t_sql(query.from_user.id)
        
    if not boolen:
        await query.answer("Розкладу ще немає ☹️", show_alert=True)
        return
    
    await query.message.delete()
    await query.message.answer_photo(photo=photo, caption=date, reply_markup=await user_back_kb())
    
    


# ===========================Переглянути розклад дзвінків============================
@router.callback_query(F.data == "Розклад дзвінків ⌛️")  # registration router
async def view_calls_teacher(query: types.CallbackQuery):
    db = await Database.setup()
    
    check, value, date = await db.see_photo_sql('calls')

    if not check:
        await query.answer("Дзвінки ще немає ☹️", show_alert=True)
        return

    await query.message.delete()
    await query.message.answer_photo(value, date, reply_markup=await user_back_kb())

# ===========================Змінити групу============================   
@router.message(F.text == 'Вийти 🚫')  # registration router
async def delete_user_teacher(message: types.Message):
    db = await Database.setup()
    if not await db.teacher_exists_sql(message.from_user.id):
        await message.answer("❗️Ви не зареєстровані❗️")
        return
    
    if not await db.admin_exists_sql(message.from_user.id):
        await db.delete_teacher_sql(message.from_user.id)
        await message.answer("Тепер ви не викладач ✅", reply_markup=await start_all_kb())
        return
    
    await db.delete_teacher_sql(message.from_user.id)
    await message.answer("Тепер ви не викладач ✅", reply_markup=await start_admin_kb())


# =========================== Дріб ===========================
@router.callback_query(F.data == 'Ч/З тиждень ✒️')  # registration router
async def fraction_teacher(query: types.CallbackQuery):
    delta = datetime.timedelta(hours=2, minutes=0)
    todays = datetime.datetime.now(datetime.timezone.utc) + delta
    days = int(todays.strftime("%d"))
    years = int(todays.strftime("%y"))
    mouth = int(todays.strftime("%m"))
    today = datetime.date(year=years, month=mouth, day=days)
    week_number = today.isocalendar()[1]
    if week_number % 2 == 0:
        await query.answer("Цей тиждень - знаменник 🫡", show_alert=True)
    elif week_number % 2 != 0:
        await query.answer("Цей тиждень - чисельник 🫡", show_alert=True)


# =========================== Тривога ===========================
@router.callback_query(F.data == "Тривоги ☢️")  # registration router
async def alert(query: types.CallbackQuery):
    await query.message.delete()

    all_alerts, check = await alert_func()

    text = (
        f"{all_alerts}\n"
        "<a href='https://alerts.in.ua/'>Дані з сайту</a>"
    )

    await query.message.answer(
        text=text,
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=await reg_back_kb()
    )

#        "Розклад студ. 🧑‍🎓","Розклад викл. 👨‍🏫"
@router.callback_query(F.data == 'Розклад викл. 👨‍🏫')
async def schedule_teacher(query: types.CallbackQuery, state: FSMContext):
    await query.message.delete()
    await query.message.answer("Виберіть групу викладача", reply_markup=await teacher_group_list_kb())
    await state.set_state(FSMTeacher.name_gpoup)



@router.callback_query(FSMTeacher.name_gpoup)
async def schedule_teacher1(query: types.CallbackQuery, state: FSMContext):
    db = await Database.setup()
    await query.message.edit_reply_markup()

    if query.data == 'Назад':
        await query.message.delete()
        await query.message.answer("Ваша клавіатура ⌨️", reply_markup=await schedule_kb(query.from_user.id))
        await state.clear()
        return
    
    
    boolen, photo, date = await db.see_schedule_teacher_sql(query.data)

    if not boolen:
        await query.answer(f"У викладача {query.data} \nнемає розкладу ☹️", show_alert=True)
        await query.message.delete()
        await query.message.answer("Ваша клавіатура ⌨️", reply_markup=await schedule_kb(query.from_user.id))
        await state.clear()
        return

    await query.message.delete()
    await query.message.answer_photo(photo=photo, caption=date, reply_markup=await user_back_kb())
