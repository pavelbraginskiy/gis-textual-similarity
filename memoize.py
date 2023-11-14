import functools
from typing import Callable, TypeAlias

point: TypeAlias = [float]
trajectory: TypeAlias = [point]

def memoize(func):
    @functools.wraps(func)
    def ret(*args):
        cachable_args = tuple(tuple(tuple(j) if isinstance(j, list) else j for j in i) if isinstance(i, list) else i for i in args)
        if cachable_args in ret.cache:
            return ret.cache[cachable_args]
        result = func(*args)
        ret.cache[cachable_args] = result
        return result
    ret.cache = {}
    return ret
