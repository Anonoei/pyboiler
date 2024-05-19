"""Wrap python.logging Formatters"""

import re
from enum import Enum, auto
from typing import Any

from ...generic import slot_storage
from .config import config
from .record import Record

from ..color.colors import parse as c_parse
from ..color.colors import ST
from ..color.config import config as c_conf

from .level import LevelColors


class TagWrapper(slot_storage):
    __slots__ = ("tag", "inst", "val")

    def __init__(self, idx: int, tag: str, inst, val: Any = None):
        self.idx: int
        self.tag = tag
        self.inst = inst
        self.val = val

    def __str__(self) -> str:
        return f"{type(self).__name__} tag: {self.tag}, val: {self.val}"


class Tags(Enum):
    name = auto()
    levelnum = auto()
    levelname = auto()
    filepath = auto()
    filename = auto()
    linenum = auto()
    func = auto()
    time = auto()
    message = auto()

    @staticmethod
    def parse(string: str):
        raw_tags = re.findall(config.TAG_RE, string)
        tags = []
        for idx, item in enumerate(raw_tags):
            tag = item[2:-1]
            wrap = TagWrapper(idx, item, Tags[tag])
            tags.append(wrap)
        return tags


class TagsColor(Enum):
    name = f"{c_conf.TAG_START}sBOLD{c_conf.TAG_END}{c_conf.TAG_START}bBLACK{c_conf.TAG_END}{c_conf.TAG_START}fGREEN{c_conf.TAG_END}"
    levelnum = f"{c_conf.TAG_START}sBOLD{c_conf.TAG_END}{c_conf.TAG_START}fWHITE{c_conf.TAG_END}"
    levelname = f"{c_conf.TAG_START}sBOLD{c_conf.TAG_END}{c_conf.TAG_START}fWHITE{c_conf.TAG_END}"
    filepath = f"{c_conf.TAG_START}fBLUE{c_conf.TAG_END}"
    filename = f"{c_conf.TAG_START}fBLUE{c_conf.TAG_END}"
    linenum = f"{c_conf.TAG_START}fGREEN{c_conf.TAG_END}"
    func = f"{c_conf.TAG_START}fGREEN{c_conf.TAG_END}"
    time = f"{c_conf.TAG_START}fYELLOW{c_conf.TAG_END}"
    message = ""  # Defined in level.LevelColors


class Formatter:
    """Log record formatter"""

    __slots__ = ("fmt", "datefmt", "color")

    def __init__(self, fmt: str = None, datefmt: str = None, color=False):  # type: ignore
        if fmt is None:
            fmt = config.DFLT_FMT
        if datefmt is None:
            datefmt = config.DFLT_DATEFMT
        self.fmt = fmt
        self.datefmt = datefmt
        self.color = color

    @staticmethod
    def _parse(string):
        return Tags.parse(string)

    @staticmethod
    def _add_vals(tags, record: Record, datefmt, color: bool):
        mapping = {
            Tags.name: record.name,
            Tags.levelnum: record.level.value,
            Tags.levelname: record.level.name,
            Tags.filepath: str(record.meta.filepath),
            Tags.filename: record.meta.filepath.name,
            Tags.linenum: record.meta.line,
            Tags.func: record.meta.func,
            Tags.time: record.time.strftime(datefmt),
            Tags.message: record.msg,
        }
        if not color:
            for tag in tags:
                tag.val = mapping[tag.inst]
        else:
            for tag in tags:
                col = TagsColor[tag.inst.name].value
                if tag.inst.name == "message":
                    col = LevelColors[record.level.name].value
                tag.val = ""
                if col:
                    col_fmt = c_parse(col)
                    for fmt in col_fmt:
                        tag.val += fmt.val
                    tag.val += f"{mapping[tag.inst]}{ST.RESET.code()}"
                else:
                    tag.val = mapping[tag.inst]

    def format(self, record: Record) -> str:
        tags = type(self)._parse(self.fmt)
        type(self)._add_vals(tags, record, self.datefmt, self.color)

        message = self.fmt
        for tag in tags:
            message = message.replace(tag.tag, tag.val)
        return message


default = Formatter()
colored = Formatter(color=True)
