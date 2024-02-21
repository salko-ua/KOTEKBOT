from aiosqlite import Cursor, Row


async def get_text(text: Cursor) -> str:
    text: Row = await text.fetchone()

    if not text:
        return ""

    return text[0]


async def get_number(number: Cursor) -> int:
    number: Row = await number.fetchone()
    if not number:
        return 0

    return number[0]


async def get_list(lists: Cursor) -> list:
    lists: Row = await lists.fetchall()
    if not lists:
        return []

    return list(map(lambda e: e[0], lists))
