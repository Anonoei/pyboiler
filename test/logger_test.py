from anoboiler_test import _init_path

_init_path()

from anoboiler.logger import Logger


def test_logger_singleton():
    logger = Logger("anoboiler")
    assert logger is Logger()


def test_logger_log():
    Logger().info("Hello world!")


def test_logger_child():
    Logger().Child("test")
    Logger().test.warn("Test!")


def test_logger_child_child():
    Logger().test.Child(name="child")
    Logger().test.child.info("I'm aliiiiiiiive")
