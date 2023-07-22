from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from data_base import Database

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

        builder.add(InlineKeyboardButton(text="Сховати ❌", callback_data="Сховати ❌"))

        builder.add(
            InlineKeyboardButton(
                text="Змінити групу 🔄", callback_data="change_student_group"
            )
        )
        return builder.adjust(1,1,1,2).as_markup()

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

        builder.add(InlineKeyboardButton(text="Сховати ❌", callback_data="Сховати ❌"))

        builder.add(
            InlineKeyboardButton(
                text="Змінити групу 🔄", callback_data="change_teacher_group"
            )
        )
        return builder.adjust(1,1,1,2).as_markup()
