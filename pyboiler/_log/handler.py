import logging
import sys

from .format import Formatter


class Handler(logging.Handler):
    def __init__(self, level=logging.NOTSET):
        super().__init__(level)
        self.setFormatter(Formatter())


class StreamHandler(Handler, logging.StreamHandler):
    pass


class FileHandler(Handler, logging.FileHandler):
    pass


class StdoutHandler(StreamHandler):
    def __init__(self):
        super().__init__(sys.stdout)


class StderrHandler(StreamHandler):
    def __init__(self):
        super().__init__(sys.stderr)


handlers = {k: v for k, v in globals().items() if k.endswith("Handler")}
