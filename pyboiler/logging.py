import logging as _logging
import sys

from ._log.handler import handlers
from ._log.level import Level, _Level


class logging:
    def __init__(self, name, level: _Level):
        self._log = _logging.Logger(name, level.value)
        self.setLogs()

    def addHandler(self, hdlr):
        self._log.addHandler(hdlr)

    @staticmethod
    def availableHandlers():
        return handlers

    @staticmethod
    def availableLevels():
        return Level.s()

    def setLogs(self):
        for name, level in logging.availableLevels().items():
            lname = name.lower()
            log_cmd = lambda msg, log=self, lvl=level, *args, **kwargs: log.log(
                lvl, msg, *args, **kwargs
            )
            setattr(self, lname, log_cmd)

    def log(self, *arg, **kwargs):
        if not self._log.handlers:
            self.addHandler(logging.availableHandlers()["StdoutHandler"]())
        self._log.log(*arg, **kwargs)
