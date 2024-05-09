import logging

from ._log.level import Level


class Logger:
    __instance = None

    def __new__():
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance
