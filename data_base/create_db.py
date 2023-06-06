import abc
from aiosqlite import Cursor, Connection


class BaseDBPart(abc.ABC):
    def __init__(self, base: Connection, cursor: Cursor) -> None:
        self.base = base
        self.cur = cursor