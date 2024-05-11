def _init_path():
    import pathlib
    import sys

    PATH_ROOT = pathlib.Path(__file__).parent.parent

    sys.path[0] = str(PATH_ROOT / "src")


_init_path()


def test_import():
    import pyboiler
