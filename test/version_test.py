from anoboiler_test import _init_path

_init_path()

from anoboiler.version import Version


def test_version_init():
    Version(0, 0, 1)


def test_version_eq():
    ver = Version(0, 0, 1)
    assert ver == Version(0, 0, 1)
    assert not ver == Version(0, 0, 2)


def test_version_lt():
    ver = Version(0, 0, 2)
    assert ver < Version(0, 0, 3)
    assert ver < Version(0, 1, 0)
    assert ver < Version(1, 0, 0)


def test_version_gt():
    ver = Version(0, 2, 1)
    assert ver > Version(0, 1, 1)
    assert ver > Version(0, 2, 0)
    assert Version(1, 0, 0) > ver
