import asyncache
import aiosqlite
from data_base.user_db import UserDB
from data_base.teacher_db import TeacherDB
from data_base.admin_db import AdminDB
from data_base.group_db import GroupDB
from data_base.teachers_name_db import TeacherGroupDB
from data_base.all_photo_db import AllPhotoDB
from data_base.text_db import TextDB
from data_base.stats_db import StatsDB


class Database(
    UserDB, TeacherDB, AdminDB, GroupDB, TeacherGroupDB, AllPhotoDB, TextDB, StatsDB
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
                count        INTEGER
                count_month  INTEGER
                count_week   INTEGER
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
