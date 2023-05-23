from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data_base import Database



#======================================================================
kb = InlineKeyboardButton("Далі", callback_data = "1")
kb1 = InlineKeyboardButton("Далі", callback_data = "2")
kb2 = InlineKeyboardButton("Далі", callback_data = "3")

inline_stats_kb_always = InlineKeyboardMarkup(row_width=1).add(kb)
inline_stats_kb_month = InlineKeyboardMarkup(row_width=1).add(kb1)
inline_stats_kb_week = InlineKeyboardMarkup(row_width=1).add(kb2)
#======================================================================


#======================================================================
async def inline_kb_group():
    db = await Database.setup()
    h = await db.group_list_sql()
    kb_course = InlineKeyboardMarkup(row_width=4)
    for i in range(0, len(h)):
        kb_course.insert(InlineKeyboardButton(h[i], callback_data=h[i]))
    return kb_course.add(InlineKeyboardButton("Назад", callback_data="Назад"))
#======================================================================


#======================================================================
back = InlineKeyboardButton("Вибрати іншу групу", callback_data="інша")

inline_back = InlineKeyboardMarkup(row_width=1).add(back)
#======================================================================


#======================================================================
text_inline = InlineKeyboardButton("Змінити замітку", callback_data = "edit_text")
text_inline_kb = InlineKeyboardMarkup(row_width=1).add(text_inline)

cancle_inline = InlineKeyboardButton("Відмінити ❌", callback_data = "cancel")
cancle_inline_kb = InlineKeyboardMarkup(row_width=1).add(cancle_inline)
#======================================================================




