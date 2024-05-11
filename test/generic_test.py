from anoboiler_test import _init_path

_init_path()

import anoboiler.generic as generic

t_dict = {"test": "hierarchy", "subclass": {"another": "dict"}}


def test_generic_init():
    generic.hierarchy("test", None, t_dict)


def test_generic_json():
    heir = generic.hierarchy("test", None, t_dict)
    assert t_dict == heir.json()
