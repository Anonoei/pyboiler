import re
from string import Formatter as _Formatter

from .colors import ColorEnum

_str_formatter = _Formatter()


class Formatter:
    _tag = re.compile(r"\\?</?((?:[fb]g\s)?[^<>\s]*)>", re.I)

    def __init__(self, fmt, *, defaults=None):
        self._fmt = fmt or self.default_format
        self._defaults = defaults

    def validate(self):
        """Validate the input format, ensure it matches the correct style"""
        if not self._tag.search(self._fmt):
            raise ValueError(f"Invalid format '{self._fmt}'")

    def _format(self, record):
        if defaults := self._defaults:
            values = defaults | record.__dict__
        else:
            values = record.__dict__
        return self._fmt % values

    def format(self, record):
        try:
            return self._format(record)
        except KeyError as e:
            raise ValueError("Formatting field not found in record: %s" % e)


def escape(obj):
    if isinstance(obj, ColorEnum):
        return f"\033[{obj.value}m"
    return ""
