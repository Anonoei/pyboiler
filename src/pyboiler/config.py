import pathlib
import subprocess

from .imports import get_locals


class config:
    """Global configuration, not intended to be modified by users"""

    __instance = None

    # define singleton attributes
    PATH_ROOT: pathlib.Path = None  # type: ignore

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            cls.__instance.init()
        return cls.__instance

    def init(self):
        """Initialize config attributes"""
        self.PATH_ROOT = self._init_path_root()
        self.PATH_LOGS = self.PATH_ROOT / "logs"
        self.PATH_PROFILE = self.PATH_ROOT / "profiler.stats"

        self.SERIAL = "xml"  # one of "xml" or "json"

        self.PATH_SETTINGS = self.PATH_ROOT / f"settings.{self.SERIAL}"
        self.SYS_PLAT = self._init_sys_plat()

        self.SENTINEL = object()

    def json(self) -> dict:
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
        from .platform import Platform

        return Platform.get()
