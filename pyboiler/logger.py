import logging as _logging
import pathlib

from ._log.level import Level, _Level
from .config import config
from .logging import Manager, logging


class Logger:
    __instance = None

    _parent = None
    _str_name = None
    _log = None

    def __new__(cls, name=None, level=Level().TRACE):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            cls._str_name = name
            cls._log = logging(name, level)
            cls._addHandlers(cls.__instance)
            cls.manager = Manager(cls._log._log)
            cls._setLogs(cls.__instance)
        return cls.__instance

    def _addHandlers(self, level=config().SENTINEL):
        if level is config().SENTINEL:
            level = self._level
        self._log.addHandler(logging.availableHandlers()["StdoutHandler"](level=level))
        self._log.addHandler(
            logging.availableHandlers()["FileHandler"](self._logPath())
        )

    @property
    def _name(self) -> str:
        if self._parent is None:
            return str(self._str_name)
        return f"{self._parent._name}.{self._str_name}"

    @property
    def _level(self) -> _Level:
        return self._log.level

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
            print(f"{log_path = }")
        return log_path

    def _setLogs(self):
        for name, level in Level.s().items():
            lname = name.lower()
            log_cmd = lambda msg, log=self._log, lvl=level, *args, **kwargs: log.log(
                lvl, msg, *args, **kwargs
            )
            setattr(self, lname, log_cmd)

    def Child(self, name: str):
        log_inst = _Logger(self, name)
        log_inst._init(Logger().manager.getLogger(log_inst._name))
        setattr(self, name, log_inst)


class _Logger(Logger):
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def __init__(self, parent, name):
        self._parent = parent
        self._str_name = name

    def _init(self, logger: _logging.Logger):
        self._log = logging(self._name, self._parent._level)
        logger
        print(f"{self._log._log.handlers}")
        self._addHandlers()
        print(f"{self._log._log.handlers}")
        self._logPath()
        self._setLogs()
