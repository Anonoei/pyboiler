"""Wrap python.logging levels"""

import logging
from enum import Enum, unique

logging.addLevelName(5, "TRACE")


@unique
class Level(Enum):
    """Enum for getting logging levels"""

    FATAL = logging.FATAL
    ERROR = logging.ERROR
    WARN = logging.WARN
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    TRACE = 5

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

    @staticmethod
    def get(key):
        if isinstance(key, str):
            return Level[key.upper()]
        for v in Level.s():
            if v.value == key:
                return v
        return None

    @staticmethod
    def s():
        return list(Level)
