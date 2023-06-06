from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# ======================================================================
kb = InlineKeyboardButton("Запит на участь 📝", callback_data="request")
kb1 = InlineKeyboardButton("Надіслати відгук ☺️", callback_data="response")
kb2 = InlineKeyboardButton("Повідомити про помилку 🤔", callback_data="error")

dev_inline_kb = InlineKeyboardMarkup(row_width=1).add(kb).add(kb1).add(kb2)
# ======================================================================


# ======================================================================
back = InlineKeyboardButton("⬅️ Назад", callback_data="back_dev")

dev_back_inline_kb = InlineKeyboardMarkup(row_width=1).add(back)
# ======================================================================


# ======================================================================
backs = InlineKeyboardButton("⬅️ Назад", callback_data="back_dev")
dev = InlineKeyboardButton("Підтвердити 🫡", callback_data="okay")

dev_request_inline_kb = InlineKeyboardMarkup(row_width=1).add(dev, back)
# ======================================================================
