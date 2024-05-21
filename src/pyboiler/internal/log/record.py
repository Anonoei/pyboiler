"""Wrap python.logging.LogRecord"""

import datetime as dt

from ...generic import slot_storage
from .inspect import meta
from .level import Level


class Record(slot_storage):
    """A LogRecord instance represents an event being logged."""

    __slots__ = ("name", "level", "msg", "time", "meta")

    def __init__(self, name: str, level: Level, msg: str, depth: int):
        self.name = name
        self.level = level
        self.msg = msg
        self.time = dt.datetime.now()
        self.meta = meta(depth)
