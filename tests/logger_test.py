from pyboiler.logger import Logger
from pyboiler.logging import Level, logging


def test_logging():
    assert Level.get("error") == Level.ERROR

    log = logging("logging_test", Level.TRACE)
    # print(f"Handlers: {logging.availableHandlers().keys()}")
    log.trace("Hello world!")


def test_logger():
    logger = Logger("pyboiler_anonoei")
    assert logger is Logger()

    Logger().info("Hello world!")

    Logger().Child("test")
    Logger().test.warn("Test!")

    Logger().test.Child(name="child")
    Logger().test.child.info("I'm aliiiiiiiive")


if __name__ == "__main__":
    from utils import run_tests

    run_tests(globals())
