"""KDTree implementation.

A KDTree recursively splits a set of points along alternating axes using the
midpoint of the current bounding interval. Each split produces a
:class:`KDCluster` containing the points that fall into that sub-region.
"""

import collections
import typing

from ktree.libs import SupportNumber, middleaxis, middledist
from ktree.tree import ClusterInterface, TreeContainerInterface


class KDCluster(ClusterInterface, typing.Generic[SupportNumber]):
    """A cluster produced by the KDTree partitioning process.

    Attributes:
        level: The recursion depth at which this cluster was created.
        shape: The axis-aligned bounding box for this cluster.
        data: The points stored in this cluster.
    """

    def __init__(
        self,
        level: int,
        axis: list[tuple[float, float]],
        data: list[tuple[float, float]],
    ):
        """Create a new KDTree cluster.

        Args:
            level: Recursion depth (0 for the root region).
            axis: Bounding box as a list of ``(min, max)`` intervals, one per
                dimension.
            data: Points stored in this cluster.
        """
        self.__level = level
        self.__axis: list[tuple[float, float]] = axis
        self.__data: list[tuple[float, float]] = data

    @property
    def level(self) -> int:
        """Recursion depth of this cluster."""
        return self.__level

    @property
    def shape(self) -> list[tuple[float, float]]:
        """Bounding box of this cluster."""
        return self.__axis

    @property
    def data(self) -> list[tuple[float, float]]:
        """Points stored in this cluster."""
        return self.__data

    def append(self, data: tuple[float, float]) -> None:
        """Add a point to this cluster.

        Args:
            data: The point to append.
        """
        self.__data.append(data)

    def clear(self) -> None:
        """Remove all points from this cluster."""
        self.__data = []

    def __len__(self) -> int:
        return len(self.data)

    def __hash__(self) -> int:
        return hash(tuple(self.__axis))

    def __iter__(self) -> typing.Iterator[tuple[float, float]]:
        return iter(self.data)

    def __repr__(self) -> str:
        return f"Cluster(axis={self.shape}, level={self.level})"


class KDTree(TreeContainerInterface, typing.Generic[SupportNumber]):
    """Recursive axis-aligned K-dimensional tree.

    Points are inserted and later partitioned by calling :meth:`sort`. The
    splitting dimension cycles through each axis at every recursion level.

    Example:
        >>> tree = KDTree([(-5, 5), (-5, 5)])
        >>> tree.insert([1.0, 2.0])
        >>> tree.insert([-2.0, -1.0])
        >>> clusters = tree.sort()
        >>> len(clusters) > 0
        True

    Args:
        axis: Initial bounding box as a list of ``(min, max)`` intervals, one
            per dimension.
    """

    def __init__(self, axis: list[tuple[SupportNumber, SupportNumber]]):
        self.__n_axis = len(axis[0])
        self.__axis: list[tuple[SupportNumber, SupportNumber]] = axis
        self.__items: collections.deque[list[SupportNumber]] = collections.deque()
        self.__clusters: list[KDCluster[SupportNumber]] = []

    def insert(self, data: list[SupportNumber]) -> None:
        """Insert a point into the tree.

        Args:
            data: A point with one coordinate per dimension.
        """
        self.__items.append(data)

    def sort(self) -> list[KDCluster[SupportNumber]]:
        """Partition the inserted points into clusters.

        Returns:
            A list of :class:`KDCluster` instances covering the partitioned
            regions.
        """

        def recursive_sorting(data, axis, n, clusters, level=0):
            if len(data) <= 1:
                return clusters.append(KDCluster(level, axis, data))

            clusters.append(KDCluster(level, axis, data))

            mid = middledist(axis[0])
            left, right = [], []

            for p in data:
                if p[n] < mid:
                    left.append(p)
                else:
                    right.append(p)

            n = (n + 1) % len(data[0])

            if len(data) <= 3 and (len(right) == len(data) or len(left) == len(data)):
                return clusters.append(KDCluster(level, axis, data))

            l_axis, r_axis = middleaxis(axis[0])
            level += 1

            if len(right) == 0:
                return recursive_sorting(left, [*axis[1:], l_axis], n, clusters, level)
            elif len(left) == 0:
                return recursive_sorting(right, [*axis[1:], r_axis], n, clusters, level)
            else:
                return (
                    recursive_sorting(left, [*axis[1:], l_axis], n, clusters, level),
                    recursive_sorting(right, [*axis[1:], r_axis], n, clusters, level),
                )

        self.__clusters = []

        recursive_sorting(self.__items, self.__axis, 0, self.__clusters)

        return self.__clusters

    def clear(self) -> None:
        """Remove all inserted points."""
        self.__items.clear()

    def __iter__(self) -> typing.Iterator[KDCluster[SupportNumber]]:
        return iter(self.__clusters)
