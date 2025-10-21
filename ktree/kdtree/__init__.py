import collections
import typing

from ktree.libs import SupportNumber, middleaxis, middledist
from ktree.tree import TreeContainerInterface, ClusterInterface


class KDCluster(ClusterInterface, typing.Generic[SupportNumber]):
    def __init__(self, level: int, axis: typing.List[typing.Tuple[float, float]],
                 data: typing.List[typing.Tuple[float, float]]):
        self.__level = level
        self.__axis: typing.List[typing.Tuple[float, float]] = axis
        self.__data: typing.List[typing.Tuple[float, float]] = data

    @property
    def level(self):
        return self.__level

    @property
    def axis(self):
        return self.__axis

    @property
    def data(self):
        return self.__data

    def append(self, data):
        self.__data.append(data)

    def clear(self):
        self.__data = []

    def __len__(self):
        return len(self.__data)

    def __hash__(self):
        return hash(tuple(self.__axis))

    def __iter__(self):
        return iter(self.__data)

    def __repr__(self):
        return f"Cluster(axis={self.axis}, size={len(self)})"


class KDTree(TreeContainerInterface, typing.Generic[SupportNumber]):
    def __init__(self, axis: typing.List[typing.Tuple[SupportNumber, SupportNumber]], min_size: int):
        self.__min_size = min_size
        self.__n_axis = len(axis[0])
        self.__axis: typing.List[typing.Tuple[SupportNumber, SupportNumber]] = axis
        self.__items: typing.Deque[typing.List[SupportNumber]] = collections.deque()
        self.__clusters: typing.List[KDCluster[SupportNumber]] = []

    def insert(self, data):
        self.__items.append(data)

    def sort(self):
        def recursive_sorting(data, axis, n, level=0):
            if len(data) <= self.__min_size:
                return self.__clusters.append(KDCluster(level, axis, data))

            mid = middledist(axis[0])
            left, right = [], []

            for p in data:
                if p[n] < mid:
                    left.append(p)
                else:
                    right.append(p)

            n = (n + 1) % len(data[0])

            if len(data) <= self.__min_size and (len(right) == len(data) or len(left) == len(data)):
                return self.__clusters.append(KDCluster(level, axis, data))

            l_axis, r_axis = middleaxis(axis[0])
            level += 1

            if len(right) == 0:
                return recursive_sorting(left, [*axis[1:], l_axis], n, level)
            elif len(left) == 0:
                return recursive_sorting(right, [*axis[1:], r_axis], n, level)
            else:
                return (
                    recursive_sorting(left, [*axis[1:], l_axis], n, level),
                    recursive_sorting(right, [*axis[1:], r_axis], n, level)
                )

        self.__clusters = []

        recursive_sorting(self.__items, self.__axis, 0)

        return self.__clusters

    def clear(self):
        self.__items.clear()

    def __iter__(self):
        return iter(self.__clusters)
