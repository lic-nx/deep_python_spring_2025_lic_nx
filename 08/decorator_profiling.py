"""задание 3"""

import cProfile
import pstats
from functools import wraps


def profile_deco(func):
    """Декоратор для профилирования"""
    profiler = cProfile.Profile()

    def print_stat():
        stats = pstats.Stats(profiler)
        stats.sort_stats("cumulative")
        stats.print_stats()

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = profiler.runcall(func, *args, **kwargs)
        return result

    wrapper.print_stat = print_stat
    return wrapper


@profile_deco
def add(a, b):
    """просто сложение"""
    return a + b


@profile_deco
def sub(a, b):
    """просто вычитаниие"""
    return a - b


add(1, 2)
add(4, 5)
sub(4, 5)
add.print_stat()
sub.print_stat()
