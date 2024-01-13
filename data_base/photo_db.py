from data_base.create_db import BaseDBPart


class PhotoDB(BaseDBPart):
    async def add_photo_sql(self, name_photo, id_photo, date_photo):
        await self.cur.execute(
            """
                               DELETE FROM photo
                               WHERE name_photo = ? AND (SELECT COUNT(id_photo) FROM photo WHERE name_photo = ?) > 0
                               """,
            (
                name_photo,
                name_photo,
            ),
        )
        await self.cur.execute(
            "INSERT INTO photo (name_photo, id_photo, date_photo) VALUES (?,?,?)",
            (
                name_photo,
                id_photo,
                date_photo,
            ),
        )
        return await self.base.commit()

    async def delete_photo_sql(self, name_photo):
        result = await (
            await self.cur.execute(
                "SELECT COUNT(id_photo) FROM photo WHERE name_photos = ?", (name_photo,)
            )
        ).fetchall()
        if len(result) == False:
            return False
        elif len(result) == True:
            await self.cur.execute(
                "DELETE FROM photo WHERE name_photo = ?", (name_photo,)
            )
            await self.base.commit()
            return True

    async def see_photo_sql(self, name_photo):
        result = await (
            await self.cur.execute(
                "SELECT id_photo, date_photo FROM photo WHERE name_photo = ?",
                (name_photo,),
            )
        ).fetchall()
        try:
            id_photo = result[0][0]
            date_photo = result[0][1]
        except:
            return False, None, None

        return True, id_photo, date_photo
