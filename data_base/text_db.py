from data_base.create_db import BaseDBPart


class TEXTDB(BaseDBPart):
    async def add_text_sql(self, text_user, group_name):
        exits = await (
            await self.cur.execute(
                "SELECT id FROM text WHERE group_name=?", (group_name,)
            )
        ).fetchall()

        if len(exits) < 1:
            await self.cur.execute(
                "INSERT INTO `text` (`text_user`, `group_name`) VALUES (?,?)",
                (
                    text_user,
                    group_name,
                ),
            )
        elif len(exits) > 0:
            await self.cur.execute(
                "UPDATE `text` SET `text_user` = ? WHERE `group_name` = ?",
                (
                    text_user,
                    group_name,
                ),
            )
        return await self.base.commit()

    async def see_text_sql(self, group_name):
        exits = await (
            await self.cur.execute(
                "SELECT text_user FROM text WHERE group_name=?", (group_name,)
            )
        ).fetchall()

        if len(exits) < 1:
            return False, None
        elif len(exits) > 0:
            return True, exits[0][0]
