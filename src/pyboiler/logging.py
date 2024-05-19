"""Wrap python.logging in an interface I prefer"""

import queue

from ._internal.log import Handler, Level, Record, config, handlers
from .generic import storage

logstore = storage()
logstore.queue = queue.Queue()


class logging:

    __slots__ = ("name", "_level", "handlers", "disabled")

    def __init__(self, name, level):
        self.name = name
        self._level = Level.get(level)
        self.handlers = dict()
        self.disabled = False

    @property
    def level(self):
        """Get logging level"""
        return self._level

    @level.setter
    def level(self, level):
        self._level = level

    @staticmethod
    def avail_handlers():
        return list(handlers.keys())

    @staticmethod
    def avail_levels():
        return list(Level)

    def mk_handler(self, handler, *args, **kwargs):  # type: ignore
        """Add a handler"""
        if isinstance(handler, str):
            handler: Handler = handlers[handler.lower()]
        else:
            if issubclass(handler, Handler):
                self.handlers[handler.name()] = handler
                return
        if not issubclass(handler, Handler):  # type: ignore
            raise Exception(f"Invalid handler: {handler}")

        if not handler in self.handlers:
            self.handlers[handler.name()] = handler(*args, **kwargs)

    def rm_handler(self, hdlr):
        """Remove a handler"""
        if isinstance(hdlr, str):
            hdlr = handlers[hdlr]
        self.handlers.pop(hdlr)

    def ls_handlers(self):
        return self.handlers

    def trace(self, msg):
        """Log trace"""
        self._log(Level.TRACE, msg)

    def debug(self, msg):
        """Log debug"""
        self._log(Level.DEBUG, msg)

    def info(self, msg):
        """Log info"""
        self._log(Level.INFO, msg)

    def warn(self, msg):
        """Log warn"""
        self._log(Level.WARN, msg)

    def error(self, msg):
        """Log error"""
        self._log(Level.ERROR, msg)

    def exception(self, msg):
        """Log error and raise an exception"""
        pass

    def log(self, lvl: Level, msg: str):
        """This probably shouldn't be used in your code"""
        self._log(lvl, msg)

    def _log(self, lvl: Level, msg: str):
        """logging internal method"""
        if Level.get(lvl) < self._level:
            return
        record = Record(self.name, lvl, msg, depth=3)
        self.handle(record)

    def handle(self, record: Record):
        if self.disabled:
            return
        for handler in self.handlers.values():
            handler.handle(record)
