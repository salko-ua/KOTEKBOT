from data_base.create_db import BaseDBPart


class ALLPHOTOTDB(BaseDBPart):
    async def add_calls_sql(self, types, id_photo, date_photo):
        id = 1
        ress = await self.cur.execute("SELECT `id` FROM all_photo WHERE id = ?", (id,))
        res = await ress.fetchall()
        if bool(len(res)) == False or res[0][0] != 1:
            await self.cur.execute("INSERT INTO `all_photo` (`id`) VALUES(?)", (id,))
            await self.cur.execute(
                "UPDATE `all_photo` SET `type` = ?,`id_photo` = ?, date_photo = ? WHERE `id` = ?",
                (
                    types,
                    id_photo,
                    date_photo,
                    id,
                ),
            )
        elif res[0][0] == 1:
            await self.cur.execute(
                "UPDATE `all_photo` SET `type` = ?,`id_photo` = ?, date_photo = ? WHERE `id` = ?",
                (
                    types,
                    id_photo,
                    date_photo,
                    id,
                ),
            )
        return await self.base.commit()

    async def delete_calls_sql(self):
        id = 1
        ress = await self.cur.execute("SELECT `id` FROM all_photo WHERE id = ?", (id,))
        res = await ress.fetchall()
        if bool(len(res)) == False or res[0][0] != 1:
            return False
        elif res[0][0] == 1:
            await self.cur.execute("DELETE FROM all_photo WHERE id = ?", (id,))
            await self.base.commit()
            return True

    async def see_calls_sql(self):
        id = 1
        ress = await self.cur.execute("SELECT `id` FROM all_photo WHERE id = ?", (id,))
        res = await ress.fetchall()
        date = await self.cur.execute(
            "SELECT `date_photo` FROM all_photo WHERE id = ?", (id,)
        )
        rows_date = await date.fetchall()
        try:
            if res[0][0] == 1:
                datka = rows_date[0][0]
                res = await self.cur.execute(
                    "SELECT id_photo FROM all_photo WHERE id = ?", (id,)
                )
                rows_res = await res.fetchall()
                resulta = rows_res[0][0]
                return True, resulta, datka
        except IndexError:
            return False, None, None
