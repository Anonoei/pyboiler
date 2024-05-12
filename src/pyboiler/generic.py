"""Generic class implementations that can be extended in user code"""

from typing import TYPE_CHECKING

from .imports import get_locals


class storage:
    """Used to save values similar to a C struct

    ```
    from pyboiler.generic import storage
    stor = storage()
    stor.value = "example"
    ```
    """

    _ignore = set(("_:", "json"))

    def json(self) -> dict:
        """Return attributes as dictionary for json serialization
        Instances of `type(self)` are returned as dictionaries
        """
        fmt = {}
        for k in get_locals(self, self._ignore):
            v = getattr(self, k)
            if isinstance(v, type(self)):
                fmt[k] = v.json()
            else:
                fmt[k] = v
        return fmt

    if TYPE_CHECKING:

        def __getattr__(self, key):
            return lambda msg: print(msg)


class hierarchy(storage):
    """Dynamically create a hierarchical structure from a dict

    u_* methods are intended to be overridden by children

    ```python
    from pyboiler.generic import hierarchy
    h_dict = {"these": {"are": "nested"}, "dicts": "hierarchy"}
    hier = hierarchy("root", None, h_dict)
    print(hier.these.are) # Returns "nested"
    print(hier.json()) # Returns h_dict
    ```
    """

    _parent = None
    _str_name = None

    def __init__(self, name: str, parent, heir: dict):
        self._parent = parent
        self._str_name = name
        self._ignore = set(("_:", "json", "u_:"))
        self._i_init(heir)

    def __repr__(self) -> str:
        return f"<{self._str_name}>"

    @property
    def _name(self) -> str:
        if self._parent is None:
            return f"{type(self).__name__}.{self._str_name}"
        elif isinstance(self._parent, type(self)):
            return f"{self._parent._name}.{self._str_name}"
        return f"{type(self._parent).__name__}.{self._str_name}"

    def _i_init(self, heir: dict):
        """Internal init so it can be called outside of __init__"""
        for key, val in heir.items():
            k = self.u_fmt_k(key, val)
            v = self.u_fmt_v(k, val)
            setattr(self, k, v)

    def u_fmt_k(self, k, v):
        """Format keys before setattr"""
        return k

    def u_fmt_v(self, k, v):
        """Format v before setattr.

        Use `v = super().u_fmt(k, v)` if `isinstance(v, dict)` isn't implemented in child methods
        """
        if isinstance(v, dict):
            return type(self)(k, self, v)
        return v

    if TYPE_CHECKING:

        def __getattr__(self, key):
            return lambda msg: print(msg)
