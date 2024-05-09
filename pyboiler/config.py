import pathlib
import subprocess


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
        self.PATH_ROOT = self.init_path_root()

    def init_path_root(self) -> pathlib.Path:
        """Initialize PATH_ROOT to the toplevel of the git repo"""
        fpath = subprocess.getoutput("git rev-parse --show-toplevel")
        if "fatal:" in fpath:
            fpath = pathlib.Path(__file__).parent.parent
        else:
            fpath = pathlib.Path(fpath)
        return fpath
