import inspect
import pathlib

from ...generic import slot_storage


class MetaWrapper(slot_storage):
    __slots__ = ("filepath", "line", "func")

    def __init__(self, fr: inspect.FrameInfo):
        self.filepath = pathlib.Path(fr.filename)
        self.line = fr.lineno
        self.func = fr.function


def stack():
    depth = 0
    stack = inspect.stack()
    for item in stack:
        if item.filename == __file__:
            depth += 1
    return inspect.stack()[depth:]


def frame(depth=0) -> inspect.FrameInfo:
    return stack()[depth]


def meta(depth=0):
    return MetaWrapper(frame(depth))
