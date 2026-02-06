import collections
import typing

import numpy as np

from ktree.libs import is_collision, calc_distance_euclidean, SupportNumber
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
    def __init__(self, axis: M, limit_divisions: int = 1):
        """
        NTree is the main container for sorting elements.

        :param axis: Establishes the main axes where the elements will be ordered.
        :param limit_divisions: Maximum number of divisions.
        """
        if limit_divisions < -1:
            raise ValueError("Limit divisions cannot be less than one.")

        self.__children: typing.Dict[int, NTreeStatic[M]] = {}
        self.__node: NClusterNode = NClusterNode(shape=axis, data=[])
        self.__shape: M = axis
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
        self.__insert_recursive(data)

    def sort(self) -> list:
        """
        This method returns the elements already sorted from sorted.
        :return:
        """
        return self.__iter_child_recursive()

    def __iter__(self):
        """
        Iterate the already sorted elements of sorted ones.
        :return:
        """
        return iter(self.__iter_child_recursive())

    def clear(self):
        self.__node = NClusterNode(shape=self.__shape, data=[])

    def __insert_recursive(self, verx: typing.List[SupportNumber]):
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
            return tree.insert(verx)
        else:
            if not tree.node.is_collide(verx):
                raise ValueError(f"Vertex no collide: {tree.node} {verx}")

            tree.node.append(verx)

        return tree

    def __iter_child_recursive(self):
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
    def __init__(self, limit_divisions: int = 1, shape=None):
        """
        NTreeDynamic is the main container for sorting elements.

        :param shape: Establishes the main axes where the elements will be ordered.
        :param limit_divisions: Maximum number of divisions.
        """
        if limit_divisions < -1:
            raise ValueError("Limit divisions cannot be less than one.")

        self.__children: typing.Dict[int, NTreeDynamic[M]] = {}

        # self.__node: typing.Optional[NClusterNode[SupportNumber]] = None
        self.__shape: M = shape

        self.__limit_divisions: int = limit_divisions
        self.__data: typing.Deque[M] = collections.deque()

    def __del__(self):
        self.clear()

    def __hash__(self):
        return hash(tuple(self.__shape))

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
        self.__data.append(data)

    def sort(self) -> list:
        """
        This method returns the elements already sorted from sorted.
        :return:
        """

        sorted_elements: list = []

        self.__children = {}
        self.__recursive_sorting(sorted_elements)

        return sorted_elements

    def __iter__(self):
        """
        Iterate the already sorted elements of sorted ones.
        :return:
        """
        return iter(self.sort())

    def clear(self):
        self.__children.clear()
        self.__data.clear()

    def __recursive_sorting(self, sorted_data: list):
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
        shape = np.array([(min(data[:, n]), max(data[:, n])) for n in range(axis)]).astype(float).tolist()

        self.__shape = shape

        if self.__limit_divisions > 0:
            for d in self.__data:
                tree: NTreeDynamic = NTreeDynamic(self.__limit_divisions - 1, shape=calc_subshape(d, shape))
                tree_key = hash(tree)

                if tree_key in self.__children:
                    tree = self.__children[tree_key]
                else:
                    self.__children[tree_key] = tree

                tree.insert(d)

            for tree in self.__children.values():
                tree.__recursive_sorting(sorted_data)
        else:
            sorted_data.append(NClusterNode(
                shape=self.shape,
                data=collections.deque(self.__data)
            ))
