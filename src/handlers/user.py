import datetime

import asyncache
import cachetools
from aiogram import F, Router

from src.data_base import Database

router = Router()


@asyncache.cached(cachetools.TTLCache(1, 1))
async def user_update_db(
    user_id: int, first_name: str, last_name: str | None, username: str | None
):
    db = await Database.setup()
    now = datetime.datetime.now()

    date_join = now.strftime("%d/%m/%Y, %H:%M:%S")
    count_message = 1
    last_message = now.strftime("%d/%m/%Y, %H:%M:%S")
    admin = await db.admin_exists(user_id)

    # student group
    student_group = "absent"
    if await db.student_exists(user_id):
        student_group = await db.group_for_student_id(user_id)

    # user exists (update user)
    if not await db.user_exists(user_id):
        await db.add_user(
            user_id,
            first_name,
            last_name,
            username,
            date_join,
            count_message,
            last_message,
            admin,
            student_group,
        )
        return

    await db.update_user(
        user_id,
        first_name,
        last_name,
        username,
        last_message,
        admin,
        student_group,
    )
