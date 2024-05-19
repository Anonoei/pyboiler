import functools
import time
from typing import Any, Callable

from .logger import Level, Logger

# def example(decor_args, or_multiple) -> Callable[..., Any]:
#     def decorator(func: Callable[..., Any]):
#         @functools.wraps(func)
#         def wrapper(*args, **kwargs) -> Any:
#             # stuff before func
#             func(*args, **kwargs)
#             # stuff after func
#         return wrapper
#     return decorator


def benchmark(itter: int = 1):
    def decorator(func: Callable[..., Any]):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            duration = time.perf_counter()
            for _ in range(0, itter):
                func(*args, **kwargs)
            duration = time.perf_counter() - duration

        return wrapper

    return decorator


def with_logging(log: Logger):

    def decorator(func: Callable[..., Any]):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs, log=log)

        return wrapper

    return decorator
