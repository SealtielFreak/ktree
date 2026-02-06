import functools
import math
import operator
import typing

SupportNumber = typing.TypeVar('SupportNumber', int, float)


def check_axis_intersect(that: typing.Tuple[SupportNumber, SupportNumber], z: SupportNumber):
    x, y = that
    return y >= z >= x


def is_collision(that: typing.List[typing.Tuple[SupportNumber, SupportNumber]],
                 other: typing.List[SupportNumber]) -> bool:
    if len(that) != len(other):
        raise ValueError("Invalid arguments, different length of values")

    return all([check_axis_intersect(t, z) for t, z in zip(that, other)])


def calc_distance_euclidean(x: SupportNumber, y: SupportNumber):
    return math.fabs(y - x) / 2


def calcdist(axis: typing.Tuple[SupportNumber, SupportNumber]):
    return math.sqrt(functools.reduce(operator.sub, axis) ** 2)


def middledist(axis: typing.Tuple[SupportNumber, SupportNumber]):
    dist = calcdist(axis) / 2

    return axis[0] + dist


def middleaxis(axis: typing.Tuple[SupportNumber, SupportNumber]):
    dist = calcdist(axis) / 2
    middle = axis[0] + dist

    return (axis[0], middle), (middle, axis[1])
