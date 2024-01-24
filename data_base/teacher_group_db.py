from data_base.create_db import BaseDBPart


class TeacherGroupDB(BaseDBPart):
    # Функція перевірки чи є розклад викладача з данним name_group у db
    # Повертає True or False
    async def teacher_group_exists_sql(self, name_group):
        result = await (
            await self.cur.execute(
                "SELECT COUNT(`id`) FROM `teacher_group` WHERE `name_group` = ?",
                (name_group,),
            )
        ).fetchall()
        return bool(result[0][0])

    # Отримати список назв всіх груп - використовується для побудови клавіатури
    # Повертає список назв всіх груп - type list
    async def teacher_group_list_sql(self):
        keys = []
        reslt = await self.cur.execute("SELECT `name_group` FROM `teacher_group`")
        reslt = await reslt.fetchall()
        for i in reslt:
            keys.append(i[0])
        keys.sort()
        return keys

    # Додає групу вчителя -> name_group
    # Повертає збереження бази данних
    async def add_teacher_group_sql(self, name_group):
        await self.cur.execute(
            "INSERT INTO `teacher_group` (`name_group`) VALUES (?)",
            (name_group,),
        )
        return await self.base.commit()

    # Оновлює розклад для певного вчителя -> name_group
    # Повертає збереження бази данних
    async def teacher_group_photo_update_sql(self, photo, name_group, transl):
        await self.cur.execute(
            "UPDATE `teacher_group` SET photo = ?, date = ? WHERE name_group = ?",
            (
                photo,
                transl,
                name_group,
            ),
        )
        return await self.base.commit()

    # Видаляє розклад для певного вчителя -> name_group
    # Повертає збереження бази данних
    async def delete_name_techers_sql(self, name_group):
        await self.cur.execute(
            "UPDATE teacher_group SET photo = NULL, date = NULL WHERE name_group = ?",
            (name_group,),
        )
        return await self.base.commit()

    async def see_rod_t_sql(self, user_id):
        # ініціали вчителя
        name = await self.cur.execute(
            "SELECT `group_teacher` FROM `teacher` WHERE `user_id` = ?", (user_id,)
        )
        rows_name = await name.fetchall()

        h = rows_name[0][0]

        photo = await self.cur.execute(
            "SELECT photo FROM teacher_group WHERE name_group = ?", (h,)
        )
        rows_photo = await photo.fetchall()
        date = await self.cur.execute(
            "SELECT `date` FROM teacher_group WHERE name_group = ?", (h,)
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

    async def see_schedule_teacher_sql(self, name_group):
        photo = await (
            await self.cur.execute(
                "SELECT `photo` FROM teacher_group WHERE name_group = ?", (name_group,)
            )
        ).fetchall()
        date = await (
            await self.cur.execute(
                "SELECT `date` FROM teacher_group WHERE name_group = ?", (name_group,)
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
