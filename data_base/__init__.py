import asyncache
import aiosqlite
from data_base.admin_db import AdminDB
from data_base.photo_db import PhotoDB
from data_base.stats_db import StatsDB
from data_base.text_db import TextDB
from data_base.user_db import UserDB

from data_base.student_db import StudentDB
from data_base.teacher_db import TeacherDB

from data_base.student_group_db import StudentGroupDB
from data_base.teacher_group_db import TeacherGroupDB


class Database(
    AdminDB,
    PhotoDB,
    StatsDB,
    StudentDB,
    TeacherDB,
    StudentGroupDB,
    TeacherGroupDB,
    TextDB,
    UserDB,
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
                user_id       INTEGER NOT NULL, -- ід користувача (int)
                first_name    TEXT,             -- Ім'я користувача (str)
                last_name     TEXT,             -- Призвіще користувача (str)
                username      TEXT,             -- нікнейм користувача @ (str)
                date_join     TEXT,             -- дата приєднання (дати від 1 вересня 2023) (str)
                count_message INTEGER DEFAULT 0,-- кількість надісланих повідомлень боту (int)
                last_message  TEXT,             -- дата останнього повідомлення (str)
                admin         BOOLEAN,          -- якщо адмін True в іншому разі False
                student_group TEXT,             -- якщо є ім'я(str) немає absent(str)
                teacher_group TEXT              -- якщо є ім'я(str) немає absent(str)
            )
            """
        )
        await base.execute(
            """
            CREATE TABLE IF NOT EXISTS admin(
                user_id  INTEGER UNIQUE NOT NULL,
                username TEXT
            )
            """
        )
        await base.execute(
            """
            CREATE TABLE IF NOT EXISTS student(
                user_id       INTEGER UNIQUE,
                group_student TEXT,
                send_news     BOOLEAN DEFAULT 1,
                send_write    BOOLEAN DEFAULT 1,
                send_alert    BOOLEAN DEFAULT 1
            )
            """
        )
        await base.execute(
            """
            CREATE TABLE IF NOT EXISTS teacher(
                user_id       INTEGER UNIQUE,
                group_teacher TEXT,
                send_news     BOOLEAN DEFAULT 1,
                send_write    BOOLEAN DEFAULT 1,
                send_alert    BOOLEAN DEFAULT 1
            )
            """
        )
        await base.execute(
            """
            CREATE TABLE IF NOT EXISTS student_group(
                id         INTEGER PRIMARY KEY,
                name_group TEXT NOT NULL,
                photo      TEXT,
                date       TEXT
            )
            """
        )
        await base.execute(
            """
            CREATE TABLE IF NOT EXISTS teacher_group(
                id         INTEGER PRIMARY KEY,
                name_group TEXT NOT NULL,
                photo      TEXT,
                date       TEXT
            )
            """
        )
        await base.execute(
            """
            CREATE TABLE IF NOT EXISTS photo(
                id_photo   TEXT UNIQUE,
                name_photo TEXT,
                date_photo TEXT
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
                user_text    TEXT NOT NULL,
                name_group   TEXT
            )
            """
        )
        await base.commit()
        return cls(base, cur)
