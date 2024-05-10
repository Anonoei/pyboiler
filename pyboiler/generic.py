class storage:
    pass


class hierarchy:
    """
    Dynamically create a hierarchical structure from a dict
    i_* methods are internal
    u_* methods are intended to be overridden by user inheritance
    """

    _parent = None
    _str_name = None

    def __init__(self, name: str, parent, heir: dict):
        self._parent = parent
        self._str_name = name
        self.i_init(heir)

    def __repr__(self) -> str:
        return f"<{self._str_name}>"

    @property
    def _name(self) -> str:
        if self._parent is None:
            return f"{type(self).__name__}.{self._str_name}"
        elif isinstance(self._parent, type(self)):
            return f"{self._parent._name}.{self._str_name}"
        return f"{type(self._parent).__name__}.{self._str_name}"

    def json(self) -> dict:
        """Return attributes as dictionary for json serialization"""
        fmt = {}
        for k in dir(self):
            if k in ["json"]:
                continue
            if k.startswith("_"):
                continue
            v = getattr(self, k)
            if k.startswith("_") or k.startswith("i_") or k.startswith("u_"):
                continue
            if isinstance(v, type(self)):
                fmt[k] = v.json()
            else:
                fmt[k] = v
        return fmt

    def i_init(self, heir: dict):
        """Internal init so it can be called outside of __init__"""
        for key, val in heir.items():
            k = self.u_fmt_k(key, val)
            v = self.u_fmt_v(k, val)
            setattr(self, k, v)

    def u_fmt_k(self, k, v):
        """User format k, used to change key formatting behavior"""
        return k

    def u_fmt_v(self, k, v):
        """User format v, used to change value formatting behavior"""
        if isinstance(v, dict):
            return type(self)(k, self, v)
        return v
