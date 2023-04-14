from data_base.create_db import BaseDBPart


class GROUPDB(BaseDBPart):
    # Функція перевірки чи є гурпа з данним groupname у db
    # Повертає True or False
    async def group_exists_sql(self, groupname):
        result = await self.cur.execute(
            "SELECT COUNT(`groupname`) FROM `groupa` WHERE `groupname` = ?",
            (groupname,),
        )
        result = await result.fetchall()
        return bool(result[0][0])

    # Отримати список назв всіх груп - використовується для побудови клавіатури
    # Повертає список назв всіх груп - type list
    async def group_list_sql(self):
        keys = []
        reslt = await self.cur.execute("SELECT `groupname` FROM `groupa`")
        reslt = await reslt.fetchall()
        for i in reslt:
            keys.append(i[0])
        keys.sort()
        return keys

    # Додає розклад для певного вчителя -> name_teacher
    # Повертає збереження бази данних
    async def add_group_sql(self, user_id, group):
        await self.cur.execute(
            "INSERT INTO `groupa` (`user_id`,`groupname`) VALUES (?,?)",
            (user_id, group),
        )
        return await self.base.commit()

    # Оновлює розклад для певного вчителя -> name_teacher
    # Повертає збереження бази данних
    async def group_photo_update_sql(self, photo, groupname, transl):
        await self.cur.execute(
            "UPDATE `groupa` SET photos = ?, date = ? WHERE groupname = ?",
            (
                photo,
                transl,
                groupname,
            ),
        )
        return await self.base.commit()

    # Видаляє розклад для певного вчителя -> name_teacher
    # Повертає збереження бази данних
    async def delete_groups_sql(self, group):
        await self.cur.execute("DELETE FROM groupa WHERE groupname = ?", (group,))
        return await self.base.commit()

    async def see_rod_sql(self, user_id):
        # назва групи користувача
        groups = await self.cur.execute(
            "SELECT `group_user` FROM `user` WHERE `user_id` = ?", (user_id,)
        )
        rows_groups = await groups.fetchall()
        h = rows_groups[0][0]

        photo = await self.cur.execute(
            "SELECT photos FROM groupa WHERE groupname = ?", (h,)
        )
        rows_photo = await photo.fetchall()
        date = await self.cur.execute(
            "SELECT `date` FROM groupa WHERE groupname = ?", (h,)
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
