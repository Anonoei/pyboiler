"""Wrap python.logging Handlers"""

import sys
import pathlib
import socket
import random

from ...generic import slot_storage
from .format import Formatter, default, colored
from .level import Level
from .record import Record

from .queue import Queue


class Handler(slot_storage):
    """Handle logs"""

    __slots__ = ("_level", "_format")

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
        """Get the base name of this handler"""
        return cls.__name__[:-7].lower()

    @property
    def level(self):
        """Get/Set this handler's level"""
        return self._level

    @level.setter
    def level(self, lvl: Level):
        self._level = Level.get(lvl)

    @property
    def formatter(self):
        """Get/Set this handler's formatter"""
        return self._format

    @formatter.setter
    def formatter(self, val: Formatter):
        self._format = val

    def _handle(self, record: Record):
        if self.level < record.level:
            return False
        return True

    def handle(self, record: Record):
        """Handle a log record"""
        ...

    def format(self, record):
        """Format a log record"""
        return self._format.format(record)


class StreamHandler(Handler):
    """Writes logs to stream"""

    __slots__ = ("_level", "_format", "_io")

    def __init__(self, stream, level: Level):
        super().__init__(level)
        self._io = stream

    def handle(self, record):
        if not self._handle(record):
            return
        msg = self.format(record)
        self._io.write(msg + "\n")
        self._io.flush()


class FileHandler(StreamHandler):
    """Writes logs to file"""

    __slots__ = ("_level", "_format", "_io")

    def __init__(
        self, filepath: pathlib.Path, level: Level, mode="a", encoding="UTF-8"
    ):
        if not filepath.exists():
            mode = "w"
        _io = filepath.open(mode=mode, encoding=encoding)
        super().__init__(_io, level)

    def close(self):
        Queue().stop()
        self._io.close()

    def handle(self, record):
        sup = super()
        Queue().add([lambda s=sup, r=record: sup.handle(record)])


class OverwriteFileHandler(FileHandler):
    """Write logs to file and overwrite them if they exist"""

    __slots__ = ("_level", "_format", "_io")

    def __init__(self, filepath: pathlib.Path, level: Level, encoding="UTF-8"):
        super().__init__(filepath, level, "w", encoding)


class StdoutHandler(StreamHandler):
    """Write logs to stdout"""

    __slots__ = ("_level", "_format", "_io")

    def __init__(self, level: Level):
        super().__init__(sys.stdout, level)
        self._format = colored


class StderrHandler(StreamHandler):
    """Write logs to stderr"""

    __slots__ = ("_level", "_format", "_io")

    def __init__(self, level: Level):
        super().__init__(sys.stderr, level)


class SocketHandler(Handler):
    __slots__ = ("_level", "_format", "_socket", "_address", "_encoding")

    def __init__(self, host, port, level: Level, encoding="UTF-8"):
        self._level = level
        self._format = default
        self._address = (host, port)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect(self._address)
        self._encoding = encoding

    def handle(self, record: Record):
        if not self._handle(record):
            return
        msg = self.format(record)
        self._socket.send(msg.encode(self._encoding))


handlers = {
    k[:-7].lower(): v
    for k, v in globals().items()
    if not k == "Handler" and k.endswith("Handler")
}
