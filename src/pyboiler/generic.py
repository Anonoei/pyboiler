"""Generic class implementations that can be extended in user code"""


class pyboiler_generic:
    def json(self):
        """Returns the object as a dict"""
        ...


class storage(pyboiler_generic):
    """Used to save values similar to a C struct

    ```
    from pyboiler.generic import storage
    stor = storage()
    stor.value = "example"
    ```
    """

    __slots__ = ["_internal"]

    def __init__(self):
        self._internal = {}

    def json(self) -> dict:
        """Return attributes as dictionary for json serialization
        Instances of `type(self)` are returned as dictionaries
        """
        fmt = {}
        for k, v in self._internal.items():
            if isinstance(v, type(self)):
                fmt[k] = v.json()
                continue

            fmt[k] = v

        return fmt

    def keys(self):
        """Return names of all objects"""
        return self._internal.keys()

    def values(self):
        """Return values of all objects"""
        return self._internal.values()

    def items(self):
        """Return k, v of all objects"""
        return self._internal.items()

    def __getitem__(self, key):
        getattr(self, key)

    def __setitem__(self, key, val):
        setattr(self, key, val)

    def __getattr__(self, key):
        if key in self.__slots__ or key == "__wrapped__":
            return super(storage, self).__getattribute__(key)
        return self._internal[key]

    def __setattr__(self, key, val):
        if key in self.__slots__ or key == "__wrapped__":
            super(storage, self).__setattr__(key, val)
            return
        self._internal[key] = val


class slot_storage(pyboiler_generic):
    """Children of this class must have __slots__ defined"""

    def json(self, ignore=None):
        if ignore is None:
            ignore = []
        return {k: getattr(self, k) for k in type(self).__slots__ if not k in ignore}  # type: ignore


class hierarchy(pyboiler_generic):
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

    __slots__ = ("_parent", "_name", "_data")

    def __init__(self, name: str, parent, heir: dict):
        self._parent = parent
        self._name = name
        self._data = {}

        def _getattr(self, key):
            if key in self.__slots__:
                return self.__dict__[key]
            return self._data[key]

        def _setattr(self, key, val):
            if key in self.__slots__:
                self.__dict__[key] = val
                return
            self._data[key] = val

        self.__getattr__ = _getattr
        self.__setattr__ = _setattr

        self._i_init(heir)

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self._name}>"

    def json(self):
        fmt = {}
        for k, v in self._data.items():
            if isinstance(v, type(self)):
                fmt[k] = v.json()
            else:
                fmt[k] = v
        return fmt

    @property
    def name(self) -> str:
        """Return hierarchical name"""
        if self._parent is None:
            return f"{type(self).__name__}: {self._name}"
        elif isinstance(self._parent, type(self)):
            return f"{self._parent.name}.{self._name}"
        return f"{type(self._parent).__name__}: {self._name}"

    def _i_init(self, heir: dict):
        """Internal init so it can be called outside of __init__"""
        for key, val in heir.items():
            k = self.u_fmt_k(key, val)
            v = self.u_fmt_v(k, val)
            self._data[k] = v

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
