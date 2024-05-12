"""Wraps python.json methods to utilize the HSONEncoder to encode pyboiler objects and others"""

import json
from json import decoder, encoder


class HSONEncoder(json.encoder.JSONEncoder):
    """Encode objects that json doesn't normally encode"""

    def default(self, o):
        try:
            return super().default(o)
        except TypeError:
            try:
                return o.json()
            except AttributeError:
                return str(o)


def dump(*args, **kwargs):
    """Serialize obj to a json formatted stream"""
    return json.dump(*args, **kwargs)


def dumps(*args, **kwargs):
    """Serialize obj to a json formatted string"""
    kwargs["cls"] = HSONEncoder
    if not kwargs.get("pretty"):
        kwargs["indent"] = 4
    else:
        kwargs.pop("pretty")
    return json.dumps(*args, **kwargs)


def load(*args, **kwargs):
    """Deserialize a json formatted stream to python objects"""
    return json.load(*args, **kwargs)


def loads(*args, **kwargs):
    """Deserialize a json formatted string to python objects"""
    return json.loads(*args, **kwargs)
