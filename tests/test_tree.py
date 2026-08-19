"""Unit tests for the abstract interfaces in :mod:`ktree.tree`."""

import pytest

from ktree.kdtree import KDCluster, KDTree
from ktree.ntree import NClusterNode, NTreeDynamic, NTreeStatic
from ktree.tree import ClusterInterface, TreeContainerInterface


class TestClusterInterface:
    def test_cannot_instantiate(self):
        with pytest.raises(TypeError):
            ClusterInterface()

    def test_implementations(self):
        assert issubclass(KDCluster, ClusterInterface)
        assert issubclass(NClusterNode, ClusterInterface)

    def test_instances(self):
        assert isinstance(KDCluster(0, [(0.0, 1.0)], []), ClusterInterface)
        assert isinstance(NClusterNode([(0.0, 1.0)], []), ClusterInterface)


class TestTreeContainerInterface:
    def test_cannot_instantiate(self):
        with pytest.raises(TypeError):
            TreeContainerInterface()

    def test_implementations(self):
        assert issubclass(KDTree, TreeContainerInterface)
        assert issubclass(NTreeStatic, TreeContainerInterface)
        assert issubclass(NTreeDynamic, TreeContainerInterface)

    def test_instances(self):
        assert isinstance(KDTree([(0.0, 1.0)]), TreeContainerInterface)
        assert isinstance(NTreeStatic([(0.0, 1.0)]), TreeContainerInterface)
        assert isinstance(NTreeDynamic(), TreeContainerInterface)
