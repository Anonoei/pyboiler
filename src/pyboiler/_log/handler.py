"""Wrap python.logging Handlers"""

import logging
import sys

from ..config import config
from .format import Formatter


class Handler(logging.Handler):
    """Wrap python.logging.Handler to use pyboiler._log.format.Formatter"""

    def __init__(self, level=logging.NOTSET):
        super().__init__(level)
        self.setFormatter(Formatter())


class StreamHandler(logging.StreamHandler):
    """Wrap python.logging.StreamHandler to use pyboiler._log.format.Formatter"""

    def __init__(self, stream=None, level=config().SENTINEL):
        super().__init__(stream)
        self.setFormatter(Formatter())
        if not level is config().SENTINEL:
            self.level = level.value


class _FileHandler(logging.FileHandler):
    """Wrap python.logging.FileHandler to use pyboiler._log.format.Formatter"""

    def __init__(self, filename, mode="a", encoding=None, delay=False, errors=None):
        super().__init__(filename, mode, encoding, delay, errors)
        self.setFormatter(Formatter())


class StdoutHandler(StreamHandler):
    """Wrap StreamHandler and set it to use sys.stdout"""

    def __init__(self, level=config().SENTINEL):
        super().__init__(stream=sys.stdout)


class StderrHandler(StreamHandler):
    """Wrap StreamHandler and set it to use sys.stderr"""

    def __init__(self, level=config().SENTINEL):
        super().__init__(stream=sys.stderr)


class FileHandler(_FileHandler):
    """Wrap python.logging.FileHandler"""

    def __init__(
        self,
        filename,
        mode="a",
        encoding=None,
        delay=False,
        errors=None,
        level=config().SENTINEL,
    ):
        super().__init__(filename, mode, encoding, delay, errors)


handlers = {k: v for k, v in globals().items() if k.endswith("Handler")}
