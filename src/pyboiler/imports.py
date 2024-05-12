"""Import helpers"""

import importlib
import pathlib


def get_locals(obj, ignore=None):
    """Return locals for `obj`, while ignoring `ignore`

    Args:
        obj (Any): dict of locals to parse.
        ignore (list[str], optional): list of strings to ignore, with some special syntaxes

    >> `:ig` - check if obj.iter().endswith(ig)

    >> `!:ig` - only include obj.iter().endswith(ig)

    >> `ig:` - check if obj.iter().startswith(ig)

    >> `!ig:` - only include obj.iter().startswith(ig)


    Returns:
        A list of unique locals, ignoring anything starting with _ or values in ignore
    """
    # print(type(obj))
    # print(obj)

    if ignore is None:
        ignore = set("_:")

    def should_ignore(k, ign) -> bool:
        inverse = False
        for v in ign:
            if v[0] == "!":
                inverse = True
                v = v[1:]

            if v[-1] == ":":
                if k.startswith(v[:-1]):
                    return not inverse
            elif v[0] == ":":
                if k.endswith(v[1:]):
                    return not inverse
            else:
                if k == v:
                    return not inverse
        return inverse

    if isinstance(obj, dict):
        obj = list(obj.keys())
    elif isinstance(obj, object):
        obj = dir(obj)

    vals = []

    if isinstance(obj, list):
        for item in obj:
            if should_ignore(item, ignore):
                continue
            vals.append(item)
    return vals


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
