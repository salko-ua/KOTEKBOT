from data_base.create_db import BaseDBPart


class STATSDB(BaseDBPart):
    async def add_or_update_stats_sql(self, name, count):
        name_exits = await self.cur.execute(
            "SELECT `id` FROM `stats` WHERE `stats_name` = ?", (name,)
        )
        name_exits = await name_exits.fetchall()
        if len(name_exits) == 0:
            await self.cur.execute(
                "INSERT INTO `stats` (`stats_name`) VALUES(?)", (name,)
            )
            await self.cur.execute(
                "UPDATE `stats` SET `count` = ? WHERE `stats_name` = ?",
                (
                    count,
                    name,
                ),
            )
        elif len(name_exits) == 1:
            count_db = await self.cur.execute(
                "SELECT `count` FROM `stats` WHERE `stats_name` = ?", (name,)
            )
            count_db = await count_db.fetchall()
            count_finish = int(count_db[0][0]) + int(count)
            await self.cur.execute(
                "UPDATE `stats` SET `count` = ? WHERE `stats_name` = ?",
                (
                    count_finish,
                    name,
                ),
            )
        elif len(name_exits) > 1:
            id = await self.cur.execute(
                "SELECT `id` FROM `stats` WHERE `stats_name` = ?", (name,)
            )
            id = await id.fetchone()
            await self.cur.execute("DELETE FROM `stats` WHERE `id` = ?", (id[0],))
        return await self.base.commit()

    # other
    async def see_all_stats_sql(self):
        all_stats: list[tuple[str, str]] = await (
            await self.cur.execute("SELECT `stats_name`, `count` FROM `stats`")
        ).fetchall()
        all_stats.sort(key=lambda e: int(e[1]), reverse=True)
        if len(all_stats) == 0:
            return " • Немає"
        text = ""
        for category, number in all_stats:
            text += f" • {category} : {number}\n"
        return text
