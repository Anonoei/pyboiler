"""Wrap python.logging in an interface I prefer"""

import logging as _logging
import sys
from logging import Manager

from ._log.handler import handlers
from ._log.level import Level, _Level


class logging:
    def __init__(self, name, level: _Level, logger=None):
        if logger is None:
            logger = _logging.Logger(name, level.value)
        self._log = logger
        self.setLogs()

    def addHandler(self, hdlr):
        self._log.addHandler(hdlr)

    @staticmethod
    def availableHandlers():
        return handlers

    @staticmethod
    def availableLevels():
        return Level.s()

    @property
    def level(self) -> _Level:
        return Level.fromInt(self._log.level)

    def setLogs(self):
        for name, level in logging.availableLevels().items():
            lname = name.lower()
            log_cmd = lambda msg, log=self, lvl=level, *args, **kwargs: log.log(
                lvl, msg, *args, **kwargs
            )
            setattr(self, lname, log_cmd)

    def log(self, *arg, **kwargs):
        self._log.log(*arg, **kwargs)
