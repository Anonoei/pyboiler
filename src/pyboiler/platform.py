"""Platform specific helpers"""

import os
import sys
from enum import Enum, auto


class Platform(Enum):
    Windows = auto()
    Linux = auto()
    Mac = auto()

    @staticmethod
    def get():
        if sys.platform.startswith("win"):
            return Platform.Windows
        elif sys.platform == "darwin":
            return Platform.Mac
        return Platform.Linux


def clear():
    """OS independent clear console"""
    from .config import config

    if config().SYS_PLAT is Platform.Windows:
        os.system("cls")
    else:
        os.system("clear")
