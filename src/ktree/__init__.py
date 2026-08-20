"""KTree provides hierarchical spatial grouping structures.

KTree exposes a small collection of tree-based containers for partitioning
points in N-dimensional space:

- :class:`ktree.KDTree` for recursive axis-aligned splitting.
- :class:`ktree.NTreeStatic` for fixed-bounds N-ary trees (QuadTree, Octree).
- :class:`ktree.NTreeDynamic` for data-driven N-ary trees.

The public interfaces are defined by :class:`ktree.ClusterInterface` and
:class:`ktree.TreeContainerInterface`.
"""

from ktree.kdtree import KDCluster, KDTree
from ktree.ntree import NClusterNode, NTreeDynamic, NTreeStatic
from ktree.tree import ClusterInterface, TreeContainerInterface

__VERSION__ = "0.2.2"

__all__ = [
    "ClusterInterface",
    "KDCluster",
    "KDTree",
    "NClusterNode",
    "NTreeDynamic",
    "NTreeStatic",
    "TreeContainerInterface",
]
