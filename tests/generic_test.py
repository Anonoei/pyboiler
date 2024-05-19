import pyboiler.generic as generic


def test_generic_storage():
    stor = generic.storage()
    stor.hello = "world"
    assert stor.json().keys() == {"hello": "world"}.keys()


def test_generic_slot_storage():
    class test(generic.slot_storage):
        __slots__ = ("k1", "k2")

        def __init__(self, v1, v2):
            self.k1 = v1
            self.k2 = v2

    stor = test("v1", "v2")
    assert stor.json() == {"k1": "v1", "k2": "v2"}


def test_generic_json():
    t_dict = {"test": "hierarchy", "subclass": {"another": "dict"}}
    heir = generic.hierarchy("test", None, t_dict)
    assert t_dict == heir.json()


if __name__ == "__main__":
    from utils import run_tests

    run_tests(globals())
