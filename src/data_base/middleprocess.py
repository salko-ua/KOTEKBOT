from aiosqlite import Cursor, Row


async def get_text(exist_cur: Cursor) -> bool:
    text: Row = await exist_cur.fetchone()

    if not text:
        return ""

    return text[0]


async def get_number(exist_cur: Cursor) -> bool:
    number: Row = await exist_cur.fetchone()
    if not number:
        return 0

    return number[0]
