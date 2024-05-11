__version__ = "0.0.1"


def __init():
    from .config import config
    from .imports import get_imports

    import_path = config().PATH_ROOT / "src" / "pyboiler"

    # print(f"Running __init on {import_path}")
    for k, v in get_imports(import_path).items():
        globals()[k] = v

    globals()["settings"].Settings().deserialize()


__init()


def dir():
    imports = globals()["imports"].get_locals(globals())
    imports.sort()
    return imports
