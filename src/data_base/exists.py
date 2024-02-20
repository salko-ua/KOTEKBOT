import asyncache
import cachetools

from src.data_base.create_db import BaseDBPart
from src.data_base.middleprocess import get_number


class ExistDB(BaseDBPart):
    @asyncache.cached(cachetools.TTLCache(1, 2))
    async def admin_exists(self, user_id: int):
        exists = await self.cur.execute(
            "SELECT COUNT(`user_id`) FROM `admin` WHERE `user_id` = ?", (user_id,)
        )
        return await get_number(exists)

    async def student_exists(self, user_id):
        exists = await self.cur.execute(
            "SELECT COUNT(`user_id`) FROM `student` WHERE `user_id` = ?", (user_id,)
        )
        return await get_number(exists)

    async def photo_exists(self, name_photo):
        exists = await self.cur.execute(
            "SELECT COUNT(`id`) FROM `photo` WHERE `name_photo` = ?", (name_photo,)
        )
        return await get_number(exists)

    async def student_in_group_exists(self, group_student):
        exists = await self.cur.execute(
            "SELECT COUNT(`user_id`) FROM `student` WHERE `group_student` = ?",
            (group_student,),
        )
        return await get_number(exists)

    async def student_group_exists(self, name_group):
        exists = await self.cur.execute(
            "SELECT COUNT(`id`) FROM `student_group` WHERE `name_group` = ?",
            (name_group,),
        )
        return await get_number(exists)

    async def user_exists(self, user_id):
        exists = await self.cur.execute(
            "SELECT COUNT(`user_id`) FROM `user` WHERE `user_id` = ?", (user_id,)
        )
        return await get_number(exists)

    async def student_agreed_news_exsists(self, user_id):
        exists = await self.cur.execute(
            "SELECT `send_news` FROM `student` WHERE user_id = ?", (user_id,)
        )
        return await get_number(exists)

    async def student_agreed_alert_exsists(self, user_id):
        exists = await self.cur.execute(
            "SELECT `send_alert` FROM `student` WHERE user_id = ?", (user_id,)
        )
        return await get_number(exists)
