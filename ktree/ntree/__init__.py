import collections
import typing

import numpy as np

from ktree.libs import is_collision, distance, SupportNumber
from ktree.tree import TreeContainerInterface, ClusterInterface


class NClusterNode(ClusterInterface, typing.Generic[SupportNumber]):
    def __init__(self, axis: typing.List[typing.Tuple[SupportNumber, SupportNumber]], data: typing.List):
        self.__axis: typing.List[typing.Tuple[SupportNumber, SupportNumber]] = axis
        self.__data: typing.List = data

    @property
    def data(self):
        return self.__data

    @property
    def axis(self):
        return self.__axis

    def clear(self):
        self.__data = []

    def append(self, data):
        self.__data.append(data)

    def is_collide(self, node: typing.List[SupportNumber]):
        return is_collision(self.axis, node)

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    def __hash__(self):
        return hash(tuple(self.axis))

    def __repr__(self):
        return f"Cluster(axis={self.axis})"


class NTreeStatic(TreeContainerInterface, typing.Generic[SupportNumber]):
    def __init__(self, axis: typing.List[typing.Tuple[SupportNumber, SupportNumber]], limit_divisions: int = 1):
        """
        NTree is the main container for sorting elements.

        :param axis: Establishes the main axes where the elements will be ordered.
        :param limit_divisions: Maximum number of divisions.
        """
        if limit_divisions < -1:
            raise ValueError("Limit divisions cannot be less than one.")

        self.__children: typing.Dict[int, NTreeStatic[SupportNumber]] = {}
        self.__node: NClusterNode[SupportNumber] = NClusterNode(axis=axis, data=[])
        self.__axis: typing.List[typing.Tuple[SupportNumber, SupportNumber]] = axis
        self.__limit_divisions: int = limit_divisions

    def __hash__(self):
        return hash(self.__node)

    @property
    def axis(self):
        return [*self.__axis]

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

    def sort(self):
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
        self.__node = NClusterNode(axis=self.__axis, data=[])

    def __insert_recursive(self, verx: typing.List[SupportNumber]):
        def create_static_vertex(verx):
            root_axis = collections.deque()

            for axis, c in zip(self.axis, verx):
                x, y = axis
                d = distance(x, y)

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
