from data_base.create_db import BaseDBPart
import asyncache
import cachetools

class ADMINDB(BaseDBPart):
    # Функція перевірки чи є адмін з данним user_id у db
    # Повертає True or False
    @asyncache.cached(cachetools.TTLCache(1, 60))
    async def admin_exists_sql(self, user_id: int):
        result = await self.cur.execute(
            "SELECT COUNT(`id`) FROM `admin` WHERE `user_id` = ?", (user_id,)
        )
        result = await result.fetchall()
        return bool(result[0][0])

    # Додає адміна до бази даних
    # Повертає збереження бази данних
    async def add_admin_sql(self, user_id, Name, Nickname):
        await self.cur.execute(
            "INSERT INTO `admin` (`user_id`, `Name`, `Nickname`) VALUES (?,?,?)",
            (user_id, Name, Nickname),
        )
        return await self.base.commit()

    # Видаляє адміна за його user_id
    # Повертає збереження бази данних
    async def delete_admins_sql(self, user_id):
        await self.cur.execute("DELETE FROM admin WHERE user_id = ?", (user_id,))
        return await self.base.commit()

    # Перегляд таблиці admin в бд
    # Повертає True or false and str or None , str = адмінів присутніх у бд
    async def admin_all_sql(self):
        keys = []
        keys.clear()
        result = await self.cur.execute("SELECT * FROM `admin`")
        list_r = await result.fetchall()
        if len(list_r) == 0:
            return True, None
        elif len(list_r) > 0:
            for i in list_r:
                keys.append(i)
            reslt = ""
            for i in range(0, len(keys)):
                reslt += f"{i + 1}|{keys[i][1]}|[{keys[i][2]}-{keys[i][3]}]|\n"
            keys = reslt
            return False, keys
