"""Wrap python.logging in an interface I prefer"""

import logging as _logging
from typing import TYPE_CHECKING

from ._internal.log import Level, handlers


class logging:
    def __init__(self, name, level: Level, logger=None):
        if logger is None:
            logger = _logging.Logger(name, level.value)
        self._log: _logging.Logger = logger
        self._setLogs()

    def addHandler(self, hdlr):
        """Add a handler"""
        self._log.addHandler(hdlr)

    @staticmethod
    def handlers():
        """Return all available handlers"""
        return handlers

    @staticmethod
    def levels():
        """Return all available levels"""
        return Level.s()

    @property
    def level(self) -> Level:
        """Return logging level"""
        return Level.get(self._log.level)  # type: ignore

    @level.setter
    def level(self, level):
        """Set logging level"""
        self._log.setLevel(level.value)

    def _setLogs(self):
        for level in logging.levels():
            lname = level.name.lower()
            log_cmd = lambda msg, log=self, lvl=level.value, *args, **kwargs: log.log(
                lvl, msg, *args, **kwargs
            )
            setattr(self, lname, log_cmd)

    def log(self, *arg, **kwargs):
        """Log a message

        Dynamically called from logging.<level name>

        Args:
            level (int): logging level
            msg (str): message to log
        """
        self._log.log(*arg, **kwargs)

    if TYPE_CHECKING:

        def __getattr__(self, key):
            return lambda msg: print(msg)
