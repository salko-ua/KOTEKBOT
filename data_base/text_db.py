from data_base.create_db import BaseDBPart


class TextDB(BaseDBPart):
    async def add_text_sql(self, text_user, group_name):
        exits = await (
            await self.cur.execute(
                "SELECT `id` FROM `text` WHERE `name_group`=?", (group_name,)
            )
        ).fetchall()
        if len(exits) < 1:
            await self.cur.execute(
                "INSERT INTO `text` (`user_text`, `name_group`) VALUES (?,?)",
                (
                    text_user,
                    group_name,
                ),
            )
        elif len(exits) > 0:
            await self.cur.execute(
                "UPDATE `text` SET `user_text` = ? WHERE `name_group` = ?",
                (
                    text_user,
                    group_name,
                ),
            )
        return await self.base.commit()

    async def see_text_sql(self, group_name):
        exits = await (
            await self.cur.execute(
                "SELECT `user_text` FROM `text` WHERE `name_group`=?", (group_name,)
            )
        ).fetchall()

        if len(exits) < 1:
            return False, None
        elif len(exits) > 0:
            return True, exits[0][0]
