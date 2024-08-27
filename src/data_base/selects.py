from src.data_base.create_db import BaseDBPart
from src.data_base.middleprocess import get_number, get_text, get_list, get_all_in_list


class SelectDB(BaseDBPart):
    async def count_user(self):
        counts = await self.cur.execute("SELECT COUNT(user_id) FROM user")
        return await get_number(counts)

    async def count_student(self):
        counts = await self.cur.execute("SELECT COUNT(user_id) FROM student")
        return await get_number(counts)

    async def list_of_all_user(self):
        result = await self.cur.execute("SELECT `user_id` FROM user")
        return await get_list(result)

    async def list_id_student_agreed_news(self):
        result = await self.cur.execute(
            "SELECT `user_id` FROM `student` WHERE send_news = ?", (1,)
        )
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
        result = await self.cur.execute("SELECT `name_group` FROM `student_group`")
        return sorted(await get_list(result))

    async def see_schedule_student(self, user_id):
        groups = await self.cur.execute(
            "SELECT `group_student` FROM `student` WHERE `user_id` = ?", (user_id,)
        )
        name_group = await get_text(groups)

        data_photo = await self.cur.execute(
            "SELECT photo, date FROM student_group WHERE name_group = ?", (name_group,)
        )
        data = await get_all_in_list(data_photo)

        if None in data or not data or data[0] == "":
            return []

        return data[0], data[1]

    async def see_schedule_for_group(self, name_group):
        data_photo = await self.cur.execute(
            "SELECT photo, date FROM student_group WHERE name_group = ?", (name_group,)
        )

        data = await get_all_in_list(data_photo)

        if None in data or not data or data[0] == "":
            return []

        return data[0], data[1]

    async def see_photo(self, name_photo):
        data_photo = await self.cur.execute(
            "SELECT photo, date_photo FROM photo WHERE name_photo = ?", (name_photo,)
        )

        data = await get_all_in_list(data_photo)
        if None in data or not data:
            return []

        return data[0], data[1]

    async def user_show_data(self, user_id):
        result = await self.cur.execute(
            "SELECT * FROM user WHERE user_id = ?", (user_id,)
        )
        return await get_all_in_list(result)

    async def get_student_theme(self, user_id):
        result = await self.cur.execute(
            "SELECT theme_name FROM student WHERE user_id = ?", (user_id,)
        )
        return await get_text(result)
