import os

import aiosqlite
import asyncache

from src.data_base.add import AddDB
from src.data_base.delete import DeleteDB
from src.data_base.exist import ExistDB
from src.data_base.select import SelectDB
from src.data_base.update import UpdateDB


class Database(AddDB, DeleteDB, ExistDB, SelectDB, UpdateDB):
    @classmethod
    @asyncache.cached({})
    async def setup(cls):
        if not os.path.exists("./data"):
            os.mkdir("./data")

        base = await aiosqlite.connect("data/database.db")
        cur = await base.cursor()

        if base:
            print("DATA BASE CONNECTED")

        await base.execute(
            """
            CREATE TABLE IF NOT EXISTS user(
                user_id           INTEGER NOT NULL, -- ід користувача (int)
                first_name        TEXT,             -- Ім'я користувача (str)
                last_name         TEXT,             -- Призвіще користувача (str)
                username          TEXT,             -- нікнейм користувача @ (str)
                date_join         TEXT,             -- дата приєднання (дати від 1 вересня 2023) (str)
                count_interaction INTEGER DEFAULT 0,-- кількість взаємодій боту (int)
                last_interaction  TEXT,             -- дата останньої взаємодій (str)
                admin             BOOLEAN,          -- якщо адмін True в іншому разі False
                student_group     TEXT              -- якщо є ім'я(str) немає absent(str)
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
            CREATE TABLE IF NOT EXISTS photo(
                id_photo   TEXT UNIQUE,
                name_photo TEXT,
                date_photo TEXT
            )
            """
        )
        return cls(base, cur)