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

import pathlib

from .generic import storage
from .config import config
from .logging import Level, logging


class Logger(storage):
    """Project root logger"""

    __slots__ = ["_internal", "_parent", "_str_name", "_logger"]

    __instance = None

    def __new__(cls, name=None, level: Level = None):
        if cls.__instance is None:
            inst = object.__new__(cls)
            if name is None:
                name = "Logger"
            if level is None:
                level = Level.TRACE

            inst._internal = {}
            inst._parent = None
            inst._str_name = name
            inst._logger = logging(name, Level.get(level))
            inst._addHandlers()
            cls.__instance = inst
        return cls.__instance

    def __init__(self, *args, **kwargs):
        pass

    def Child(self, name: str, level=None):
        """Create a child logger"""
        if level is None:
            level = self.get_level()
        log_inst = _Logger(self, name, level)
        self._internal[name] = log_inst

    def get_level(self) -> Level:
        """Get log level"""
        return self._logger.level

    def set_level(self, level):
        """Set log level"""
        self._logger.level = level

    def _addHandlers(self, lvl: Level = config().SENTINEL):  # type: ignore
        if lvl is config().SENTINEL:
            lvl: Level = self.get_level()
        self._logger.mk_handler("stdout", lvl)
        self._logger.mk_handler("file", self._log_path(), lvl)

    def name(self) -> str:
        """Return structured name"""
        if self._parent is None:
            return self._str_name
        return f"{self._parent.name}.{self._str_name}"

    def _log_path(self) -> pathlib.Path:
        path_sep = self.name().split(".")
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

    def trace(self, msg):
        """log.trace"""
        self._logger.trace(msg)

    def debug(self, msg):
        """log.debug"""
        self._logger.debug(msg)

    def info(self, msg):
        """log.info"""
        self._logger.info(msg)

    def warn(self, msg):
        """log.warn"""
        self._logger.warn(msg)

    def error(self, msg):
        """log.error"""
        self._logger.error(msg)

    def exception(self, msg):
        """log.exception"""
        self._logger.exception(msg)


class _Logger(Logger):
    """Child Logger class"""

    __slots__ = ["_internal", "_parent", "_str_name", "_logger"]

    def __new__(cls, *args, **kwargs):
        inst = object.__new__(cls)
        inst.__init__(*args, **kwargs)
        return inst

    def __init__(self, parent, name: str, level: Level):
        self._internal = {}
        self._parent = parent
        self._str_name = name
        self._logger = logging(self.name, level)
        self._addHandlers()
