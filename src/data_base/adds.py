from typing import Literal

from src.data_base.create_db import BaseDBPart


class AddDB(BaseDBPart):
    async def add_voting(
        self, title: str, options: str, status: Literal["Waiting", "In progress", "Finished"]
    ):
        await self.cur.execute(
            "INSET INTO voting (title, options, status) VALUES (?,?,?)", (title, options, status)
        )
        return await self.base.commit()

    async def add_admin(self, user_id, username):
        await self.cur.execute(
            "INSERT INTO `admin` (`user_id`, `username`) VALUES (?,?)", (user_id, username)
        )
        return await self.base.commit()

    async def add_photo(self, name_photo, photo, date_photo):
        await self.cur.execute(
            "INSERT INTO photo (name_photo, photo, date_photo) VALUES (?,?,?)",
            (name_photo, photo, date_photo),
        )
        return await self.base.commit()

    async def add_student_group(self, student_group):
        await self.cur.execute(
            "INSERT INTO `student_group` (`name_group`) VALUES (?)", (student_group,)
        )
        return await self.base.commit()

    async def add_student(self, user_id, group_student):
        await self.cur.execute(
            "INSERT INTO `student` (`user_id`, `group_student`) VALUES (?,?)",
            (user_id, group_student),
        )
        return await self.base.commit()

    async def add_user(
        self, tg_id, first_name, last_name, username, date_join, last_msg, admin, group
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
            (tg_id, first_name, last_name, username, date_join, 1, last_msg, admin, group),
        )
        return await self.base.commit()
