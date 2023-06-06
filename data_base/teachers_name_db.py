from data_base.create_db import BaseDBPart


class TeacherGroupDB(BaseDBPart):
    # Функція перевірки чи є розклад викладача з данним name_teacher у db
    # Повертає True or False
    async def teachers_name_exists_sql(self, name_teacher):
        result = await (
            await self.cur.execute(
                "SELECT COUNT(`id`) FROM `teachers_name` WHERE `name_teacher` = ?",
                (name_teacher,),
            )
        ).fetchall()
        return bool(result[0][0])

    # Отримати список назв всіх груп - використовується для побудови клавіатури
    # Повертає список назв всіх груп - type list
    async def teachers_name_list_sql(self):
        keys = []
        reslt = await self.cur.execute("SELECT `name_teacher` FROM `teachers_name`")
        reslt = await reslt.fetchall()
        for i in reslt:
            keys.append(i[0])
        keys.sort()
        return keys

    # Додає розклад для певного вчителя -> name_teacher
    # Повертає збереження бази данних
    async def add_teachers_name_sql(self, user_id, name_teacher):
        await self.cur.execute(
            "INSERT INTO `teachers_name` (`user_id`,`name_teacher`) VALUES (?,?)",
            (user_id, name_teacher),
        )
        return await self.base.commit()

    # Оновлює розклад для певного вчителя -> name_teacher
    # Повертає збереження бази данних
    async def teacher_photo_update_sql(self, photo, name_teacher, transl):
        await self.cur.execute(
            "UPDATE `teachers_name` SET photos = ?, date = ? WHERE name_teacher = ?",
            (
                photo,
                transl,
                name_teacher,
            ),
        )
        return await self.base.commit()

    # Видаляє розклад для певного вчителя -> name_teacher
    # Повертає збереження бази данних
    async def delete_name_techers_sql(self, name_teacher):
        await self.cur.execute(
            "DELETE FROM teachers_name WHERE name_teacher = ?", (name_teacher,)
        )
        return await self.base.commit()

    async def see_rod_t_sql(self, user_id):
        # ініціали вчителя
        name = await self.cur.execute(
            "SELECT `teacher_name` FROM `teachers` WHERE `user_id` = ?", (user_id,)
        )
        rows_name = await name.fetchall()

        h = rows_name[0][0]

        photo = await self.cur.execute(
            "SELECT photos FROM teachers_name WHERE name_teacher = ?", (h,)
        )
        rows_photo = await photo.fetchall()
        date = await self.cur.execute(
            "SELECT `date` FROM teachers_name WHERE name_teacher = ?", (h,)
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
