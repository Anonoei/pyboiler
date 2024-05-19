"""Generic semantic versioning class/implementation"""

from typing import Any


class Version:
    __slots__ = ("release", "major", "minor")

    def __init__(self, release: int, major: int, minor: int):
        self.release = release
        self.major = major
        self.minor = minor

    def __str__(self) -> str:
        return f"{self.release}.{self.major}.{self.minor}"

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {str(self)}>"

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            raise NotImplementedError(f"Cannot check if {type(self)} == {type(other)}")
        if self.release == other.release:
            if self.major == other.major:
                if self.minor == other.minor:
                    return True
        return False

    def __lt__(self, other) -> bool:
        if not isinstance(other, type(self)):
            raise NotImplementedError(f"Cannot check if {type(self)} < {type(other)}")
        checks = list(self.__slots__)
        for idx, check in enumerate(checks):
            s_check = getattr(self, check)
            o_check = getattr(other, check)
            if s_check < o_check:
                return True
        return False

    def __gt__(self, other) -> bool:
        if not isinstance(other, type(self)):
            raise NotImplementedError(f"Cannot check if {type(self)} < {type(other)}")
        checks = list(self.__slots__)
        for idx, check in enumerate(checks):
            s_check = getattr(self, check)
            o_check = getattr(other, check)
            if s_check > o_check:
                return True
        return False

    def __le__(self, other) -> bool:
        if self == other:
            return True
        return self < other

    def __ge__(self, other) -> bool:
        if self == other:
            return True
        return self > other
