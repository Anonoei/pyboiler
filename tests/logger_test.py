from pyboiler.logger import Logger
from pyboiler.logging import Level, logging


def test_logging_level():
    assert Level.get("fatal") == Level.FATAL


def test_methods():
    log = logging("test", Level.TRACE)
    assert log.handlers()


def test_logging_log():
    log = logging("logging_test", Level.TRACE)
    # print(f"Handlers: {logging.availableHandlers().keys()}")
    log.trace("Hello world!")


def test_logger_singleton():
    logger = Logger("pyboiler_anonoei")
    assert logger is Logger()


def test_logger_log():
    Logger().info("Hello world!")


def test_logger_child():
    Logger().Child("test")
    Logger().test.warn("Test!")


def test_logger_child_child():
    Logger().test.Child(name="child")
    Logger().test.child.info("I'm aliiiiiiiive")
