import pyboiler.hml as hml

t_dict = {
    "example": "dict",
    "obj": "here",
    "dict": {"nested": "dict", "list": ["item1", "item2"]},
}


def test_hml_serial():
    xml = hml.dumps(t_dict)
    loads_obj = hml.loads(xml)
    assert t_dict == loads_obj
