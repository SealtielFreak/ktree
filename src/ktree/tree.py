"""Abstract interfaces shared by the KTree containers.

This module defines the contracts that every cluster node and tree container
must satisfy. Implementations live in :mod:`ktree.kdtree` and
:mod:`ktree.ntree`.
"""

import abc
import collections.abc
import typing

T = typing.TypeVar("T")


class ClusterInterface(abc.ABC, typing.Generic[T]):
    """Abstract base class for a cluster that holds spatially grouped points.

    A cluster knows its geometric ``shape`` (e.g., an axis-aligned bounding
    box) and stores the ``data`` points that fall inside that shape.
    """

    @abc.abstractmethod
    def clear(self) -> None:
        """Remove every stored point from the cluster."""

    @abc.abstractmethod
    def append(self, node: T) -> None:
        """Add a new point to the cluster.

        Args:
            node: The point to store. The concrete type depends on the tree
                implementation.
        """

    @property
    @abc.abstractmethod
    def data(self) -> collections.abc.Iterable[T]:
        """The points stored in this cluster."""

    @property
    @abc.abstractmethod
    def shape(self) -> typing.Any:
        """The geometric bounds of this cluster."""

    @abc.abstractmethod
    def __len__(self) -> int:
        """Return the number of stored points."""

    @abc.abstractmethod
    def __hash__(self) -> int:
        """Return a hash based on the cluster shape."""

    @abc.abstractmethod
    def __iter__(self) -> collections.abc.Iterator[T]:
        """Yield the stored points."""

    @abc.abstractmethod
    def __repr__(self) -> str:
        """Return a concise, human-readable representation."""


class TreeContainerInterface(abc.ABC, typing.Generic[T]):
    """Abstract base class for a tree that partitions spatial points.

    A tree container accepts points via :meth:`insert`, produces a sorted
    collection of :class:`ClusterInterface` instances via :meth:`sort`, and
    can be cleared with :meth:`clear`.
    """

    @abc.abstractmethod
    def insert(self, data: T) -> None:
        """Insert a point into the tree.

        Args:
            data: The point to insert. The concrete type depends on the tree
                implementation.
        """

    @abc.abstractmethod
    def sort(self) -> collections.abc.Sequence[ClusterInterface[T]]:
        """Sort the inserted points into clusters and return those clusters.

        Returns:
            A sequence of cluster nodes produced by the partitioning algorithm.
        """

    @abc.abstractmethod
    def clear(self) -> None:
        """Remove all inserted points and reset the tree."""

    @abc.abstractmethod
    def __iter__(self) -> collections.abc.Iterator[ClusterInterface[T]]:
        """Yield the clusters produced by the tree."""
