import asyncache
import aiosqlite
from data_base.user_db import USERDB
from data_base.teacher_db import TEACHERDB
from data_base.admin_db import ADMINDB
from data_base.group_db import GROUPDB
from data_base.teachers_name_db import TEACHERGROUPDB
from data_base.all_photo_db import ALLPHOTOTDB
from data_base.text_db import TEXTDB
from data_base.stats_db import STATSDB


class Database(
    USERDB, TEACHERDB, ADMINDB, GROUPDB, TEACHERGROUPDB, ALLPHOTOTDB, TEXTDB, STATSDB
):
    @classmethod
    @asyncache.cached({})
    async def setup(cls):
        base = await aiosqlite.connect("data/database.db")
        cur = await base.cursor()
        if base:
            print("DATA BASE CONNECTED")
        await base.execute(
            """
            CREATE TABLE IF NOT EXISTS user(
                user_id    INTEGER UNIQUE,
                Name       TEXT,
                Nickname   TEXT,
                group_user TEXT
            )
            """
        )
        await base.execute(
            """
            CREATE TABLE IF NOT EXISTS groupa(
                id        INTEGER PRIMARY KEY,
                user_id   INTEGER NOT NULL,
                groupname TEXT NOT NULL,
                photos    TEXT,
                date      TEXT
            )
            """
        )
        await base.execute(
            """
            CREATE TABLE IF NOT EXISTS all_photo(
                id         INTEGER PRIMARY KEY,
                id_photo   TEXT,
                type       TEXT,
                date_photo TEXT
            )
            """
        )
        await base.execute(
            """
            CREATE TABLE IF NOT EXISTS admin(
                id       INTEGER PRIMARY KEY NOT NULL,
                user_id  INTEGER UNIQUE NOT NULL,
                Name     TEXT,
                Nickname TEXT
            )
            """
        )
        await base.execute(
            """
            CREATE TABLE IF NOT EXISTS teachers(
                id       INTEGER PRIMARY KEY NOT NULL,
                user_id  INTEGER UNIQUE NOT NULL,
                Name     TEXT,
                Nickname TEXT,
                teacher_name TEXT
            )
            """
        )
        await base.execute(
            """
            CREATE TABLE IF NOT EXISTS teachers_name(
                id        INTEGER PRIMARY KEY,
                user_id   INTEGER NOT NULL,
                name_teacher TEXT NOT NULL,
                photos    TEXT,
                date      TEXT
            )
            """
        )
        await base.execute(
            """
            CREATE TABLE IF NOT EXISTS stats(
                id           INTEGER PRIMARY KEY NOT NULL,
                stats_name   TEXT NOT NULL,
                count        TEXT
            )
            """
        )
        await base.execute(
            """
            CREATE TABLE IF NOT EXISTS text(
                id           INTEGER PRIMARY KEY NOT NULL,
                text_user   TEXT NOT NULL,
                group_name TEXT
            )
            """
        )
        await base.commit()
        return cls(base, cur)
