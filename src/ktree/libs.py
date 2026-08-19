"""Small geometry helpers used by the KTree implementations.

Most helpers work with axis-aligned intervals represented as ``(min, max)``
tuples and points represented as sequences of coordinates.
"""

import collections.abc
import functools
import math
import operator
import typing

SupportNumber = typing.TypeVar("SupportNumber", int, float)


def check_axis_intersect(that: tuple[float, float], z: float) -> bool:
    """Check whether ``z`` lies inside a single axis interval.

    Args:
        that: An interval ``(min, max)`` along one axis.
        z: A coordinate value on the same axis.

    Returns:
        ``True`` if ``min <= z <= max``.
    """
    x, y = that
    return y >= z >= x


def is_collision(
    that: collections.abc.Sequence[tuple[float, float]],
    other: collections.abc.Sequence[float],
) -> bool:
    """Check whether a point lies inside every axis interval of a box.

    Args:
        that: A list of ``(min, max)`` intervals, one per dimension.
        other: A point with one coordinate per dimension.

    Returns:
        ``True`` if the point is inside the box on every axis.

    Raises:
        ValueError: If ``that`` and ``other`` have different lengths.
    """
    if len(that) != len(other):
        raise ValueError("Invalid arguments, different length of values")

    return all([check_axis_intersect(t, z) for t, z in zip(that, other)])


def calc_distance_euclidean(x: SupportNumber, y: SupportNumber) -> float:
    """Return half of the absolute distance between two numbers.

    Args:
        x: First coordinate.
        y: Second coordinate.

    Returns:
        ``abs(y - x) / 2``.
    """
    return math.fabs(y - x) / 2


def calcdist(axis: tuple[SupportNumber, SupportNumber]) -> float:
    """Return the absolute length of an interval.

    Args:
        axis: An interval ``(min, max)``.

    Returns:
        The absolute distance ``max - min``.
    """
    return math.sqrt(functools.reduce(operator.sub, axis) ** 2)


def middledist(axis: tuple[SupportNumber, SupportNumber]) -> float:
    """Return the midpoint of an interval.

    Args:
        axis: An interval ``(min, max)``.

    Returns:
        The midpoint coordinate ``min + length / 2``.
    """
    dist = calcdist(axis) / 2

    return axis[0] + dist


def middleaxis(
    axis: tuple[SupportNumber, SupportNumber],
) -> tuple[tuple[float, float], tuple[float, float]]:
    """Split an interval into two equal halves.

    Args:
        axis: An interval ``(min, max)``.

    Returns:
        A pair of intervals ``((min, midpoint), (midpoint, max))``.
    """
    dist = calcdist(axis) / 2
    middle = axis[0] + dist

    return (axis[0], middle), (middle, axis[1])
