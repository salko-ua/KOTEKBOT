from src.data_base.create_db import BaseDBPart
from src.data_base.middleprocess import get_number, get_text, get_list


class SelectDB(BaseDBPart):
    async def count_user(self):
        counts = await self.cur.execute("SELECT COUNT(user_id) FROM user")
        return await get_number(counts)

    async def count_student(self):
        counts = await self.cur.execute("SELECT COUNT(user_id) FROM student")
        return await get_number(counts)

    async def list_id_student_agreed_news(self):
        result = await self.cur.execute("SELECT `user_id` FROM `student` WHERE send_news = ?", (1,))
        return await get_list(result)

    async def list_id_student_agreed_alert(self):
        result = await self.cur.execute(
            "SELECT `user_id` FROM `student` WHERE send_alert = ?", (1,)
        )
        return await get_list(result)

    async def group_for_student_id(self, user_id):
        name = await self.cur.execute(
            "SELECT `group_student` FROM `student` WHERE `user_id` = ?", (user_id,)
        )
        return await get_text(name)

    async def student_group_list(self):
        reslut = await self.cur.execute("SELECT `name_group` FROM `student_group`")
        return sorted(await get_list(reslut))

    async def see_rod(self, user_id):
        groups = await self.cur.execute(
            "SELECT `group_student` FROM `student` WHERE `user_id` = ?", (user_id,)
        )
        name_group = await get_text(groups)

        data_photo = await self.cur.execute(
            "SELECT `date`, `photo` FROM student_group WHERE name_group = ?", (name_group,)
        )
        data = await get_list(data_photo)

        if not data:
            return None, None

        return data[1], data[0]

    async def see_photo(self, name_photo):
        result = await (
            await self.cur.execute(
                "SELECT id_photo, date_photo FROM photo WHERE name_photo = ?",
                (name_photo,),
            )
        ).fetchone()
        try:
            id_photo = result[0]
            date_photo = result[1]
        except Exception:
            return False, None, None

        return True, id_photo, date_photo

    async def user_show_data(self, user_id):
        result = await self.cur.execute(
            "SELECT * FROM user WHERE user_id = ?",
            (user_id,),
        )
        return await result.fetchall()
