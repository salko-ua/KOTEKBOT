from src.data_base.create_db import BaseDBPart


class AddDB(BaseDBPart):
    async def add_admin(self, user_id, username):
        await self.cur.execute(
            "INSERT INTO `admin` (`user_id`, `username`) VALUES (?,?)",
            (
                user_id,
                username,
            ),
        )
        return await self.base.commit()

    async def add_photo(self, name_photo, id_photo, date_photo):
        await self.cur.execute(
            "INSERT INTO photo (name_photo, id_photo, date_photo) VALUES (?,?,?)",
            (
                name_photo,
                id_photo,
                date_photo,
            ),
        )
        return await self.base.commit()

    async def add_student_group(self, student_group):
        await self.cur.execute(
            "INSERT INTO `student_group` (`name_group`) VALUES (?)",
            (student_group,),
        )
        return await self.base.commit()

    async def add_student(self, user_id, group_student):
        await self.cur.execute(
            "INSERT INTO `student` (`user_id`, `group_student`) VALUES (?,?)",
            (user_id, group_student),
        )
        return await self.base.commit()

    async def add_user(
        self,
        user_id,
        first_name,
        last_name,
        username,
        date_join,
        count_message,
        last_message,
        admin,
        student_group,
    ):
        await self.cur.execute(
            """INSERT INTO user(
                user_id,    
                first_name,
                last_name,
                username,
                date_join,
                count_interaction,
                last_interaction,
                admin,
                student_group) 
            VALUES 
            (?,?,?,?,?,?,?,?,?)
            """,
            (
                user_id,
                first_name,
                last_name,
                username,
                date_join,
                count_message,
                last_message,
                admin,
                student_group,
            ),
        )
        return await self.base.commit()
