from aiosqlite import Cursor, Row


async def exist(exist_cur: Cursor) -> bool:
    exists: Row = await exist_cur.fetchone()
    if not exists:
        return False

    return bool(exists[0])
