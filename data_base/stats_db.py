from data_base.create_db import BaseDBPart


class STATSDB(BaseDBPart):
    async def add_or_update_stats_sql(self, name, count):
        name_exits = await (await self.cur.execute(
            "SELECT `id` FROM `stats` WHERE `stats_name` = ?", (name,)
        )).fetchall()

        if len(name_exits) == 0:
            await self.cur.execute(
                "INSERT INTO `stats` (`stats_name`) VALUES(?)", (name,)
            )
            await self.cur.execute(
                "UPDATE `stats` SET `count` = ?, `count_month` = ?, `count_week` = ? WHERE `stats_name` = ?",
                (
                    count,
                    count,
                    count,
                    name,
                ),
            )
        elif len(name_exits) == 1:
            count_db = await (await self.cur.execute(
                "SELECT `count` FROM `stats` WHERE `stats_name` = ?", (name,)
            )).fetchall()
            count_week = await (await self.cur.execute(
                "SELECT `count_week` FROM `stats` WHERE `stats_name` = ?", (name,)
            )).fetchall()
            count_month = await (await self.cur.execute(
                "SELECT `count_month` FROM `stats` WHERE `stats_name` = ?", (name,)
            )).fetchall()

            count_db = count_db[0][0] + count
            count_week = count_week[0][0] + count
            count_month = count_month[0][0] + count

            await self.cur.execute(
                "UPDATE `stats` SET `count` = ?, `count_month` = ?, `count_week` = ? WHERE `stats_name` = ?",
                (
                    count_db,
                    count_month,
                    count_week,
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
        all_stats: list[tuple[str, int, int, int]] = await (
            await self.cur.execute("SELECT `stats_name`, `count` FROM `stats`")
        ).fetchall()
        month_stats: list[tuple[str, int, int, int]] = await (
            await self.cur.execute("SELECT `stats_name`, `count_month` FROM `stats`")
        ).fetchall()
        week_stats: list[tuple[str, int, int, int]] = await (
            await self.cur.execute("SELECT `stats_name`, `count_week` FROM `stats`")
        ).fetchall()
        all_stats.sort(key=lambda e: e[1], reverse=True)
        month_stats.sort(key=lambda e: e[1], reverse=True)
        week_stats.sort(key=lambda e: e[1], reverse=True)
        if len(all_stats) == 0:
            return " • Немає\n"," • Немає\n"," • Немає\n"
        else:
            always = ""
            month = ""
            week = ""
            for category, number in all_stats:
                always += f" • {category} : {number}\n"
            for category, num_month in month_stats:
                month += f" • {category} : {num_month}\n"
            for category, num_week in week_stats:
                week += f" • {category} : {num_week}\n"
            return always, month, week
    
    async def rcreate(self):
        # cpmentarів
        all_user = await (await self.cur.execute("SELECT * FROM stats")).fetchall()
        new_list_all_user = []
        for i in range(0, len(all_user)):
            new_tuple = all_user[i][1], int(all_user[i][2])
            new_list_all_user.append(tuple(new_tuple))
        await self.cur.execute("DROP TABLE stats")
        await self.base.commit()
        await self.base.execute(
            """
            CREATE TABLE stats(
                id           INTEGER PRIMARY KEY NOT NULL,
                stats_name   TEXT NOT NULL,
                count        INTEGER,
                count_month  INTEGER,
                count_week   INTEGER
            )
            """
        )
        await self.base.commit()
        for i in range(0, len(new_list_all_user)):
            await self.cur.execute(
                "INSERT INTO `stats` (`stats_name`, `count`, count_month, count_week) VALUES (?,?,?,?)",
                (
                    new_list_all_user[i][0],
                    new_list_all_user[i][1],
                    0,
                    0,
                ),
            )
        await self.base.commit()
    
    async def delete_stats_sql(self, name):
        await self.cur.execute("DELETE FROM stats WHERE stats_name = ?",(name,))
        await self.base.commit()
    
    async def delete_month_sql(self):
        count = 0
        await self.cur.execute("UPDATE `stats` SET `count_month` = ?",(count,))
        await self.base.commit()

    async def delete_week_sql(self):
        count = 0
        await self.cur.execute("UPDATE `stats` SET `count_week` = ?",(count,))
        await self.base.commit()
