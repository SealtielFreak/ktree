import collections
import typing

import numpy as np

from ktree.libs import is_collision, calc_distance_euclidean
from ktree.tree import TreeContainerInterface, ClusterInterface

M = typing.TypeVar('M')


class NClusterNode(ClusterInterface):
    def __init__(self, shape: M, data: typing.List | typing.Deque):
        self.__shape: M = shape
        self.__data: typing.List | typing.Deque = data

    @property
    def data(self):
        return self.__data

    @property
    def shape(self):
        return self.__shape

    def clear(self):
        self.__data = []

    def append(self, data):
        self.__data.append(data)

    def is_collide(self, node):
        return is_collision(self.shape, node)

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    def __hash__(self):
        return hash(tuple(self.shape))

    def __repr__(self):
        return f"Cluster(axis={self.shape})"


class NTreeStatic(TreeContainerInterface, typing.Generic[M]):
    def __init__(self, limit_divisions: int = 1, shape=None):
        """
        NTree is the main container for sorting elements.

        :param axis: Establishes the main axes where the elements will be ordered.
        :param limit_divisions: Maximum number of divisions.
        """
        if limit_divisions < -1:
            raise ValueError("Limit divisions cannot be less than one.")

        self.raw_data: typing.Deque[M] | None = None
        self.__children: typing.Dict[int, NTreeStatic[M]] = {}
        self.__node: NClusterNode = NClusterNode(shape=shape, data=[])
        self.__shape = shape
        self.__limit_divisions: int = limit_divisions

    def __hash__(self):
        return hash(self.__node)

    @property
    def shape(self):
        return [*self.__shape]

    @property
    def children(self):
        return self.__children

    @property
    def node(self) -> NClusterNode:
        return self.__node

    @property
    def is_parent(self):
        return len(self.children) != 0

    def insert(self, data):
        if self.raw_data is None:
            self.raw_data = collections.deque()

        self.raw_data.append(data)

    def sort(self) -> list:
        """
        This method returns the elements already sorted from sorted.
        :return:
        """

        sorted_elements: list = []

        self.__children = {}
        self._recursive_sorting(sorted_elements)

        return sorted_elements

    def __iter__(self):
        """
        Iterate the already sorted elements of sorted ones.
        :return:
        """
        return iter(self.sort())

    def clear(self):
        self.__node = NClusterNode(shape=self.__shape, data=[])

    def _recursive_sorting(self, sorted_data: list):
        def calc_subshape(_data, _shape):
            root_axis = []

            for (x, y), c in zip(_shape, _data):
                dist = calc_distance_euclidean(x, y)

                if x <= c <= (x + dist):
                    root_axis.append((x, x + dist))
                else:
                    root_axis.append((x + dist, y))

            return root_axis

        data = np.array(self.raw_data)
        axis = len(data[0])
        shape = np.array([(min(data[:, n]), max(data[:, n])) for n in range(axis)])

        self.__shape = shape

        if self.__limit_divisions > 0:
            for d in self.raw_data:
                tree: NTreeStatic = NTreeStatic(self.__limit_divisions - 1, shape=calc_subshape(d, shape))
                tree_key = hash(tree)

                if tree_key in self.__children:
                    tree = self.__children[tree_key]
                else:
                    self.__children[tree_key] = tree

                tree.insert(d)

            for tree in self.__children.values():
                tree._recursive_sorting(sorted_data)
        else:
            sorted_data.append(NClusterNode(
                shape=self.shape,
                data=collections.deque(self.raw_data)
            ))

    def _iter_child_recursive(self):
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
    def __init__(self, limit_divisions: int = 1, shape=None, limit_size: int | None = None):
        """
        NTreeDynamic is the main container for sorting elements.

        :param shape: Establishes the main axes where the elements will be ordered.
        :param limit_divisions: Maximum number of divisions.
        """
        if limit_divisions < -1:
            raise ValueError("Limit divisions cannot be less than one.")

        self.raw_data: typing.Deque[M] | None = None

        self.__children: typing.Dict[int, NTreeDynamic[M]] = {}

        self.__shape: M = shape

        self.__limit_divisions: int = limit_divisions
        self.__limit_size = limit_size

    def __del__(self):
        self.clear()

    def __hash__(self):
        return hash(tuple(self.__shape))

    @property
    def limit_size(self):
        return self.__limit_size

    @property
    def shape(self):
        return [*self.__shape]

    @property
    def children(self):
        return self.__children

    @property
    def is_parent(self):
        return len(self.children) != 0

    def insert(self, data):
        if self.raw_data is None:
            self.raw_data = collections.deque()

        self.raw_data.append(data)

    def sort(self) -> list:
        """
        This method returns the elements already sorted from sorted.
        :return:
        """

        sorted_elements: list = []

        self.__children = {}
        self._recursive_sorting(sorted_elements)

        return sorted_elements

    def __iter__(self):
        """
        Iterate the already sorted elements of sorted ones.
        :return:
        """
        return iter(self.sort())

    def clear(self):
        """
        self.__children = {}
        self.__data = collections.deque()
        """

    def __len__(self):
        return len(self.raw_data)

    def _recursive_sorting(self, sorted_data: list):
        def calc_subshape(_data, _shape):
            root_axis = collections.deque()

            for (x, y), c in zip(_shape, _data):
                dist = calc_distance_euclidean(x, y)

                if x <= c <= (x + dist):
                    root_axis.append((x, x + dist))
                else:
                    root_axis.append((x + dist, y))

            return list(root_axis)

        data = np.array(self.raw_data)
        axis = len(data[0])
        shape = np.array([(min(data[:, n]), max(data[:, n])) for n in range(axis)]).astype(float).tolist()

        self.__shape = shape

        if self.__limit_divisions > 0:
            for d in self.raw_data:
                tree: NTreeDynamic = NTreeDynamic(self.__limit_divisions - 1, shape=calc_subshape(d, shape),
                                                  limit_size=self.__limit_size)
                tree_key = hash(tree)

                if tree_key in self.__children:
                    tree = self.__children[tree_key]
                else:
                    self.__children[tree_key] = tree

                tree.insert(d)

            for tree in self.__children.values():
                tree._recursive_sorting(sorted_data)
        else:
            sorted_data.append(NClusterNode(
                shape=self.shape,
                data=collections.deque(self.raw_data)
            ))


