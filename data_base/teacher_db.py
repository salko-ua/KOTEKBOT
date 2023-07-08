from data_base.create_db import BaseDBPart


class TeacherDB(BaseDBPart):
    # Функція перевірки чи є викладач з данним user_id у db
    # Повертає True or False
    async def teacher_exists_sql(self, user_id):
        result = await self.cur.execute(
            "SELECT COUNT(`user_id`) FROM `teacher` WHERE `user_id` = ?", (user_id,)
        )
        result = await result.fetchall()
        return bool(result[0][0])

    # Перевірка чи є у групі викладачі якщо немає False якщо є 1 або більше True
    # Повертає True or False
    async def teacher_for_group_exists_sql(self, group_teacher):
        result = await self.cur.execute(
            "SELECT COUNT(`user_id`) FROM `teacher` WHERE `group_teacher` = ?",
            (group_teacher,),
        )
        result = await result.fetchall()
        return bool(result[0][0])

    # Додає викладача до бази даних
    # Повертає збереження бази данних
    async def add_teacher_sql(self, user_id, group_teacher):
        await self.cur.execute(
            "INSERT INTO `teacher` (user_id, group_teacher) VALUES (?,?)",
            (
                user_id,
                group_teacher,
            ),
        )
        return await self.base.commit()

    # Видалити викладача за його id (user_id)
    # Повертає збереження бази данних
    async def delete_teacher_sql(self, user_id):
        await self.cur.execute("DELETE FROM teacher WHERE user_id = ?", (user_id,))
        return await self.base.commit()

    # Видалити викладачів за їх групою (group_teacher)
    # Повертає збереження бази данних
    async def delete_teacher_name_sql(self, group_teacher):
        await self.cur.execute(
            "DELETE FROM teacher WHERE group_teacher = ?", (group_teacher,)
        )
        return await self.base.commit()

    # Переглянути ім'я групи викладача за user_id
    # Повертає назву групи str
    async def see_group_for_teach_id(self, user_id):
        groups = await self.cur.execute(
            "SELECT `group_teacher` FROM `teacher` WHERE `user_id` = ?", (user_id,)
        )
        result = await groups.fetchall()
        return result[0][0]

    # Переглянути число всіх користувачів
    # Повертає число користувачів int
    async def count_teacher_sql(self):
        counts = await self.cur.execute("SELECT `user_id` FROM teacher")
        return len(await counts.fetchall())

    # Переглянути групу користувача за його user_id
    # Повертає назву групи str
    async def group_for_teacher_id_sql(self, user_id):
        groups = await self.cur.execute(
            "SELECT `group_teacher` FROM `teacher` WHERE `user_id` = ?", (user_id,)
        )
        result = await groups.fetchall()
        return result[0][0]

    # Додає користувача до бази даних
    # Повертає збереження бази данних
    async def update_teacher_sql(self, group_student):
        await self.cur.execute(
            "UPDATE`teacher` SET `group_teacher` = ?",
            (group_student,),
        )
        return await self.base.commit()

    # Зміна дозволів викладача
    async def teacher_change_news_sql(self, boolean: bool, user_id: int):
        await self.cur.execute(
            "UPDATE `teacher` SET `send_news` = ? WHERE user_id = ?",
            (
                boolean,
                user_id,
            ),
        )
        return await self.base.commit()

    async def teacher_change_write_sql(self, boolean: bool, user_id: int):
        await self.cur.execute(
            "UPDATE `teacher` SET `send_write` = ? WHERE user_id = ?",
            (
                boolean,
                user_id,
            ),
        )
        return await self.base.commit()

    async def teacher_change_alert_sql(self, boolean: bool, user_id: int):
        await self.cur.execute(
            "UPDATE `teacher` SET `send_alert` = ? WHERE user_id = ?",
            (
                boolean,
                user_id,
            ),
        )
        return await self.base.commit()

    # Перевірка дозвілів викладача
    async def teacher_agreed_write_exsists_sql(self, user_id):
        result = await self.cur.execute(
            "SELECT `send_write` FROM `teacher` WHERE user_id = ?", (user_id,)
        )
        result = await result.fetchall()
        return bool(result[0][0])

    async def teacher_agreed_news_exsists_sql(self, user_id):
        result = await self.cur.execute(
            "SELECT `send_news` FROM `teacher` WHERE user_id = ?", (user_id,)
        )
        result = await result.fetchall()
        return bool(result[0][0])

    async def teacher_agreed_alert_exsists_sql(self, user_id):
        result = await self.cur.execute(
            "SELECT `send_alert` FROM `teacher` WHERE user_id = ?", (user_id,)
        )
        result = await result.fetchall()
        return bool(result[0][0])

    # Список студентів з позитивним дозволом
    async def list_id_teacher_agreed_news_sql(self):
        result = await self.cur.execute(
            "SELECT `user_id` FROM `teacher` WHERE send_news = ?", (1,)
        )
        return await result.fetchall()

    async def list_id_teacher_agreed_write_sql(self):
        result = await self.cur.execute(
            "SELECT `user_id` FROM `teacher` WHERE send_write = ?", (1,)
        )
        return await result.fetchall()

    async def list_id_teacher_agreed_alert_sql(self):
        result = await self.cur.execute(
            "SELECT `user_id` FROM `teacher` WHERE send_alert = ?", (1,)
        )
        return await result.fetchall()
