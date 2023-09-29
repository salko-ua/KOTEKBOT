from data_base.create_db import BaseDBPart


class StudentDB(BaseDBPart):
    # Функція перевірки чи є користувач з данним user_id у db
    # Повертає True or False
    async def student_exists_sql(self, user_id):
        result = await (
            await self.cur.execute(
                "SELECT COUNT(`user_id`) FROM `student` WHERE `user_id` = ?", (user_id,)
            )
        ).fetchall()
        return bool(result[0][0])

    # Перевірка чи є у групі користувачі якщо немає False якщо є 1 або більше True
    # Повертає True or False
    async def student_in_group_exists_sql(self, text):
        result = await self.cur.execute(
            "SELECT COUNT(`user_id`) FROM `student` WHERE `group_student` = ?", (text,)
        )
        result = await result.fetchall()
        return bool(result[0][0])

    # Переглянути групу користувача за його user_id
    # Повертає назву групи str
    async def group_for_student_id_sql(self, user_id):
        groups = await self.cur.execute(
            "SELECT `group_student` FROM `student` WHERE `user_id` = ?", (user_id,)
        )
        result = await groups.fetchall()
        return result[0][0]

    # Переглянути число всіх користувачів
    # Повертає число користувачів int
    async def count_student_sql(self):
        counts = await self.cur.execute("SELECT `user_id` FROM student")
        return len(await counts.fetchall())

    # Додає користувача до бази даних
    # Повертає збереження бази данних
    async def add_student_sql(self, user_id, group_student):
        await self.cur.execute(
            "INSERT INTO `student` (`user_id`, `group_student`) VALUES (?,?)",
            (user_id, group_student),
        )
        return await self.base.commit()

    # Додає користувача до бази даних
    # Повертає збереження бази данних
    async def update_student_sql(self, user_id, group_student):
        await self.cur.execute(
            "UPDATE `student` SET `group_student` = ? WHERE user_id = ?",
            (group_student, user_id,),
        )
        return await self.base.commit()

    # Видаляє користувача з бд за його user_id
    # Повертає збереження бази данних
    async def delete_student_sql(self, user_id):
        await self.cur.execute("DELETE FROM student WHERE user_id = ?", (user_id,))
        return await self.base.commit()

    # Видаляє всіх користувачів з групи (group)
    # Повертає збереження бази данних
    async def delete_student_for_group_sql(self, group):
        await self.cur.execute("DELETE FROM student WHERE group_student = ?", (group,))
        return await self.base.commit()

    # Зміна дозволів студента
    async def student_change_news_sql(self, boolean: bool, user_id: int):
        await self.cur.execute(
            "UPDATE `student` SET `send_news` = ? WHERE user_id = ?",
            (
                boolean,
                user_id,
            ),
        )
        return await self.base.commit()

    async def student_change_write_sql(self, boolean: bool, user_id: int):
        await self.cur.execute(
            "UPDATE `student` SET `send_write` = ? WHERE user_id = ?",
            (
                boolean,
                user_id,
            ),
        )
        return await self.base.commit()

    async def student_change_alert_sql(self, boolean: bool, user_id: int):
        await self.cur.execute(
            "UPDATE `student` SET `send_alert` = ? WHERE user_id = ?",
            (
                boolean,
                user_id,
            ),
        )
        return await self.base.commit()

    # Перевірка дозвілів студента
    async def student_agreed_write_exsists_sql(self, user_id):
        result = await self.cur.execute(
            "SELECT `send_write` FROM `student` WHERE user_id = ?", (user_id,)
        )
        result = await result.fetchall()
        return bool(result[0][0])

    async def student_agreed_news_exsists_sql(self, user_id):
        result = await self.cur.execute(
            "SELECT `send_news` FROM `student` WHERE user_id = ?", (user_id,)
        )
        result = await result.fetchall()
        return bool(result[0][0])

    async def student_agreed_alert_exsists_sql(self, user_id):
        result = await self.cur.execute(
            "SELECT `send_alert` FROM `student` WHERE user_id = ?", (user_id,)
        )
        result = await result.fetchall()
        return bool(result[0][0])

    # Список студентів з позитивним дозволом
    async def list_id_student_agreed_news_sql(self):
        result = await self.cur.execute(
            "SELECT `user_id` FROM `student` WHERE send_news = ?", (1,)
        )
        return await result.fetchall()

    async def list_id_student_agreed_write_sql(self, group_student):
        result = await self.cur.execute(
            "SELECT `user_id` FROM `student` WHERE group_student = ? AND send_write = ?",
            (group_student, 1),
        )
        return await result.fetchall()

    async def list_id_student_agreed_alert_sql(self):
        result = await self.cur.execute(
            "SELECT `user_id` FROM `student` WHERE send_alert = ?",
            (1,),
        )
        return await result.fetchall()
