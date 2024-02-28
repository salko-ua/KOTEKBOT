from src.data_base.create_db import BaseDBPart


class UpdateDB(BaseDBPart):
    async def update_student(self, user_id, group_student):
        await self.cur.execute(
            "UPDATE `student` SET `group_student` = ? WHERE user_id = ?", (group_student, user_id)
        )
        return await self.base.commit()

    async def student_change_news(self, boolean: bool, user_id: int):
        await self.cur.execute(
            "UPDATE `student` SET `send_news` = ? WHERE user_id = ?", (boolean, user_id)
        )
        return await self.base.commit()

    async def student_change_alert(self, boolean: bool, user_id: int):
        await self.cur.execute(
            "UPDATE `student` SET `send_alert` = ? WHERE user_id = ?", (boolean, user_id)
        )
        return await self.base.commit()

    async def student_group_photo_update(self, name_group, photo, date):
        await self.cur.execute(
            "UPDATE `student_group` SET photo = ?, date = ? WHERE name_group = ?",
            (photo, date, name_group),
        )
        return await self.base.commit()

    async def update_photo(self, name_photo, photo, date_photo):
        await self.cur.execute(
            "UPDATE photo SET photo = ?, date_photo = ? WHERE name_photo = ?",
            (photo, date_photo, name_photo),
        )

    async def update_user(
        self, user_id, first_name, last_name, username, last_interaction, admin, student_group
    ):
        count_interaction = await self.cur.execute(
            "SELECT count_interaction FROM user WHERE user_id = ?", (user_id,)
        )
        count_interaction = await count_interaction.fetchone()
        count_interaction = count_interaction[0]
        count_interaction += 1

        await self.cur.execute(
            """UPDATE user 
            SET     
                first_name = ?,    
                last_name = ?,    
                username = ?,    
                count_interaction = ?,  
                last_interaction = ?,  
                admin = ?,   
                student_group = ?
            WHERE user_id = ?
            """,
            (
                first_name,
                last_name,
                username,
                count_interaction,
                last_interaction,
                admin,
                student_group,
                user_id,
            ),
        )
        return await self.base.commit()
