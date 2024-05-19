"""Script configuration singleton for internal variables

config contains global configuration information not intended to be modified by users

Example usage
```python
from pyboiler.config import config
print(config().PATH_ROOT)
```

Add your own global configuration variables
```python
config().MY_VARIABLE = "Hello, world!"
```
"""

import pathlib
import subprocess

from .imports import get_locals


class config:
    """Global configuration, not intended to be modified by users"""

    __instance = None

    # define singleton attributes
    #: Path to project root, defaults to the toplevel of the git repository
    PATH_ROOT: pathlib.Path = None  # type: ignore
    #: PATH_ROOT / "logs"
    PATH_LOGS: pathlib.Path = None  # type: ignore
    FILEPATH_PROFILE: pathlib.Path = None  # type: ignore
    FILEPATH_SETTINGS: pathlib.Path = None  # type: ignore

    #: Defines what serialize type to use. One of ['json', 'xml']
    SERIAL: str = "json"

    #: pyboiler.Platform enum for the current platform
    SYS_PLAT = None
    SENTINEL = object()

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            cls.__instance._init()
        return cls.__instance

    def _init(self):
        """Initialize config attributes"""
        self.PATH_ROOT = self._init_path_root()
        self.PATH_LOGS = self.PATH_ROOT / "logs"
        self.FILEPATH_PROFILE = self.PATH_ROOT / "profiler.stats"
        self.FILEPATH_SETTINGS = self.PATH_ROOT / f"settings.{self.SERIAL}"

        self.SYS_PLAT = self._init_sys_plat()

    def json(self) -> dict:
        """Return config attributes as a dictionary"""
        fmt = {}

        for k in get_locals(self, ("init", "json")):
            fmt[k] = getattr(self, k)
        return fmt

    def _init_path_root(self) -> pathlib.Path:
        """Initialize PATH_ROOT to the toplevel of the git repo"""
        fpath = subprocess.getoutput("git rev-parse --show-toplevel")
        if "fatal:" in fpath:
            fpath = pathlib.Path(__file__).parent.parent
        else:
            fpath = pathlib.Path(fpath)
        return fpath

    def _init_sys_plat(self):
        """Initialize SYS_PLAT to a pyboiler.platform.Platform enum"""
        from .platform import Platform

        return Platform.get()
