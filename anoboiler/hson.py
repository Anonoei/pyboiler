import json
from json import decoder, encoder


class HSONEncoder(json.encoder.JSONEncoder):
    """Encode non-json encodable objects"""

    def default(self, o):
        try:
            return super().default(o)
        except TypeError:
            try:
                return o.json()
            except AttributeError:
                return str(o)


def dump(*args, **kwargs):
    """Performs json.dump"""
    return json.dump(*args, **kwargs)


def dumps(*args, **kwargs):
    """Performs json.dumps"""
    kwargs["cls"] = HSONEncoder
    if not kwargs.get("pretty"):
        kwargs["indent"] = 4
    else:
        kwargs.pop("pretty")
    return json.dumps(*args, **kwargs)


def load(*args, **kwargs):
    """Performs json.load"""
    return json.load(*args, **kwargs)


def loads(*args, **kwargs):
    """Performs json.loads"""
    return json.loads(*args, **kwargs)
