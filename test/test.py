import importlib
import pathlib
import sys


def main():
    PATH_ROOT = pathlib.Path(__file__).parent.parent
    sys.path[0] = str(PATH_ROOT)
    import pyboiler

    print(f"Imported modules: {pyboiler.dir()}")

    for k, v in globals().items():
        if k.startswith("test"):
            print(f"Running '{k}'!")
            v()
            print()


def test_config():
    from pyboiler.config import config

    print(f"config.PATH_ROOT = {config().PATH_ROOT}")


def test_generic():
    import pyboiler.generic as generic

    hier = generic.hierarchy(
        "test", None, {"test": "hierarchy", "subclass": {"another": "dict"}}
    )
    print(f"{hier._name} = {hier.json()}")
    print(f"{hier.subclass._name} = {hier.subclass.json()}")


def test_logging():
    from pyboiler.logging import Level, logging

    log = logging("pyboiler_test", Level.TRACE)

    print(f"Handlers: {logging.availableHandlers().keys()}")
    log.trace("Hello world!")


def test_logger():
    from pyboiler.logger import Logger

    logger = Logger("pyboiler")
    logger.info("Hello world!")


if __name__ == "__main__":
    main()
