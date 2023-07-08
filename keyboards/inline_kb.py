from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from data_base import Database
from aiogram import types


# ======================================================================
async def update_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text="Оновити ♻️", callback_data="update"))

    return builder.as_markup()


# ======================================================================
# ======================================================================
async def inline_kb_student_group():
    db = await Database.setup()
    group_list = await db.student_group_list_sql()
    builder = InlineKeyboardBuilder()

    for group in group_list:
        builder.add(InlineKeyboardButton(text=group, callback_data=group))

    builder.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="Назад")).adjust(4)

    return builder.adjust(4).as_markup()


# ======================================================================
# ======================================================================
async def inline_kb_teacher_group():
    db = await Database.setup()
    group_list = await db.teacher_group_list_sql()
    builder = InlineKeyboardBuilder()

    for group in group_list:
        builder.add(InlineKeyboardButton(text=group, callback_data=group))

    builder.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="Назад")).adjust(4)

    return builder.adjust(2).as_markup()


# ======================================================================
# ======================================================================
async def back_inline_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="back_dev"))

    return builder.as_markup()


# ======================================================================
# ======================================================================
async def other_inline_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(text="⬅️ Вибрати іншу групу", callback_data="інша")
    )

    return builder.as_markup()


# ======================================================================
# ======================================================================
async def text_inline_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(text="Змінити замітку ✏️", callback_data="edit_text")
    )

    return builder.as_markup()


async def cancle_inline_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text="Відмінити ❌", callback_data="cancel"))

    return builder.as_markup()


# ======================================================================
# ======================================================================
async def url_card_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text="Поповнити монобанку 🖤", url="https://send.monobank.ua/jar/5uzN1NcwYA"
        )
    )

    return builder.as_markup()


# ======================================================================
# ======================================================================
async def url_contact_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text="Перевірити на сайті 🌐", url="https://vvpc.com.ua/contacts"
        )
    )

    return builder.as_markup()


# ======================================================================
# ======================================================================
async def url_score_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text="Перевірити актуальність 🌐", url="https://vvpc.com.ua/node/980"
        )
    )

    return builder.as_markup()


# ======================================================================
# ======================================================================
async def url_official_site_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(text="Посилання на сайт 🌐", url="https://vvpc.com.ua/")
    )

    return builder.as_markup()


# ======================================================================
# ======================================================================
async def url_introduction_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text="Вступ ➡️", url="https://vvpc.com.ua/vstup"))

    return builder.as_markup()


# ======================================================================
# ======================================================================
async def url_about_college_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(text="Про коледж 🛡", url="https://vvpc.com.ua/node/948")
    )

    return builder.as_markup()


# ======================================================================
# ======================================================================
async def url_speciality_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text="Спеціальності 🤯",
            url="https://padlet.com/VasylT/padlet-2ppk483bi2mgsg3h",
        )
    )

    return builder.as_markup()


# ======================================================================
# ======================================================================
async def settings_inile_kb(user_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    db = await Database.setup()

    if await db.student_exists_sql(user_id):
        if await db.student_agreed_news_exsists_sql(user_id):
            builder.add(
                InlineKeyboardButton(
                    text="Сповіщати про новини ✅",
                    callback_data="change_news_not_agreed",
                )
            )

        elif not await db.student_agreed_news_exsists_sql(user_id):
            builder.add(
                InlineKeyboardButton(
                    text="Сповіщати про новини 🚫", callback_data="change_news_agreed"
                )
            )
        if await db.student_agreed_alert_exsists_sql(user_id):
            builder.add(
                InlineKeyboardButton(
                    text="Сповіщати про тривоги ✅",
                    callback_data="change_alert_not_agreed",
                )
            )

        elif not await db.student_agreed_alert_exsists_sql(user_id):
            builder.add(
                InlineKeyboardButton(
                    text="Сповіщати про тривоги 🚫", callback_data="change_alert_agreed"
                )
            )

        if await db.student_agreed_write_exsists_sql(user_id):
            builder.add(
                InlineKeyboardButton(
                    text="Повідомлення від груп ✅",
                    callback_data="change_write_not_agreed",
                )
            )

        elif not await db.student_agreed_write_exsists_sql(user_id):
            builder.add(
                InlineKeyboardButton(
                    text="Повідомлення від груп 🚫", callback_data="change_write_agreed"
                )
            )

        builder.add(
            InlineKeyboardButton(
                text="Змінити групу 🔄", callback_data="change_student_group"
            )
        )
        return builder.adjust(1).as_markup()

    if await db.teacher_exists_sql(user_id):
        if await db.teacher_agreed_news_exsists_sql(user_id):
            builder.add(
                InlineKeyboardButton(
                    text="Сповіщати про новини ✅",
                    callback_data="change_news_not_agreed",
                )
            )

        elif not await db.teacher_agreed_news_exsists_sql(user_id):
            builder.add(
                InlineKeyboardButton(
                    text="Сповіщати про новини 🚫", callback_data="change_news_agreed"
                )
            )
        if await db.teacher_agreed_alert_exsists_sql(user_id):
            builder.add(
                InlineKeyboardButton(
                    text="Сповіщати про тривоги ✅",
                    callback_data="change_alert_not_agreed",
                )
            )

        elif not await db.teacher_agreed_alert_exsists_sql(user_id):
            builder.add(
                InlineKeyboardButton(
                    text="Сповіщати про тривоги 🚫", callback_data="change_alert_agreed"
                )
            )

        if await db.teacher_agreed_write_exsists_sql(user_id):
            builder.add(
                InlineKeyboardButton(
                    text="Повідомлення від груп ✅",
                    callback_data="change_write_not_agreed",
                )
            )

        elif not await db.teacher_agreed_write_exsists_sql(user_id):
            builder.add(
                InlineKeyboardButton(
                    text="Повідомлення від груп 🚫", callback_data="change_write_agreed"
                )
            )

        builder.add(
            InlineKeyboardButton(
                text="Змінити групу 🔄", callback_data="change_teacher_group"
            )
        )
        return builder.adjust(1).as_markup()


# ======================================================================
