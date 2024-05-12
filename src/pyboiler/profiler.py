"""Wrapper for python.profile"""

import cProfile
import pstats

from .config import config


def run(cmd: str, locals: dict, globals: dict, builtins=True):
    prof = cProfile.Profile(builtins=builtins)
    prof.runctx(cmd, locals, globals)
    prof.dump_stats(str(config().FILEPATH_PROFILE))


def get():
    if config().FILEPATH_PROFILE.exists():
        ps = pstats.Stats()
        ps.load_stats(str(config().FILEPATH_PROFILE))
        return ps
    return None


def view(ps):
    if not isinstance(ps, pstats.Stats):
        return
    ps.strip_dirs().sort_stats("cumtime").print_stats()
