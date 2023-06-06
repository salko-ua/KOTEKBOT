from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data_base import Database


# ======================================================================
update = InlineKeyboardButton("Оновити ♻️", callback_data="update")

update_kb = InlineKeyboardMarkup(row_width=1).add(update)
# ======================================================================


# ======================================================================
async def inline_kb_group():
    db = await Database.setup()
    h = await db.group_list_sql()
    kb_course = InlineKeyboardMarkup(row_width=4)
    for i in range(0, len(h)):
        kb_course.insert(InlineKeyboardButton(h[i], callback_data=h[i]))
    return kb_course.add(InlineKeyboardButton("⬅️ Назад", callback_data="Назад"))


# ======================================================================


# ======================================================================
back = InlineKeyboardButton("⬅️ Вибрати іншу групу", callback_data="інша")

inline_back = InlineKeyboardMarkup(row_width=1).add(back)
# ======================================================================


# ======================================================================
text_inline = InlineKeyboardButton("Змінити замітку ✏️", callback_data="edit_text")
text_inline_kb = InlineKeyboardMarkup(row_width=1).add(text_inline)

cancle_inline = InlineKeyboardButton("Відмінити ❌", callback_data="cancel")
cancle_inline_kb = InlineKeyboardMarkup(row_width=1).add(cancle_inline)
# ======================================================================


# ======================================================================
url_card = InlineKeyboardButton("Поповнити монобанку 🖤", url="https://send.monobank.ua/jar/5uzN1NcwYA")
url_card_kb = InlineKeyboardMarkup(row_width=1).add(url_card)
# ======================================================================

# ======================================================================
site_contacts = InlineKeyboardButton("Перевірити на сайті 🌐", url="https://vvpc.com.ua/contacts")
site_contacts_url = InlineKeyboardMarkup(row_width=1).add(site_contacts)
# ======================================================================