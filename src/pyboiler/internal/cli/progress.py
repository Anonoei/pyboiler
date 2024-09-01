from ..color.colors import FG, BG, ST

import time

def _fmt(percent: float, msg: str = None, rtime: float=None, etime: float=None, width: int=40, fill="#", empty="."):
        count_f = int(width * percent)
        count_e = width - count_f
        fmt = "[" + (fill * count_f) + (empty * count_e) + "] "
        fmt += f"{percent * 100:.2f}% "
        if rtime is not None and etime is not None:
            fmt += f"{rtime:.2f}/{etime:.2f}s"
        elif rtime is not None:
            fmt += f"{rtime:.2f}s"
        elif etime is not None:
            fmt += f"{etime:.2f}s eta"
        fmt += f": {msg}"
        return fmt

def _cfmt(percent: float, msg: str = None, rtime: float=None, etime: float=None, width: int=40):
        count_f = int(width * percent)
        count_e = width - count_f
        msg_f = msg[0:count_f]
        if len(msg_f) < count_f:
            msg_f = msg_f + ("." * (count_f - len(msg_f)))
        msg_e = msg[count_f:]
        if len(msg_e) > count_e:
            msg_e = msg_e[:count_e]
        else:
            msg_e = msg_e + ("." * (count_e - len(msg_e)))

        fmt = "["
        fmt += ST.RESET.code() + BG.WHITE.code() + FG.BLACK.code()
        fmt += msg_f + ST.RESET.code()
        fmt += BG.BLACK.code() + FG.WHITE.code()
        fmt += msg_e + ST.RESET.code()
        fmt += f"] {percent* 100:.2f}% "
        if rtime is not None and etime is not None:
            fmt += f"{rtime:.2f}/{etime:.2f}s"
        elif rtime is not None:
            fmt += f"{rtime:.2f}s"
        elif etime is not None:
            fmt += f"{etime:.2f}s eta"
        return fmt

class _Progress:
    @staticmethod
    def _fmt(percent: float, msg: str = None, rtime=None, etime=None, width: int=40):
        return " " + _fmt(percent, msg, rtime=rtime, etime=etime, width=width)

class _ProgressColored(_Progress):
    @staticmethod
    def _fmt(percent: float, msg: str = None, rtime=None, etime=None, width: int=40):
        return " " + _cfmt(percent, msg, rtime=rtime, etime=etime, width=width)

class Simple(_Progress):
    def bar(self, percent, message, rt=None, et=None):
        print(type(self)._fmt(percent, message, rt, et), end="\r")

class SimpleColored(_ProgressColored):
    def bar(self, percent, message, rt=None, et=None):
        print(type(self)._fmt(percent, message, rt, et), end="\r")

class Context(_Progress):
    def __init__(self, name=None, timer=True, etc=True):
        self.timer = timer
        self.etc = etc

        self._cache = {}
        if name is not None:
            self._cache["name"] = name

    def __enter__(self, name=""):
        self._cache = {
            "name": self._cache.get("name", name),
            "percent": 0,
            "start": time.perf_counter(),
            "last": None,
            "dur": None,
            "est": None,
            "itr": 0,
            "message": ""
        }
        return self

    def __exit__(self, *args, **kwargs):
        self.show(1.0)
        print()
        self._cache = {}

    def update(self, percent, message=""):
        self._cache["percent"] = percent
        self._cache["message"] = message

    def show(self, percent=None, message=None):
        if percent is not None:
            self._cache["percent"] = percent
        if message is not None:
            self._cache["message"] = message
        self._cache["itr"] += 1

        if self.timer is True:
            cur = time.perf_counter()
            if self._cache["last"] is not None:
                if cur - self._cache["last"] < 0.2:
                    return
            self._cache["last"] = cur
            if self.etc is True:
                self._cache["dur"] = self._cache["last"] - self._cache["start"]

                perc_per_itr = self._cache["percent"] / self._cache["itr"]
                time_per_itr = self._cache["dur"] / self._cache["itr"]
                est_itr_tot = 1 / perc_per_itr
                self._cache["est"] = est_itr_tot * time_per_itr
        print(type(self)._fmt(self._cache["percent"], self._cache["message"], self._cache["dur"], self._cache["est"]), end="\r")


class ContextColored(_ProgressColored, Context):
    pass
