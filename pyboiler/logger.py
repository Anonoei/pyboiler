import logging

from ._log.level import Level


class Logger:
    __instance = None

    _parent = None
    _str_name = None
    _log = None

    def __new__(cls, name=None, level=Level().TRACE):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            cls._str_name = name
            cls._log = logging.Logger(name, level.value)
            cls.manager = logging.Manager(cls._log)
            cls._setLogs(cls.__instance)
        return cls.__instance

    @property
    def _name(self) -> str:
        if self._parent is None:
            return str(self._str_name)
        return f"{self._parent._name}.{self._str_name}"

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
    def __new__(cls, *args, **kkwargs):
        return object.__new__(cls, *args, **kkwargs)

    def __init__(self, parent, name):
        self._parent = parent
        self._str_name = name

    def _init(self, logger):
        self._log = logger
        self._setLogs()
