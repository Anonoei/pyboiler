from tests.a_import_test import _init_path

_init_path()

import pathlib

import pyboiler.imports as imports


def test_imports_get_locals():
    assert imports.get_locals(locals()) == ["@py_assert1"]


def test_imports_get_path():
    p_path = pathlib.Path("/some/path/to/mod")
    m_path = pathlib.Path("/some/path")
    assert imports.get_path(p_path, m_path) == "to.mod"
