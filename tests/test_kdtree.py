"""Unit tests for :mod:`ktree.kdtree` (KDCluster and KDTree)."""

from ktree.kdtree import KDCluster, KDTree

AXIS_2D = [(-5.0, 5.0), (-5.0, 5.0)]


class TestKDCluster:
    def test_properties(self):
        cluster = KDCluster(1, [(0.0, 1.0)], [(0.5, 0.5)])
        assert cluster.level == 1
        assert cluster.shape == [(0.0, 1.0)]
        assert cluster.data == [(0.5, 0.5)]

    def test_len_and_iter(self):
        cluster = KDCluster(0, [(0.0, 1.0)], [(0.1, 0.1), (0.2, 0.2)])
        assert len(cluster) == 2
        assert list(cluster) == [(0.1, 0.1), (0.2, 0.2)]

    def test_append(self):
        cluster = KDCluster(0, [(0.0, 1.0)], [])
        cluster.append((0.9, 0.9))
        assert cluster.data == [(0.9, 0.9)]

    def test_clear(self):
        cluster = KDCluster(0, [(0.0, 1.0)], [(0.1, 0.1)])
        cluster.clear()
        assert len(cluster) == 0

    def test_hash_and_repr(self):
        cluster = KDCluster(1, [(0.0, 1.0), (0.0, 1.0)], [])
        assert hash(cluster) == hash(tuple([(0.0, 1.0), (0.0, 1.0)]))
        assert repr(cluster) == "Cluster(axis=[(0.0, 1.0), (0.0, 1.0)], level=1)"


class TestKDTree:
    def test_empty_sort(self):
        tree = KDTree(AXIS_2D)
        clusters = tree.sort()
        assert all(len(c) == 0 for c in clusters)

    def test_single_point(self):
        tree = KDTree(AXIS_2D)
        tree.insert([1.0, 2.0])
        clusters = tree.sort()
        assert clusters
        assert all(isinstance(c, KDCluster) for c in clusters)

    def test_points_preserved(self):
        points = [[1.0, 2.0], [-2.0, -1.0], [4.0, 4.0]]
        tree = KDTree(AXIS_2D)
        for p in points:
            tree.insert(p)

        clusters = tree.sort()
        seen = [tuple(p) for c in clusters for p in c.data]

        for p in points:
            assert tuple(p) in seen
        for p in seen:
            assert list(p) in points

    def test_multi_dimension(self):
        tree = KDTree([(-5.0, 5.0) for _ in range(5)])
        tree.insert([1.0, 2.0, 3.0, 4.0, 5.0])
        assert len(tree.sort()) > 0

    def test_iter_matches_sort(self):
        tree = KDTree(AXIS_2D)
        for p in ([1.0, 2.0], [-2.0, -1.0]):
            tree.insert(p)
        clusters = tree.sort()
        assert list(tree) == clusters

    def test_clear(self):
        tree = KDTree(AXIS_2D)
        tree.insert([1.0, 2.0])
        tree.sort()
        tree.clear()
        assert all(len(c) == 0 for c in tree.sort())
