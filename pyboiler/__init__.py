def __init():
    from .config import config
    from .imports import get_imports

    import_path = config().PATH_ROOT / "pyboiler"

    # print(f"Running __init on {import_path}")
    for k, v in get_imports(import_path).items():
        globals()[k] = v


__init()


def dir():
    imports = [k for k in globals() if not k.startswith("_")][:-1]
    return imports
