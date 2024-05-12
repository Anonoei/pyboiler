"""Wrap python.logging levels"""

import logging
from enum import Enum

logging.addLevelName(5, "TRACE")


class _Level(Enum):
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


class Level:
    """Singleton instance for accessing _Level levels, with some helpers"""

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            for key in Level.s().keys():
                setattr(cls, key, _Level[key])
        return cls.__instance

    @staticmethod
    def s():
        """Return dict of each level name and it's value"""
        return {key.name: key.value for key in _Level}

    @staticmethod
    def fromInt(val: int):
        """Given an int, return the _Level enum"""
        levels = Level.s()
        names = []
        vals = []
        for k, v in Level.s().items():
            names.append(k)
            vals.append(v)
        return _Level[names[vals.index(val)]]
