from data_base.create_db import BaseDBPart


class StudentGroupDB(BaseDBPart):
    # Функція перевірки чи є гурпа з данним name_group у db
    # Повертає True or False
    async def student_group_exists_sql(self, name_group):
        result = await self.cur.execute(
            "SELECT COUNT(`id`) FROM `student_group` WHERE `name_group` = ?",
            (name_group,),
        )
        result = await result.fetchall()
        return bool(result[0][0])

    # Отримати список назв всіх груп - використовується для побудови клавіатури
    # Повертає список назв всіх груп - type list
    async def student_group_list_sql(self):
        keys = []
        reslt = await self.cur.execute("SELECT `name_group` FROM `student_group`")
        reslt = await reslt.fetchall()
        for i in reslt:
            keys.append(i[0])
        keys.sort()
        return keys

    # Додає групу -> name_group
    # Повертає збереження бази данних
    async def add_student_group_sql(self, student_group):
        await self.cur.execute(
            "INSERT INTO `student_group` (`name_group`) VALUES (?)",
            (student_group,),
        )
        return await self.base.commit()

    # Видаляє розклад для певної групи -> name_group
    # Повертає збереження бази данних
    async def delete_student_group_photo_sql(self, student_group):
        await self.cur.execute(
            "UPDATE `student_group` SET photo = NULL, date = NULL WHERE name_group = ?",
            (student_group,),
        )
        return await self.base.commit()

    # Оновлює розклад для певної групи -> name_group
    # Повертає збереження бази данних
    async def student_group_photo_update_sql(self, photo, name_group, transl):
        await self.cur.execute(
            "UPDATE `student_group` SET photo = ?, date = ? WHERE name_group = ?",
            (
                photo,
                transl,
                name_group,
            ),
        )
        return await self.base.commit()

    # Видаляє певну групу
    # Повертає збереження бази данних
    async def delete_student_group_sql(self, student_group):
        await self.cur.execute(
            "DELETE FROM student_group WHERE name_group = ?", (student_group,)
        )
        return await self.base.commit()

    async def see_rod_sql(self, user_id):
        # назва групи користувача
        student_groups = await self.cur.execute(
            "SELECT `group_student` FROM `student` WHERE `user_id` = ?", (user_id,)
        )
        rows_student_groups = await student_groups.fetchall()
        h = rows_student_groups[0][0]

        photo = await self.cur.execute(
            "SELECT `photo` FROM student_group WHERE name_group = ?", (h,)
        )
        rows_photo = await photo.fetchall()
        date = await self.cur.execute(
            "SELECT `date` FROM student_group WHERE name_group = ?", (h,)
        )
        rows_date = await date.fetchall()
        try:
            lens = len(rows_photo[0][0])
        except TypeError:
            lens = 1
        if lens <= 5:
            return False, None, None
        elif lens >= 6:
            reslt = rows_photo[0][0]
            datka = rows_date[0][0]
            return True, reslt, datka

    async def see_schedule_student_sql(self, name_group):
        photo = await (
            await self.cur.execute(
                "SELECT `photo` FROM student_group WHERE name_group = ?", (name_group,)
            )
        ).fetchall()
        date = await (
            await self.cur.execute(
                "SELECT `date` FROM student_group WHERE name_group = ?", (name_group,)
            )
        ).fetchall()
        try:
            lens = len(photo[0][0])
        except TypeError:
            lens = 1
        if lens <= 5:
            return False, None, None
        elif lens >= 6:
            reslt = photo[0][0]
            datka = date[0][0]
            return True, reslt, datka
