"""Unit tests for the package-level exports in :mod:`ktree`."""

import ktree


class TestPackageExports:
    def test_version(self):
        assert isinstance(ktree.__VERSION__, str)
        assert ktree.__VERSION__

    def test_all(self):
        expected = {
            "ClusterInterface",
            "KDCluster",
            "KDTree",
            "NClusterNode",
            "NTreeDynamic",
            "NTreeStatic",
            "TreeContainerInterface",
        }
        assert set(ktree.__all__) == expected

    def test_reexports(self):
        for name in ktree.__all__:
            assert hasattr(ktree, name)
