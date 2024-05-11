from anoboiler_test import _init_path

_init_path()

from anoboiler.settings import Settings

t_dict = {"example": "value", "test": {"c_ex": "value2", "test2": {"cc_ex": "value3"}}}


def test_settings_singleton():
    sets = Settings()
    assert sets is Settings()


def test_settings_init():
    Settings().init("example", t_dict["example"])


def test_settings_child():
    Settings().Child("test")


def test_settings_child_init():
    Settings().test.init("c_ex", t_dict["test"]["c_ex"])


def test_settings_child_child():
    Settings().test.Child("test2")


def test_settings_child_child_init():
    Settings().test.test2.init("cc_ex", t_dict["test"]["test2"]["cc_ex"])


def test_settings_json():
    assert Settings().json() == t_dict
