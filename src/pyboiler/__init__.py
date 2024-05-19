"""pyboiler's initialization and dynamic importer

 Imports all files in src/pyboiler/* so they can be imported as
 `pyboiler.config`
"""

import pathlib

__version__ = "0.3.0"
__author__ = "Anonoei <dev@anonoei.com>"
init_run = False


def __init(_val=[]):
    """Import all files in `import_path`"""
    if _val:
        return
    _val.append(True)
    from .config import config
    from .imports import get_imports

    import_path = pathlib.Path(__file__).parent

    # print(f"Running __init on {import_path}")
    for k, v in get_imports(import_path).items():
        globals()[k] = v

    globals()["settings"].Settings().deserialize()


def view():
    """View all available pyboiler imports"""
    __init()
    imports = globals()["imports"].get_locals(globals())
    imports.sort()
    return imports
