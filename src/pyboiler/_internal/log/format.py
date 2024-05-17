"""Wrap python.logging Formatters"""

import logging

default_fmt = "%(asctime)s <%(name)s> %(levelname)s: %(message)s"
default_datefmt = "%Y-%m-%d_%H.%M.%S"


class Formatter(logging.Formatter):
    """Wrap python.logging.Formatter"""

    def __init__(self, *args, **kwargs):
        super().__init__(
            fmt=default_fmt,
            datefmt=default_datefmt,
            *args,
            **kwargs,
        )
