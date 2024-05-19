"""Wrap python.logging Handlers"""

import sys

from ...generic import slot_storage
from .format import Formatter, default, colored
from .level import Level
from .record import Record


class Handler(slot_storage):
    """Handle log records"""

    __slots__ = ("_level", "_format", "_io", "_meta")

    def __init__(self, level=Level.NOTSET):
        self._level = level
        self._format = default
        self._io = None
        try:
            self._meta
        except AttributeError:
            self._meta = {}

    def __hash__(self):
        return hash(id(self))

    def __str__(self) -> str:
        return type(self).name()

    def __repr__(self) -> str:
        return f"<{type(self).__name__}: {self._level}>"

    @classmethod
    def name(cls):
        return cls.__name__[:-7].lower()

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, lvl: Level):
        self._level = Level.get(lvl)

    @property
    def formatter(self):
        return self._format

    @formatter.setter
    def formatter(self, val: Formatter):
        self._format = val

    def _handle(self, record: Record):
        if self.level < record.level:
            return False
        return True

    def handle(self, record: Record): ...

    def close(self): ...

    def format(self, record):
        return self._format.format(record)


class StreamHandler(Handler):
    """Writes log records to a stream"""

    def __init__(self, stream, level: Level):
        super().__init__(level)
        self._io = stream

    def flush(self):
        self._io.flush()

    def handle(self, record):
        if not self._handle(record):
            return
        msg = self.format(record)
        self._io.write(msg + "\n")
        self.flush()


class FileHandler(StreamHandler):
    """Writes log records to a file"""

    def __init__(self, filepath, level: Level, mode="a", encoding="UTF-8"):
        self._io = None
        self.meta = {}
        self.meta["filepath"] = filepath
        self.meta["mode"] = mode
        self.meta["encoding"] = encoding
        self.meta["open"] = False
        super().__init__(self._open(), level)

    def _open(self):
        _io = self._io
        if not self.meta["open"]:
            _io = open(
                self.meta["filepath"],
                mode=self.meta["mode"],
                encoding=self.meta["encoding"],
            )
            self.meta["open"] = True
        return _io

    def _close(self):
        self._io.close()
        self.meta["open"] = False


class StdoutHandler(StreamHandler):
    def __init__(self, level: Level):
        super().__init__(sys.stdout, level)
        self._format = colored


class StderrHandler(StreamHandler):
    def __init__(self, level: Level):
        super().__init__(sys.stderr, level)


handlers = {
    k[:-7].lower(): v
    for k, v in globals().items()
    if not k == "Handler" and k.endswith("Handler")
}
