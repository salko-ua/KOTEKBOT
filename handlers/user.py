import asyncache
import cachetools

from data_base import Database
from aiogram.types import Message
import datetime


@asyncache.cached(cachetools.TTLCache(1, 1))
async def user_update_db(
    user_id: int, first_name: str, last_name: str | None, username: str | None
):
    db = await Database.setup()
    now = datetime.datetime.now()

    date_join = now.strftime("%d/%m/%Y, %H:%M:%S")
    count_message = 1
    last_message = now.strftime("%d/%m/%Y, %H:%M:%S")
    admin = await db.admin_exists_sql(user_id)

    # student group
    if await db.student_exists_sql(user_id):
        student_group = await db.group_for_student_id_sql(user_id)
    elif not await db.student_exists_sql(user_id):
        student_group = "absent"

    # teacher group
    if await db.teacher_exists_sql(user_id):
        teacher_group = await db.see_group_for_teach_id(user_id)
    elif not await db.teacher_exists_sql(user_id):
        teacher_group = "absent"

    # user exists (update user)
    if await db.user_exists_sql(user_id):
        await db.update_user_sql(
            user_id,
            first_name,
            last_name,
            username,
            last_message,
            admin,
            student_group,
            teacher_group,
        )

    # user not exists (add user)
    if not await db.user_exists_sql(user_id):
        await db.add_user_sql(
            user_id,
            first_name,
            last_name,
            username,
            date_join,
            count_message,
            last_message,
            admin,
            student_group,
            teacher_group,
        )
