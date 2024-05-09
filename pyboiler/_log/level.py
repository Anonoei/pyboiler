import logging
from enum import Enum

logging.addLevelName(5, "TRACE")


class _Level(Enum):
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
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            for key in _Level:
                setattr(cls, key, _Level()[key])
        return cls.__instance
