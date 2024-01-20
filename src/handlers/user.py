import datetime

import asyncache
import cachetools
from aiogram import Router

from src.data_base import Database

router = Router()


@asyncache.cached(cachetools.TTLCache(1, 1))
async def user_update_db(tg_id: int, first_name: str, last_name: str | None, username: str | None):
    db = await Database.setup()
    now = datetime.datetime.now()

    date_join = now.strftime("%d/%m/%Y, %H:%M:%S")
    last_msg = now.strftime("%d/%m/%Y, %H:%M:%S")
    admin = await db.admin_exists(tg_id)

    group = "absent"
    if await db.student_exists(tg_id):
        group = await db.group_for_student_id(tg_id)

    if not await db.user_exists(tg_id):
        await db.add_user(tg_id, first_name, last_name, username, date_join, last_msg, admin, group)
        return

    await db.update_user(tg_id, first_name, last_name, username, last_msg, admin, group)
