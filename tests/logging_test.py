from tests.a_import_test import _init_path

_init_path()

import logging as _logging

from pyboiler._log.level import _Level
from pyboiler.config import config
from pyboiler.logging import Level, logging


def test_logging_level():
    assert Level.TRACE == _Level.TRACE


def test_logging_log():
    log = logging("logging_test", Level.TRACE)
    # print(f"Handlers: {logging.availableHandlers().keys()}")
    log.trace("Hello world!")
