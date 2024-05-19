"""pyboiler.settings file"""

from typing import TYPE_CHECKING

from .config import config

if config().SERIAL == "json":
    from .hson import dumps, loads
else:
    from .hml import dumps, loads

from .generic import hierarchy


class Settings(hierarchy):
    """Global settings, intended to be edited by users"""

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            cls._str_name = "Settings"
            cls._defaults = {}
            cls._settings = {}
        return cls.__instance

    def __init__(self):
        pass

    def Child(self, name: str):
        sets_inst = getattr(self, name, config().SENTINEL)

        if sets_inst is config().SENTINEL:
            sets_inst = _Settings(name, self)
            self._settings[name] = sets_inst
            self._defaults[name] = sets_inst
            setattr(self, name, sets_inst)
        elif not isinstance(sets_inst, _Settings):
            raise Exception(f"Child '{name}' is not _Settings instance")
        return sets_inst

    def get(self, key, default=config().SENTINEL):
        if default is config().SENTINEL:
            _get = self._settings.get(key, config().SENTINEL)
            if _get is config().SENTINEL:
                _get = self._defaults.get(key)
            return _get
        return self._settings.get(key, default)

    def set(self, key, val):
        self._defaults[key] = val
        setattr(self, key, lambda s=self, k=key: s.get(k))

    def softSet(self, key, val):
        self._settings[key] = val

    def init(self, name: str, default):
        self.set(name, default)

    def serialize(self) -> None:
        s_data = None
        config().FILEPATH_SETTINGS.write_text(dumps(self._json()))

    def deserialize(self) -> None:
        if not config().FILEPATH_SETTINGS.exists():
            return
        self.from_dict(loads(config().FILEPATH_SETTINGS.read_text()))

    def from_dict(self, d: dict):
        for k, v in d.items():
            if isinstance(v, dict):
                _child = self.Child(k)
                _child.from_dict(v)
            else:
                if v is None:
                    v = config().SENTINEL
                self.softSet(k, v)

    def json(self) -> dict:
        """Return attributes as dictionary for json serialization"""
        fmt = {}
        for k, v in self._defaults.items():
            if isinstance(v, _Settings):
                fmt[k] = v.json()
            else:
                fmt[k] = v
        return fmt

    def _json(self) -> dict:
        """Internal serialization method for writing to settings.json"""
        fmt = {}
        for k, v in self._defaults.items():
            if isinstance(v, _Settings):
                fmt[k] = v._json()
            else:
                fmt[k] = self.get(k, None)
        return fmt

    def u_fmt_k(self, *args, **kwargs):
        raise NotImplementedError()

    def u_fmt_v(self, *args, **kwargs):
        raise NotImplementedError()

    def _i_init(self, *args, **kwargs):
        raise NotImplementedError()

    if TYPE_CHECKING:

        def __getattr__(self, key):
            return lambda msg: print(msg)


class _Settings(Settings):
    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj.__init__(*args, **kwargs)
        return obj

    def __init__(self, name: str, parent):
        self._parent = parent
        self._str_name = name
        self._defaults = {}
        self._settings = {}
