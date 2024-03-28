import pytest

from ..algorithms import bowyer_watson


def test_3_rooms_results_in_one_triangle():
    triangles = bowyer_watson([(0, 0), (10, 10), (0, 5)])
    assert len(triangles) == 1


def test_rooms_with_same_y_coordinate_results_in_0_triangles():
    triangles = bowyer_watson([(0, 0), (10, 0), (56, 0)])
    assert len(triangles) == 0
    triangles = bowyer_watson([(10, -6), (13, -6), (-6, -6)])
    assert len(triangles) == 0


def test_rooms_with_same_x_coordinate_results_in_0_triangles():
    triangles = bowyer_watson([(0, 5), (0, 23), (0, 123456)])
    assert len(triangles) == 0
    triangles = bowyer_watson([(0, -6), (0, -5), (0, -4)])
    assert len(triangles) == 0
