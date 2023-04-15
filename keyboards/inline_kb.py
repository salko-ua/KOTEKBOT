from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


kb = InlineKeyboardButton("Далі", callback_data = "1")
kb1 = InlineKeyboardButton("Далі", callback_data = "2")
kb2 = InlineKeyboardButton("Далі", callback_data = "3")

inline_stats_kb_always = InlineKeyboardMarkup(row_width=1).add(kb)
inline_stats_kb_month = InlineKeyboardMarkup(row_width=1).add(kb1)
inline_stats_kb_week = InlineKeyboardMarkup(row_width=1).add(kb2)