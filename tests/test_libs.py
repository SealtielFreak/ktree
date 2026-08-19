"""Unit tests for the geometry helpers in :mod:`ktree.libs`."""

import pytest

from ktree.libs import (
    calc_distance_euclidean,
    calcdist,
    check_axis_intersect,
    is_collision,
    middleaxis,
    middledist,
)


class TestCheckAxisIntersect:
    def test_inside(self):
        assert check_axis_intersect((0.0, 1.0), 0.5)

    def test_boundaries(self):
        assert check_axis_intersect((0.0, 1.0), 0.0)
        assert check_axis_intersect((0.0, 1.0), 1.0)

    def test_outside(self):
        assert not check_axis_intersect((0.0, 1.0), -0.1)
        assert not check_axis_intersect((0.0, 1.0), 1.1)


class TestIsCollision:
    def test_collision(self):
        assert is_collision([(0.0, 1.0), (0.0, 1.0)], [0.5, 0.5])

    def test_miss_on_one_axis(self):
        assert not is_collision([(0.0, 1.0), (0.0, 1.0)], [0.5, 2.0])

    def test_mismatched_lengths_raises(self):
        with pytest.raises(ValueError):
            is_collision([(0.0, 1.0)], [0.5, 0.5])


class TestCalcDistanceEuclidean:
    def test_half_distance(self):
        assert calc_distance_euclidean(0.0, 4.0) == 2.0
        assert calc_distance_euclidean(4.0, 0.0) == 2.0

    def test_zero_distance(self):
        assert calc_distance_euclidean(1.0, 1.0) == 0.0


class TestCalcdist:
    def test_length(self):
        assert calcdist((0.0, 4.0)) == 4.0
        assert calcdist((4.0, 0.0)) == 4.0

    def test_zero_length(self):
        assert calcdist((1.0, 1.0)) == 0.0


class TestMiddledist:
    def test_midpoint(self):
        assert middledist((0.0, 4.0)) == 2.0
        assert middledist((-2.0, 2.0)) == 0.0


class TestMiddleaxis:
    def test_split(self):
        assert middleaxis((0.0, 4.0)) == ((0.0, 2.0), (2.0, 4.0))

    def test_split_negative(self):
        assert middleaxis((-2.0, 2.0)) == ((-2.0, 0.0), (0.0, 2.0))
