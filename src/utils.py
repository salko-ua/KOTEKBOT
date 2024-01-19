from datetime import datetime
from translate import Translator
from aiosqlite import Row, Cursor


async def exist(exist_cur: Cursor) -> bool:
    exists: Row = await exist_cur.fetchone()
    if not exists:
        return False

    return bool(exists[0])


async def get_current_date() -> str:
    translator = Translator(to_lang="uk")
    now = datetime.now()
    now = now.strftime("%d - %B, %A")
    return translator.translate(now)
