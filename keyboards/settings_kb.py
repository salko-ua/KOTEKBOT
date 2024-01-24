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
                    text="Новини 🔔 ✅",
                    callback_data="change_news_not_agreed",
                )
            )

        elif not await db.student_agreed_news_exsists_sql(user_id):
            builder.add(
                InlineKeyboardButton(
                    text="Новини 🔔 🚫", callback_data="change_news_agreed"
                )
            )
        if await db.student_agreed_alert_exsists_sql(user_id):
            builder.add(
                InlineKeyboardButton(
                    text="Тривоги ⚠️ ✅",
                    callback_data="change_alert_not_agreed",
                )
            )

        elif not await db.student_agreed_alert_exsists_sql(user_id):
            builder.add(
                InlineKeyboardButton(
                    text="Тривоги ⚠️ 🚫", callback_data="change_alert_agreed"
                )
            )

        if await db.student_agreed_write_exsists_sql(user_id):
            builder.add(
                InlineKeyboardButton(
                    text="Переписка 📩 ✅",
                    callback_data="change_write_not_agreed",
                )
            )

        elif not await db.student_agreed_write_exsists_sql(user_id):
            builder.add(
                InlineKeyboardButton(
                    text="Переписка 📩 🚫", callback_data="change_write_agreed"
                )
            )

        builder.add(
            InlineKeyboardButton(
                text="Змінити групу 🔄", callback_data="change_student_group"
            )
        )

        builder.add(InlineKeyboardButton(text="Сховати ❌", callback_data="Сховати ❌"))

        builder.add(
            InlineKeyboardButton(text="Бути виклад. 👤", callback_data="change_account")
        )

        return builder.adjust(2).as_markup()

    if await db.teacher_exists_sql(user_id):
        if await db.teacher_agreed_news_exsists_sql(user_id):
            builder.add(
                InlineKeyboardButton(
                    text="Новини 🔔 ✅",
                    callback_data="change_news_not_agreed",
                )
            )

        elif not await db.teacher_agreed_news_exsists_sql(user_id):
            builder.add(
                InlineKeyboardButton(
                    text="Новини 🔔 🚫", callback_data="change_news_agreed"
                )
            )

        if await db.teacher_agreed_alert_exsists_sql(user_id):
            builder.add(
                InlineKeyboardButton(
                    text="Тривоги ⚠️ ✅",
                    callback_data="change_alert_not_agreed",
                )
            )

        elif not await db.teacher_agreed_alert_exsists_sql(user_id):
            builder.add(
                InlineKeyboardButton(
                    text="Тривоги ⚠️ 🚫", callback_data="change_alert_agreed"
                )
            )

        """ if await db.teacher_agreed_write_exsists_sql(user_id):
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
            )"""
        builder.add(
            InlineKeyboardButton(
                text="Змінити групу 🔄", callback_data="change_teacher_group"
            )
        )
        builder.add(
            InlineKeyboardButton(text="Бути студент. 👤", callback_data="change_account")
        )

        builder.add(InlineKeyboardButton(text="Сховати ❌", callback_data="Сховати ❌"))
        return builder.adjust(2, 2, 1).as_markup()
