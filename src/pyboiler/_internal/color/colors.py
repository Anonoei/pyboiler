from enum import Enum, unique
import re
from typing import Any

from .config import config
from ...generic import slot_storage


class ColorWrapper(slot_storage):
    __slots__ = ("idx", "tag", "val")

    def __init__(self, idx: int, tag: str, val: Any = None):
        self.idx: int
        self.tag = tag
        self.val = val

    def __str__(self) -> str:
        return f"{type(self).__name__} tag: {self.tag}"


@unique
class ColorEnum(Enum):
    """Base color enum class"""

    def code(self):
        return f"\033[{self.value}m"


class Style(ColorEnum):
    """Style codes"""

    r = RESET = 0
    b = BOLD = 1
    d = DIM = 2
    i = ITALIC = 3
    u = UNDERLINE = 4
    l = BLINK = 5
    v = REVERSE = 7
    h = HIDE = 8
    s = STRIKE = 9
    n = NORMAL = 22


S = ST = Style


class Foreground(ColorEnum):
    """Foreground codes"""

    RESET = 39

    b = BLACK = 30
    r = RED = 31
    g = GREEN = 32
    y = YELLOW = 33
    e = BLUE = 34
    m = MAGENTA = 35
    c = CYAN = 36
    w = WHITE = 37

    lb = L_BLACK = LIGHT_BLACK = 90
    lr = L_RED = LIGHT_RED = 91
    lg = L_GREEN = LIGHT_GREEN = 92
    ly = L_YELLOW = LIGHT_YELLOW = 93
    le = L_BLUE = LIGHT_BLUE = 94
    lm = L_MAGENTA = LIGHT_MAGENTA = 95
    lc = L_CYAN = LIGHT_CYAN = 96
    lw = L_WHITE = LIGHT_WHITE = 97


F = FG = Fore = Foreground


class Background(ColorEnum):
    """Background codes"""

    RESET = 49

    b = BLACK = 40
    r = RED = 41
    g = GREEN = 42
    y = YELLOW = 43
    e = BLUE = 44
    m = MAGENTA = 45
    c = CYAN = 46
    w = WHITE = 47

    lb = L_BLACK = LIGHT_BLACK = 100
    lr = L_RED = LIGHT_RED = 101
    lg = L_GREEN = LIGHT_GREEN = 102
    ly = L_YELLOW = LIGHT_YELLOW = 103
    le = L_BLUE = LIGHT_BLUE = 104
    lm = L_MAGENTA = LIGHT_MAGENTA = 105
    lc = L_CYAN = LIGHT_CYAN = 106
    lw = L_WHITE = LIGHT_WHITE = 107


B = BG = Back = Background


def parse(string: str):
    raw_tags = re.findall(config.TAG_RE, string)
    tags = []
    for idx, item in enumerate(raw_tags):
        tag_type = item[2]
        tag = item[3:-1]
        val = None
        if tag_type in ("s", "S"):
            val = Style[tag].code()
        elif tag_type in ("f", "F"):
            val = Foreground[tag].code()
        elif tag_type in ("b", "B"):
            val = Background[tag].code()
        else:
            raise Exception(f"Unknown tag type {tag_type}")
        wrap = ColorWrapper(idx, item, val)
        tags.append(wrap)
    return tags
