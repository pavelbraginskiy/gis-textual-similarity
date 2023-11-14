import itertools
import math
from typing import TypeAlias

import vectorize
from memoize import *

def dist(x: point, y: point) -> float:
    return math.sqrt(sum((a-b)**2 for a, b in zip(x, y, strict=True)))



def cpd(a: trajectory, b: trajectory) -> float:
    """
    Closes-Pair Distance
    """
    return min(dist(x, y) for x, y in itertools.product(a, b))


def spd(a: trajectory, b: trajectory) -> float:
    """
    Sum-of-Pairs Distance
    """
    return sum(dist(x, y) for x, y in zip(a, b))

'''

'''
@memoize
def dtw(a: trajectory, b: trajectory) -> float:
    """
    Dynamic Time-Warping Distance
    """

    if len(a) == 0 and len(b) == 0:
        return 0
    if len(a) == 0 or len(b) == 0:
        return math.inf

    a_rest = a[1:]
    b_rest = b[1:]

    return dist(a[0], b[0]) + min(
        dtw(a, b_rest),
        dtw(a_rest, b),
        dtw(a_rest, b_rest)
    )


@memoize
def lcss(a: trajectory, b: trajectory, epsilon: float, delta: float = math.inf) -> float:
    """
    Longest Common Subsequence
    :param a: Trajectory a
    :param b: Trajectory b
    :param epsilon: Maximum space shift for two points to be considered the same
    :param delta: Maximum time shift
    :return:
    """

    n = len(a)
    m = len(b)

    if n == 0 or m == 0:
        return 0

    a_rest = a[1:]
    b_rest = b[1:]

    if dist(a[0], b[0]) <= epsilon and abs(n - m) < delta:
        return 1 + lcss(a_rest, b_rest, epsilon, delta)

    return max(
        lcss(a_rest, b, epsilon, delta),
        lcss(a, b_rest, epsilon, delta)
    )


@memoize
def edr(a: trajectory, b: trajectory, epsilon: float) -> float:
    """
    Edit Distance on Real Sequence
    :param a: Trajectory a
    :param b: Trajectory b
    :param epsilon: Matching threshold for two points to be considered the same
    :return:
    """

    n = len(a)
    m = len(b)

    if m == 0:
        return n
    if n == 0:
        return m

    a_rest = a[1:]
    b_rest = b[1:]

    subcost = 0 if dist(a[0], b[0]) < epsilon else 1
    return min(
        edr(a_rest, b_rest, epsilon) + subcost,
        edr(a_rest, b, epsilon) + 1,
        edr(a, b_rest, epsilon) + 1
    )


@memoize
def erp(a: trajectory, b: trajectory, g: point = None):
    """
    Edit distance with real penalty
    :param a: Trajectory a
    :param b: Trajectory b
    :param g: A random point to compare points against. Probably doesnt need to be set.
    :return:
    """
    if g is None:
        g = [0] * vectorize.model.vector_size

    n = len(a)
    m = len(b)
    if m == 0:
        return sum(dist(i, g) for i in a)
    if n == 0:
        return sum(dist(i, g) for i in b)

    a_rest = a[1:]
    b_rest = b[1:]

    return min(
        erp(a_rest, b_rest, g) + dist(a[0], b[0]),
        erp(a_rest, b, g) + dist(a[0], g),
        erp(a, b_rest, g) + dist(b[0], g)
    )