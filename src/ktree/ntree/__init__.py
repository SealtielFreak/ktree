"""NTree implementation.

An NTree recursively partitions N-dimensional space. With two dimensions it
behaves like a :term:`QuadTree`; with three dimensions like an
:term:`Octree`. The module provides both a static variant with a fixed root
bounding box and a dynamic variant that learns the bounding box from the data.
"""

from __future__ import annotations

import collections
import typing

import numpy as np

from ktree.libs import SupportNumber, calc_distance_euclidean, is_collision
from ktree.tree import ClusterInterface, TreeContainerInterface

M = typing.TypeVar("M", bound=list[tuple[float, float]])


class NClusterNode(ClusterInterface, typing.Generic[M]):
    """A leaf cluster inside an NTree.

    A cluster stores the points whose coordinates fall inside its geometric
    ``shape``.

    Attributes:
        shape: Bounding box as a list of ``(min, max)`` intervals.
        data: The points contained in this cluster.
    """

    def __init__(self, shape: M, data: list | collections.deque):
        """Create a new leaf cluster.

        Args:
            shape: Bounding box of the cluster.
            data: Points stored in the cluster.
        """
        self.__shape: M = shape
        self.__data: list | collections.deque = data

    @property
    def data(self) -> list | collections.deque:
        """Points stored in this cluster."""
        return self.__data

    @property
    def shape(self) -> M:
        """Bounding box of this cluster."""
        return self.__shape

    def clear(self) -> None:
        """Remove all stored points."""
        self.__data = []

    def append(self, data: typing.Any) -> None:
        """Add a point to this cluster.

        Args:
            data: The point to store.
        """
        self.__data.append(data)

    def is_collide(self, node: collections.abc.Sequence[float]) -> bool:
        """Check whether a point falls inside this cluster's bounding box.

        Args:
            node: A point with one coordinate per dimension.

        Returns:
            ``True`` if the point lies inside the cluster shape.
        """
        return is_collision(typing.cast(list[tuple[float, float]], self.shape), node)

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self) -> typing.Iterator[typing.Any]:
        return iter(self.data)

    def __hash__(self) -> int:
        return hash(tuple(self.shape))

    def __repr__(self) -> str:
        return f"Cluster(axis={self.shape})"


class NTreeStatic(TreeContainerInterface, typing.Generic[M]):
    """N-ary tree with a fixed root bounding box.

    ``NTreeStatic`` is the N-dimensional generalization of the classic quadtree
    and octree. Instead of splitting a single axis per level, every axis of the
    current bounding box is bisected simultaneously at each subdivision step,
    producing ``2^N`` child regions per parent:

    - **2D** — each region is split into 4 quadrants (a QuadTree, Finkel &
      Bentley, 1974).
    - **3D** — each region is split into 8 octants (an Octree, Globus, 1991;
      Madeira et al., 2011).
    - **N-D** — the same rule produces ``2^N`` sub-regions, so the structure
      works for arbitrary dimensionality, not just 2 or 3.

    The root bounding box is fixed at construction time and every inserted
    point must fall inside it. ``limit_divisions`` controls the maximum
    recursion depth.

    Example:
        >>> tree = NTreeStatic([(0.0, 1.0), (0.0, 1.0)], limit_divisions=2)
        >>> tree.insert([0.1, 0.1])
        >>> len(tree.sort()) > 0
        True

    Args:
        axis: Root bounding box as a list of ``(min, max)`` intervals, one per
            dimension.
        limit_divisions: Maximum number of recursive subdivisions. Must be
            ``>= -1``.
    """

    def __init__(self, axis: M, limit_divisions: int = 1):
        if limit_divisions < -1:
            raise ValueError("Limit divisions cannot be less than one.")

        self.__children: dict[int, NTreeStatic[M]] = {}
        self.__node: NClusterNode = NClusterNode(shape=axis, data=[])
        self.__shape: M = axis
        self.__limit_divisions: int = limit_divisions

    def __hash__(self) -> int:
        return hash(self.__node)

    @property
    def shape(self) -> M:
        """Root bounding box as a list of ``(min, max)`` intervals."""
        return self.__shape

    @property
    def children(self) -> dict[int, NTreeStatic[M]]:
        """Child subtrees indexed by hash."""
        return self.__children

    @property
    def node(self) -> NClusterNode:
        """The root cluster node."""
        return self.__node

    @property
    def is_parent(self) -> bool:
        """``True`` if this node has at least one child subtree."""
        return len(self.children) != 0

    def insert(self, data: list[SupportNumber]) -> None:
        """Insert a point into the tree.

        Args:
            data: A point with one coordinate per dimension. Each coordinate
                must be inside the root bounding box.

        Raises:
            ValueError: If the point does not collide with the target leaf
                cluster.
        """
        self.__insert_recursive(data)

    def sort(self) -> list[NClusterNode]:
        """Return the populated leaf clusters.

        Returns:
            A list of :class:`NClusterNode` leaf clusters that contain at least
            one inserted point.
        """
        return self.__iter_child_recursive()

    def __iter__(self) -> typing.Iterator[NClusterNode]:
        """Yield the populated leaf clusters."""
        return iter(self.__iter_child_recursive())

    def clear(self) -> None:
        """Reset the tree, removing all inserted points and child subtrees."""
        self.__node = NClusterNode(shape=self.__shape, data=[])

    def __insert_recursive(self, verx: list[SupportNumber]) -> NTreeStatic[M]:
        def create_static_vertex(v):
            root_axis = collections.deque()

            for axis, c in zip(self.shape, v):
                x, y = axis
                d = calc_distance_euclidean(x, y)

                if x <= c <= (x + d):
                    root_axis.append((x, x + d))
                else:
                    root_axis.append((x + d, y))

            axis = list(root_axis)

            return axis

        shape = create_static_vertex(verx)

        tree = NTreeStatic(shape, self.__limit_divisions - 1)
        tree_key = hash(tree)

        if tree_key in self.__children:
            tree = self.__children[tree_key]
        else:
            self.__children[tree_key] = tree

        if self.__limit_divisions > 0:
            tree.insert(verx)
            return tree
        else:
            if not tree.node.is_collide(verx):
                raise ValueError(f"Vertex no collide: {tree.node} {verx}")

            tree.node.append(verx)

        return tree

    def __iter_child_recursive(self) -> list[NClusterNode]:
        def get_iter_child(root, nodes=None):
            if nodes is None:
                nodes = []

            for _, child in root.children.items():
                if child.is_parent:
                    get_iter_child(child, nodes)
                else:
                    if len(child.node) > 0:
                        nodes.append(child.node)

            return nodes

        return get_iter_child(self, [])


