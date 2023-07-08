from data_base.create_db import BaseDBPart
import asyncache
import cachetools


class AdminDB(BaseDBPart):
    # Функція перевірки чи є адмін з данним user_id у db
    # Повертає True or False
    @asyncache.cached(cachetools.TTLCache(1, 60))
    async def admin_exists_sql(self, user_id: int):
        result = await self.cur.execute(
            "SELECT COUNT(`user_id`) FROM `admin` WHERE `user_id` = ?", (user_id,)
        )
        result = await result.fetchall()
        return bool(result[0][0])

    # Додає адміна до бази даних
    # Повертає збереження бази данних
    async def add_admin_sql(self, user_id, username):
        await self.cur.execute(
            "INSERT INTO `admin` (`user_id`, `username`) VALUES (?,?)",
            (
                user_id,
                username,
            ),
        )
        return await self.base.commit()

    # Видаляє адміна за його user_id
    # Повертає збереження бази данних
    async def delete_admins_sql(self, user_id):
        await self.cur.execute("DELETE FROM admin WHERE user_id = ?", (user_id,))
        return await self.base.commit()
