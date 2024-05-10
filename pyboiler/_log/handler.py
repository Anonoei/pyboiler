import logging
import pathlib
import sys

from ..config import config
from .format import Formatter


class Handler(logging.Handler):
    def __init__(self, level=logging.NOTSET):
        super().__init__(level)
        self.setFormatter(Formatter())


class StreamHandler(logging.StreamHandler):
    def __init__(self, stream=None, level=config().SENTINEL):
        super().__init__(stream)
        self.setFormatter(Formatter())
        if not level is config().SENTINEL:
            self.level = level.value


class _FileHandler(logging.FileHandler):
    def __init__(self, filename, mode="a", encoding=None, delay=False, errors=None):
        super().__init__(filename, mode, encoding, delay, errors)
        self.setFormatter(Formatter())


class StdoutHandler(StreamHandler):
    def __init__(self, level=config().SENTINEL):
        super().__init__(stream=sys.stdout)


class StderrHandler(StreamHandler):

    def __init__(self, level=config().SENTINEL):
        super().__init__(stream=sys.stderr)


class FileHandler(_FileHandler):

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
