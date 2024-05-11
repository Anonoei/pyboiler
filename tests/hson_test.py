from tests.a_import_test import _init_path

_init_path()

import json

import pyboiler.hson as hson

t_dict = {"test": "hson", "serial": {"dict": "same"}, "list": ["i1", "i2"]}


def test_hson_same():
    t_str = json.dumps(t_dict)
    assert json.loads(t_str) == hson.loads(t_str)