class NTreeMean(TreeContainerInterface, typing.Generic[M]):
    def __init__(self, limit_divisions: int = 1, shape=None):
        """
        NTreeDynamic is the main container for sorting elements.

        :param shape: Establishes the main axes where the elements will be ordered.
        :param limit_divisions: Maximum number of divisions.
        """
        if limit_divisions < -1:
            raise ValueError("Limit divisions cannot be less than one.")

        self.raw_data: typing.Deque[M] | None = None

        self.__children: typing.Dict[int, NTreeMean[M]] = {}
        self.__shape = shape
        self.__limit_divisions: int = limit_divisions

    def __del__(self):
        self.clear()

    def __hash__(self):
        return hash(tuple(self.__shape))

    @property
    def shape(self):
        if self.__shape:
            return [*self.__shape]

        return None

    @property
    def children(self):
        return self.__children

    @property
    def is_parent(self):
        return len(self.children) != 0

    def insert(self, data):
        if self.raw_data is None:
            self.raw_data = collections.deque()

        self.raw_data.append(data)

    def sort(self) -> list:
        """
        This method returns the elements already sorted from sorted.
        :return:
        """

        sorted_elements: list = []

        self.__children = {}
        self._recursive_sorting(sorted_elements)

        return sorted_elements

    def __iter__(self):
        """
        Iterate the already sorted elements of sorted ones.
        :return:
        """
        return iter(self.sort())

    def clear(self):
        """
        self.__children = {}
        self.__data = collections.deque()
        """

    def __len__(self):
        return len(self.raw_data)

    def _recursive_sorting(self, sorted_data: list):
        def calc_subshape(_data, _shape):
            root_axis = []

            for (x, m, y), c in zip(_shape, _data):
                if x <= c <= (x + m):
                    root_axis.append((x, x + m))
                else:
                    root_axis.append((x + m, y))

            return root_axis

        data = np.array(self.raw_data)
        axis = len(data[0])
        shape = np.array([(min(data[:, n]), np.mean(data[:, n]), max(data[:, n])) for n in range(axis)])

        self.__shape = shape

        if self.__limit_divisions > 0:
            for d in self.raw_data:
                tree: NTreeMean = NTreeMean(self.__limit_divisions - 1, shape=calc_subshape(d, shape))
                tree_key = hash(tree)

                if tree_key in self.__children:
                    tree = self.__children[tree_key]
                else:
                    self.__children[tree_key] = tree

                tree.insert(d)

            for tree in self.__children.values():
                tree._recursive_sorting(sorted_data)
        else:
            sorted_data.append(NClusterNode(
                shape=shape,
                data=collections.deque(self.raw_data)
            ))
