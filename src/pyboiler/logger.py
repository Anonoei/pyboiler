"""Wrap pyboiler.logging in a Singleton for more concrete logging structures

Example Usage:
```python
from pyboiler.logger import Logger, Level

Logger("MyProject", Level().WARN)
Logger().trace("This is a trace")
subm = Logger().Child("Submodule")
subm.trace("And another!")  # Or Logger().subm.trace("And another!")
```
"""

import logging as _logging
import pathlib
from logging import Manager
from typing import TYPE_CHECKING

from .config import config
from .logging import Level, logging


class Logger:
    """Project root logger"""

    __instance = None

    _parent = None
    _str_name: str = None  # type: ignore
    _log: logging = None  # type: ignore

    def Child(self, name: str, level=None):
        if level is None:
            level = self._level
        log_inst = _Logger(self, name)
        log_inst._init(Logger().manager.getLogger(log_inst._name), level)
        setattr(self, name, log_inst)

    @property
    def _level(self) -> Level:
        return self._log.level

    @_level.setter
    def _level(self, level):
        self._log.level = level

    def __new__(cls, name=None, level=Level.TRACE):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            if name is None:
                name = "Logger"
            cls._str_name = name
            cls._log = logging(name, level)
            cls._addHandlers(cls.__instance)
            cls.manager = Manager(cls._log._log)  # type: ignore
            cls._setLogs(cls.__instance)
        return cls.__instance

    def _addHandlers(self, level=config().SENTINEL):
        if level is config().SENTINEL:
            level = self._level
        self._log.addHandler(logging.handlers()["StdoutHandler"](level=level))
        self._log.addHandler(logging.handlers()["FileHandler"](self._logPath()))

    @property
    def _name(self) -> str:
        if self._parent is None:
            return str(self._str_name)
        return f"{self._parent._name}.{self._str_name}"

    def _logPath(self) -> pathlib.Path:
        path_sep = self._name.split(".")
        if len(path_sep) > 1:
            path_sep = path_sep[1:]
        log_path = config().PATH_LOGS
        for idx, item in enumerate(path_sep):
            if idx == len(path_sep) - 1:
                log_path.mkdir(exist_ok=True, parents=True)
                item = f"{item}.log"
            log_path /= item
            # print(f"{log_path = }")
        return log_path

    def _setLogs(self):
        for level in self._log.levels():
            lname = level.name.lower()
            log_cmd = (
                lambda msg, log=self._log, lvl=level.value, *args, **kwargs: log.log(
                    lvl, msg, *args, **kwargs
                )
            )
            setattr(self, lname, log_cmd)

    if TYPE_CHECKING:

        def __getattr__(self, key):
            return lambda msg: print(msg)


class _Logger(Logger):
    """Child Logger class"""

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def __init__(self, parent, name):
        self._parent = parent
        self._str_name = name

    def _init(self, logger: _logging.Logger, level):
        self._log = logging(self._name, level, logger)
        # print(f"{self._log._log.handlers}")
        self._addHandlers()
        # print(f"{self._log._log.handlers}")
        self._logPath()
        self._setLogs()
