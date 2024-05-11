import importlib
import json
import os
import pathlib
import sys
import time


def main():
    test_start = time.perf_counter()
    PATH_ROOT = pathlib.Path(__file__).parent.parent
    sys.path[0] = str(PATH_ROOT)
    import src.pyboiler

    print(f"Imported modules: {src.pyboiler.dir()}")

    def test():
        for k, v in globals().items():
            if k.startswith("test"):
                print(f"Running '{k}'!")
                start = time.perf_counter()
                try:
                    v()
                except KeyboardInterrupt:
                    pass
                except Exception:
                    print(f"Failed on {k}!")
                    raise
                print()
                try:
                    input(f"Finished {k}! ({time.perf_counter() - start:.2f}s)")
                except KeyboardInterrupt:
                    sys.exit(0)

    from pyboiler.config import config
    from pyboiler.profiler import get, run, view

    run("test()", locals(), globals(), False)
    view(get())
    os.remove(config().PATH_PROFILE)
    print(f"Complete after {time.perf_counter() - test_start:.2f}")


def test_config():
    import pyboiler.hson as hson
    from pyboiler.config import config

    print(f"config().json() = {hson.dumps(config().json(), indent=4)}")


def test_generic():
    import pyboiler.generic as generic

    hier = generic.hierarchy(
        "test", None, {"test": "hierarchy", "subclass": {"another": "dict"}}
    )
    print(f"{hier._name} = {hier.json()}")
    print(f"{hier.subclass._name} = {hier.subclass.json()}")


def test_hml():
    import pyboiler.hml as hml

    dict_obj = {
        "example": "dict",
        "obj": "here",
        "dict": {"nested": "dict", "list": ["item1", "item2"]},
    }

    xml = hml.dumps(dict_obj)
    # print(xml)
    loads_obj = hml.loads(xml)
    # print(pxml)j
    print(f"{dict_obj == loads_obj = }")


def test_logging():
    from pyboiler.config import config
    from pyboiler.logging import Level, logging

    log = logging("pyboiler_anonoei_test", Level.TRACE)

    print(f"Handlers: {logging.availableHandlers().keys()}")
    log.trace("Hello world!")


def test_logger():
    from pyboiler.logger import Logger

    logger = Logger("pyboiler_anonoei")
    logger.info("Hello world!")
    logger.Child("test")
    logger.test.warn("Test!")
    logger.test.Child(name="child")
    logger.test.child.info("I'm aliiiiiiiive")


def test_platform():
    from pyboiler.config import config

    print(f"{config().SYS_PLAT}")


def test_settings():
    import pyboiler.hson as hson
    from pyboiler.settings import Settings

    Settings().init("example", "value")
    Settings().Child("test")
    Settings().test.init("example2", "val")
    print(".json(): " + json.dumps(Settings().json(), indent=4))
    print("_settings: " + hson.dumps(Settings()._settings, indent=4))
    print("_defaults: " + hson.dumps(Settings()._defaults, indent=4))
    Settings().serialize()


if __name__ == "__main__":
    main()