class NTreeDynamic(TreeContainerInterface, typing.Generic[M]):
    """N-ary tree that learns its bounding box from the inserted data.

    ``NTreeDynamic`` uses the same N-ary partitioning structure as
    :class:`NTreeStatic`: every axis of the current bounding box is bisected at
    each subdivision step, forming ``2^N`` child regions. In 2D it behaves like
    a QuadTree, in 3D like an Octree, and in general N-D it supports arbitrary
    dimensionality.

    Unlike :class:`NTreeStatic`, the root ``shape`` is not provided by the
    caller. Instead, it is computed during :meth:`sort` from the minimum and
    maximum coordinate values of the inserted points on every axis, which makes
    the tree self-configuring when the search space is unknown in advance.

    Example:
        >>> tree = NTreeDynamic(limit_divisions=2)
        >>> tree.insert([0.1, 0.1])
        >>> tree.insert([0.9, 0.9])
        >>> len(tree.sort()) > 0
        True

    Args:
        limit_divisions: Maximum number of recursive subdivisions. Must be
            ``>= -1``.
        shape: Optional initial bounding box. If omitted, it is computed during
            the first :meth:`sort` call.
        limit_size: Unused placeholder for future size-based splitting.
    """

    def __init__(
        self,
        limit_divisions: int = 1,
        shape: M | None = None,
        limit_size: int | None = None,
    ):
        if limit_divisions < -1:
            raise ValueError("Limit divisions cannot be less than one.")

        self.__children: dict[int, NTreeDynamic[M]] = {}

        # self.__node: typing.Optional[NClusterNode[SupportNumber]] = None
        self.__shape: M = typing.cast(M, shape)

        self.__limit_divisions: int = limit_divisions
        self.__data: collections.deque[M] = collections.deque()
        self.__limit_size = limit_size

    def __del__(self):
        """Destructor currently delegates to :meth:`clear`."""
        self.clear()

    def __hash__(self) -> int:
        return hash(tuple(self.shape))

    @property
    def limit_size(self) -> int | None:
        """Optional size limit placeholder."""
        return self.__limit_size

    @property
    def shape(self) -> M:
        """Current bounding box as a list of ``(min, max)`` intervals."""
        return self.__shape

    @property
    def children(self) -> dict[int, NTreeDynamic[M]]:
        """Child subtrees indexed by hash."""
        return self.__children

    @property
    def is_parent(self) -> bool:
        """``True`` if this node has at least one child subtree."""
        return len(self.children) != 0

    def insert(self, data: M) -> None:
        """Insert a point into the tree.

        Args:
            data: A point with one coordinate per dimension.
        """
        self.__data.append(data)

    def sort(self) -> list[NClusterNode]:
        """Compute the bounding box, partition the points, and return leaves.

        Returns:
            A list of populated :class:`NClusterNode` leaf clusters.
        """
        sorted_elements: list = []

        self.__children = {}
        self.__recursive_sorting(sorted_elements)

        return sorted_elements

    def __iter__(self) -> typing.Iterator[NClusterNode]:
        """Yield the populated leaf clusters."""
        return iter(self.sort())

    def clear(self) -> None:
        """Reset the tree.

        Note:
            This implementation clears child subtrees but currently keeps the
            inserted data in memory. Call :meth:`sort` to re-partition from
            scratch.
        """

    def __len__(self) -> int:
        return len(self.__data)

    def __recursive_sorting(self, sorted_data: list) -> None:
        def calc_subshape(_data, _shape):
            root_axis = collections.deque()

            for (x, y), c in zip(_shape, _data):
                dist = calc_distance_euclidean(x, y)

                if x <= c <= (x + dist):
                    root_axis.append((x, x + dist))
                else:
                    root_axis.append((x + dist, y))

            return list(root_axis)

        data = np.array(self.__data)
        axis = len(data[0])
        shape = (
            np.array([(min(data[:, n]), max(data[:, n])) for n in range(axis)])
            .astype(float)
            .tolist()
        )

        self.__shape = shape

        if self.__limit_divisions > 0:
            for d in self.__data:
                tree: NTreeDynamic = NTreeDynamic(
                    self.__limit_divisions - 1,
                    shape=calc_subshape(d, shape),
                    limit_size=self.__limit_size,
                )
                tree_key = hash(tree)

                if tree_key in self.__children:
                    tree = self.__children[tree_key]
                else:
                    self.__children[tree_key] = tree

                tree.insert(d)

            for tree in self.__children.values():
                tree.__recursive_sorting(sorted_data)
        else:
            sorted_data.append(
                NClusterNode(shape=self.shape, data=collections.deque(self.__data))
            )
