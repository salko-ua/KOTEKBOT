from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.data_base import Database


async def settings_inline_kb(user_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    db = await Database.setup()

    if await db.student_agreed_news_exists(user_id):
        builder.add(
            InlineKeyboardButton(
                text="Новини 🔔 ✅",
                callback_data="change_news_not_agreed",
            )
        )

    elif not await db.student_agreed_news_exists(user_id):
        builder.add(
            InlineKeyboardButton(
                text="Новини 🔔 🚫", callback_data="change_news_agreed"
            )
        )

    if await db.student_agreed_alert_exists(user_id):
        builder.add(
            InlineKeyboardButton(
                text="Тривоги ⚠️ ✅",
                callback_data="change_alert_not_agreed",
            )
        )

    elif not await db.student_agreed_alert_exists(user_id):
        builder.add(
            InlineKeyboardButton(
                text="Тривоги ⚠️ 🚫", callback_data="change_alert_agreed"
            )
        )

    builder.add(
        InlineKeyboardButton(
            text="Тема розкладу 🗒", callback_data="change_schedule_theme"
        )
    )

    builder.add(
        InlineKeyboardButton(
            text="Змінити групу 🔄", callback_data="change_student_group"
        )
    )

    builder.add(InlineKeyboardButton(text="Сховати ❌", callback_data="Сховати ❌"))

    return builder.adjust(2).as_markup()


async def theme_colors(user_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    themes = {
        "black": "Чорний ⚫️",
        "gray": "Сірий ⚪️",
        "red": "Червоний 🔴",
        "orange": "Оранжевий 🟠",
        "purple": "Фіолетовий 🟣",
        "pink": "Розовий 💞",
        "green": "Зелений 🟢",
        "brown": "Коричневий 🟤",
        "blue": "Синій 🔵",
        "yellow": "Жовтий 🟡",
    }
    db = await Database.setup()
    current_theme = await db.get_student_theme(user_id)
    for key, value in themes.items():
        if key == current_theme:
            builder.add(
                InlineKeyboardButton(text=f"{value}✅", callback_data=f"theme {key}✅")
            )
        else:
            builder.add(InlineKeyboardButton(text=value, callback_data=f"theme {key}"))

    builder.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="back_settings_kb"))

    return builder.adjust(2).as_markup()
