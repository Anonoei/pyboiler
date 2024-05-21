"""Wrap python.logging levels"""

from enum import Enum, unique
from ..color.config import config as c_conf
from ..color.colors import FG, BG, ST


@unique
class Level(Enum):
    """Enum for getting logging levels"""

    ALL = 100
    ERROR = 50
    WARN = 40
    INFO = 30
    DEBUG = 20
    TRACE = 10
    NOTSET = 0

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
        if isinstance(key, Level):
            return key
        if isinstance(key, str):
            return Level[key.upper()]
        return Level.NOTSET

    @staticmethod
    def s():
        return list(Level)


class LevelColors(Enum):
    ALL = ""
    ERROR = f"{c_conf.TAG_START}fRED{c_conf.TAG_END}"
    WARN = f"{c_conf.TAG_START}fMAGENTA{c_conf.TAG_END}"
    INFO = f"{c_conf.TAG_START}fWHITE{c_conf.TAG_END}"
    DEBUG = f"{c_conf.TAG_START}fLIGHT_WHITE{c_conf.TAG_END}"
    TRACE = f"{c_conf.TAG_START}fLIGHT_BLUE{c_conf.TAG_END}"
    NOTSET = ""
