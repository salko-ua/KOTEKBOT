from aiosqlite import Cursor, Row


async def exist(exist_cur: Cursor) -> bool:
    exists: Row = await exist_cur.fetchone()
    if not exists:
        return False

    return bool(exists[0])


async def get_number(exist_cur: Cursor) -> bool:
    exists: Row = await exist_cur.fetchone()
    if not exists:
        return 0

    return exists[0]
