from data_base.create_db import BaseDBPart


class TEACHERDB(BaseDBPart):
    # Функція перевірки чи є викладач з данним user_id у db
    # Повертає True or False
    async def teachers_exists_sql(self, user_id):
        result = await self.cur.execute(
            "SELECT COUNT(`id`) FROM `teachers` WHERE `user_id` = ?", (user_id,)
        )
        result = await result.fetchall()
        return bool(result[0][0])

    # Перевірка чи є у групі викладачі якщо немає False якщо є 1 або більше True
    # Повертає True or False
    async def teacher_name_exists_sql(self, group):
        result = await self.cur.execute(
            "SELECT COUNT(`id`) FROM `teachers` WHERE `teacher_name` = ?", (group,)
        )
        result = await result.fetchall()
        return bool(result[0][0])

    # Додає викладача до бази даних
    # Повертає збереження бази данних
    async def add_teachers_sql(self, user_id, Name, Nickname, teachers_name):
        await self.cur.execute(
            "INSERT INTO `teachers` (`user_id`, `Name`, `Nickname`, `teacher_name`) VALUES (?,?,?,?)",
            (user_id, Name, Nickname, teachers_name),
        )
        return await self.base.commit()

    # Видалити викладача за його user_id
    # Повертає збереження бази данних
    async def delete_teach_for_id_sql(self, user_id):
        await self.cur.execute("DELETE FROM teachers WHERE user_id = ?", (user_id,))
        return await self.base.commit()

    # Видалити викладача за його user_id
    # Повертає збереження бази данних
    async def delete_teachers_sql(self, user_id):
        await self.cur.execute("DELETE FROM teachers WHERE user_id = ?", (user_id,))
        return await self.base.commit()

    # Видалити викладача за його group
    # Повертає збереження бази данних
    async def delete_teachers_name_sql(self, group):
        await self.cur.execute("DELETE FROM teachers WHERE teacher_name = ?", (group,))
        return await self.base.commit()

    # Переглянути ім'я групи викладача за user_id
    # Повертає назву групи str
    async def see_group_for_teach_id(self, user_id):
        groups = await self.cur.execute(
            "SELECT `teacher_name` FROM `teachers` WHERE `user_id` = ?", (user_id,)
        )
        result = await groups.fetchall()
        return result[0][0]

    # видає список таблиці викладачів за user_id
    # Повертає True or false and list or None
    async def teach_for_id_sql(self, user_id):
        teachers = await (
            await self.cur.execute(
                "SELECT * FROM teachers WHERE user_id = ?", (user_id,)
            )
        ).fetchall()
        if len(teachers) == 0:
            return True, None
        elif len(teachers) > 0:
            return False, teachers

    # Переглянути число всіх користувачів
    # Повертає число користувачів int
    async def count_teacher_sql(self):
        counts = await self.cur.execute("SELECT `id` FROM teachers")
        row_counts = await counts.fetchall()
        if len(row_counts) == 0:
            return 0
        else:
            return len(row_counts)
        
    # Переглянути всіх користувачів
    # Повертає user_id всіх користувачів list
    async def all_teach_id_for_group_sql(self, group):
        rest = await self.cur.execute(
            "SELECT `user_id` FROM `teachers` WHERE teacher_name = ?", (group,)
        )
        return await rest.fetchall()

    # Переглянути групу користувача за його user_id              Треба покращити
    # Повертає назву групи str
    async def group_for_teach_id(self, user_id):
        groups = await self.cur.execute(
            "SELECT `teacher_name` FROM `teachers` WHERE `user_id` = ?", (user_id,)
        )
        result = await groups.fetchall()
        return result[0][0]

    # Перегляд таблиці teachers за групою в бд
    # Повертає True or false and str or None , str = викладачів присутніх у бд за певною групою
    async def teach_all_sql(self):
        keys = []
        keys.clear()
        result = await self.cur.execute("SELECT * FROM `teachers`")
        list_r = await result.fetchall()
        if len(list_r) == 0:
            return True, None
        elif len(list_r) > 0:
            for i in list_r:
                keys.append(i)
            reslt = ""
            for i in range(0, len(keys)):
                reslt += f"{i + 1}|{keys[i][1]}|[{keys[i][2]}]|{keys[i][4]}|\n"
            keys = reslt
            return False, keys
