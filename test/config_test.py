from anoboiler_test import _init_path

_init_path()

import anoboiler.hson as hson
from anoboiler.config import config


def test_config_init():
    config()


def test_config_singleton():
    conf = config()
    assert conf is config()


def test_config_set():
    config().PATH_ROOT.exists()


def test_config_json():
    config().json()
