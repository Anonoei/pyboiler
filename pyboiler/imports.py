"""Import helpers"""

import importlib
import pathlib

from .config import config


def get_path(path: pathlib.Path, mod_path: pathlib.Path) -> str:
    """Return the import path for a given pathlib.Path object"""
    return path.relative_to(mod_path).with_suffix("").as_posix().replace("/", ".")


def get_imports(path) -> dict:
    """Import all modules in a directory tree and returns them as a dictionary."""
    if isinstance(path, str):
        path = pathlib.Path(path)
    imports = {}
    # print(f"Getting imports from {path}")
    for fpath in path.iterdir():
        # print(f"Checking {fpath}")
        if fpath.is_file():
            if fpath.name.startswith("_") or not fpath.name.endswith(".py"):
                continue
            import_path = get_path(fpath, path.parent)
            # print(f"importing {import_path}")
            imports[fpath.name[:-3]] = importlib.import_module(import_path)
    return imports
