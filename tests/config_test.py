from tests.a_import_test import _init_path

_init_path()

import src.pyboiler.hson as hson
from src.pyboiler.config import config


def test_config_init():
    config()


def test_config_singleton():
    conf = config()
    assert conf is config()


def test_config_set():
    config().PATH_ROOT.exists()


def test_config_json():
    config().json()
