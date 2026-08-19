"""Unit tests for :mod:`ktree.ntree` (NClusterNode, NTreeStatic, NTreeDynamic)."""

import pytest

from ktree.ntree import NClusterNode, NTreeDynamic, NTreeStatic

UNIT_2D = [(0.0, 1.0), (0.0, 1.0)]
UNIT_3D = [(0.0, 1.0), (0.0, 1.0), (0.0, 1.0)]


class TestNClusterNode:
    def test_properties(self):
        node = NClusterNode([(0.0, 1.0)], [0.5])
        assert node.shape == [(0.0, 1.0)]
        assert node.data == [0.5]

    def test_len_and_iter(self):
        node = NClusterNode([(0.0, 1.0)], [0.1, 0.2])
        assert len(node) == 2
        assert list(node) == [0.1, 0.2]

    def test_append_and_clear(self):
        node = NClusterNode([(0.0, 1.0)], [])
        node.append(0.9)
        assert list(node) == [0.9]
        node.clear()
        assert len(node) == 0

    def test_is_collide(self):
        node = NClusterNode([(0.0, 1.0), (0.0, 1.0)], [])
        assert node.is_collide([0.5, 0.5])
        assert not node.is_collide([2.0, 0.5])

    def test_hash_and_repr(self):
        node = NClusterNode([(0.0, 1.0), (0.0, 1.0)], [])
        assert hash(node) == hash(((0.0, 1.0), (0.0, 1.0)))
        assert repr(node) == "Cluster(axis=[(0.0, 1.0), (0.0, 1.0)])"


class TestNTreeStatic:
    def test_invalid_divisions(self):
        with pytest.raises(ValueError):
            NTreeStatic(UNIT_2D, limit_divisions=-2)

    def test_shape(self):
        tree = NTreeStatic(UNIT_2D)
        assert tree.shape == UNIT_2D

    def test_empty_sort(self):
        tree = NTreeStatic(UNIT_2D, limit_divisions=2)
        assert tree.sort() == []

    def test_single_point(self):
        tree = NTreeStatic(UNIT_2D, limit_divisions=2)
        tree.insert([0.1, 0.1])
        clusters = tree.sort()
        assert len(clusters) == 1
        assert isinstance(clusters[0], NClusterNode)
        assert clusters[0].data == [[0.1, 0.1]]

    def test_points_preserved(self):
        points = [[0.1, 0.1], [0.9, 0.9], [0.1, 0.9], [0.9, 0.1]]
        tree = NTreeStatic(UNIT_2D, limit_divisions=2)
        for p in points:
            tree.insert(p)

        clusters = tree.sort()
        seen = [tuple(p) for c in clusters for p in c.data]
        assert sorted(seen) == sorted(tuple(p) for p in points)

    def test_octree_3d(self):
        points = [[0.1, 0.1, 0.1], [0.9, 0.9, 0.9], [0.1, 0.9, 0.1]]
        tree = NTreeStatic(UNIT_3D, limit_divisions=2)
        for p in points:
            tree.insert(p)

        seen = [tuple(p) for c in tree.sort() for p in c.data]
        assert sorted(seen) == sorted(tuple(p) for p in points)

    def test_children_and_is_parent(self):
        tree = NTreeStatic(UNIT_2D, limit_divisions=1)
        tree.insert([0.1, 0.1])
        assert tree.is_parent
        assert len(tree.children) > 0

    def test_out_of_bounds_raises(self):
        tree = NTreeStatic(UNIT_2D, limit_divisions=1)
        with pytest.raises(ValueError):
            tree.insert([2.0, 2.0])

    def test_iter_matches_sort(self):
        tree = NTreeStatic(UNIT_2D, limit_divisions=2)
        tree.insert([0.1, 0.1])
        tree.insert([0.9, 0.9])
        assert list(tree) == tree.sort()

    def test_clear(self):
        tree = NTreeStatic(UNIT_2D, limit_divisions=2)
        tree.insert([0.1, 0.1])
        tree.clear()
        assert tree.sort() == []
        assert not tree.is_parent


class TestNTreeDynamic:
    def test_invalid_divisions(self):
        with pytest.raises(ValueError):
            NTreeDynamic(limit_divisions=-2)

    def test_len(self):
        tree = NTreeDynamic(limit_divisions=2)
        tree.insert([0.1, 0.1])
        tree.insert([0.9, 0.9])
        assert len(tree) == 2

    def test_limit_size_property(self):
        assert NTreeDynamic(limit_size=10).limit_size == 10

    def test_shape_none_before_sort(self):
        tree = NTreeDynamic()
        assert tree.shape is None

    def test_empty_sort(self):
        assert NTreeDynamic(limit_divisions=1).sort() == []

    def test_points_preserved(self):
        points = [[0.1, 0.1], [0.9, 0.9], [0.5, 0.5]]
        tree = NTreeDynamic(limit_divisions=2)
        for p in points:
            tree.insert(p)

        clusters = tree.sort()
        assert clusters
        assert all(isinstance(c, NClusterNode) for c in clusters)

        seen = [tuple(p) for c in clusters for p in c.data]
        assert sorted(seen) == sorted(tuple(p) for p in points)

    def test_shape_computed_from_data(self):
        tree = NTreeDynamic(limit_divisions=1)
        tree.insert([2.0, 3.0])
        tree.insert([5.0, 7.0])
        tree.sort()
        assert tree.shape == [[2.0, 5.0], [3.0, 7.0]]

    def test_iter_matches_sort(self):
        tree = NTreeDynamic(limit_divisions=2)
        tree.insert([0.1, 0.1])
        tree.insert([0.9, 0.9])

        def flatten(clusters):
            return sorted(tuple(p) for c in clusters for p in c.data)

        assert flatten(list(tree)) == flatten(tree.sort())

    def test_clear_keeps_data(self):
        tree = NTreeDynamic(limit_divisions=2)
        tree.insert([0.1, 0.1])
        tree.insert([0.9, 0.9])
        tree.clear()
        assert len(tree) == 2
