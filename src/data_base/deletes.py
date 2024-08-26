from src.data_base.create_db import BaseDBPart


class DeleteDB(BaseDBPart):
    async def delete_admins(self, user_id):
        await self.cur.execute("DELETE FROM admin WHERE user_id = ?", (user_id,))
        return await self.base.commit()

    async def delete_photo(self, name_photo):
        await self.cur.execute("DELETE FROM photo WHERE name_photo = ?", (name_photo,))
        return await self.base.commit()

    async def delete_student(self, user_id):
        await self.cur.execute("DELETE FROM student WHERE user_id = ?", (user_id,))
        return await self.base.commit()

    async def delete_student_from_group(self, group):
        await self.cur.execute("DELETE FROM student WHERE group_student = ?", (group,))
        return await self.base.commit()

    async def delete_student_group_photo(self, student_group):
        await self.cur.execute(
            "UPDATE `student_group` SET photo = NULL, date = NULL WHERE name_group = ?",
            (student_group,),
        )
        return await self.base.commit()

    async def delete_student_group(self, student_group):
        await self.cur.execute(
            "DELETE FROM student_group WHERE name_group = ?", (student_group,)
        )
        return await self.base.commit()
