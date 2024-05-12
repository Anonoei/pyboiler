"""pyboiler's initialization and dynamic importer

 Imports all files in src/pyboiler/* so they can be imported as
 `pyboiler.config`
"""

import pathlib

__version__ = "0.0.4"
__author__ = "Anonoei <dev@anonoei.com>"


def __init():
    """Import all files in `import_path`"""
    from .config import config
    from .imports import get_imports

    import_path = pathlib.Path(__file__).parent

    # print(f"Running __init on {import_path}")
    for k, v in get_imports(import_path).items():
        globals()[k] = v

    globals()["settings"].Settings().deserialize()


__init()


def dir():
    """List all available pyboiler imports"""
    imports = globals()["imports"].get_locals(globals())
    imports.sort()
    return imports
