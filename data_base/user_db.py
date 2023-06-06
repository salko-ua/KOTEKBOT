from data_base.create_db import BaseDBPart


class UserDB(BaseDBPart):
    # Функція перевірки чи є користувач з данним user_id у db
    # Повертає True or False
    async def user_exists_sql(self, user_id):
        result = await (
            await self.cur.execute(
                "SELECT COUNT(`user_id`) FROM `user` WHERE `user_id` = ?", (user_id,)
            )
        ).fetchall()
        return bool(result[0][0])

    # Перевірка чи є у групі користувачі якщо немає False якщо є 1 або більше True
    # Повертає True or False
    async def user_group_exists_sql(self, text):
        result = await self.cur.execute(
            "SELECT COUNT(`user_id`) FROM `user` WHERE `group_user` = ?", (text,)
        )
        result = await result.fetchall()
        return bool(result[0][0])

    # Переглянути групу користувача за його user_id              Треба покращити
    # Повертає назву групи str
    async def group_for_user_id(self, user_id):
        groups = await self.cur.execute(
            "SELECT `group_user` FROM `user` WHERE `user_id` = ?", (user_id,)
        )
        result = await groups.fetchall()
        return result[0][0]

    # Переглянути всіх користувачів
    # Повертає user_id всіх користувачів list
    async def all_user_id_sql(self):
        rest = await self.cur.execute("SELECT `user_id` FROM `user`")
        return await rest.fetchall()

    # Переглянути всіх користувачів за групою
    # Повертає user_id всіх користувачів list
    async def all_user_id_for_group_sql(self, group):
        rest = await self.cur.execute(
            "SELECT `user_id` FROM `user` WHERE group_user = ?", (group,)
        )
        return await rest.fetchall()

    # Переглянути число всіх користувачів
    # Повертає число користувачів int
    async def count_user_sql(self):
        counts = await self.cur.execute("SELECT `user_id` FROM user")
        row_counts = await counts.fetchall()
        if len(row_counts) == 0:
            return 0
        else:
            return len(row_counts)

    # Додає користувача до бази даних
    # Повертає збереження бази данних
    async def add_user_sql(self, user_id, Name, Nickname, groupe):
        await self.cur.execute(
            "INSERT INTO `user` (`user_id`, `Name`, `Nickname`, `group_user`) VALUES (?,?,?,?)",
            (user_id, Name, Nickname, groupe),
        )
        return await self.base.commit()

    # Видаляє користувача з бд за його user_id
    # Повертає збереження бази данних
    async def delete_users_sql(self, user_id):
        await self.cur.execute("DELETE FROM user WHERE user_id = ?", (user_id,))
        return await self.base.commit()

    # Видаляє всіх користувачів з групи (group)
    # Повертає збереження бази данних
    async def delete_user_groups_sql(self, group):
        await self.cur.execute("DELETE FROM user WHERE group_user = ?", (group,))
        return await self.base.commit()

    # Видаляє корустувача за user_id
    # Повертає збереження бази данних
    async def delete_studen_for_id_sql(self, user_id):
        await self.cur.execute("DELETE FROM user WHERE user_id = ?", (user_id,))
        return await self.base.commit()

    # Видаляє всіх користувачів з групи (group)
    # Повертає збереження бази данних
    async def id_from_group_exists_sql(self, groupname):
        result = await self.cur.execute(
            "SELECT `user_id` FROM `user` WHERE `group_user` = ?", (groupname,)
        )
        return await result.fetchall()

    # видає список таблиці користувачів за user_id
    # Повертає True or false and list or None
    async def studen_for_id_sql(self, user_id):
        student = await (
            await self.cur.execute("SELECT * FROM user WHERE user_id = ?", (user_id,))
        ).fetchall()
        if len(student) == 0:
            return True, None
        elif len(student) > 0:
            return False, student

    # Перегляд таблиці user в бд
    # Повертає str відформатований текст списку користувачів присутніх у бд
    async def user_all_sql(self):
        keys = []
        keys.clear()
        result = await self.cur.execute("SELECT * FROM `user`")
        list_r = await result.fetchall()
        if len(list_r) == 0:
            return True, None
        elif len(list_r) > 0:
            for i in list_r:
                keys.append(i)
            reslt = ""
            for i in range(0, len(keys)):
                reslt += f"{i + 1}|{keys[i][0]}|[{keys[i][1]}]|{keys[i][3]}|\n"
            keys = reslt
            return False, keys

    # Перегляд таблиці user за групою в бд
    # Повертає True or false and str or None , str = користувачів присутніх у бд за певною групою
    async def user_for_group_sql(self, groupe):
        keys = []
        keys.clear()
        result = await self.cur.execute(
            "SELECT * FROM `user` WHERE group_user = ?", (groupe,)
        )
        list_r = await result.fetchall()
        if len(list_r) == 0:
            return True, None
        elif len(list_r) > 0:
            for i in list_r:
                keys.append(i)
            reslt = f"Група : {keys[0][3]}\n\n"
            for i in range(0, len(keys)):
                reslt += f"{i + 1}|{keys[i][0]}|[{keys[i][1]}]\n"
            keys = reslt
            return False, keys
