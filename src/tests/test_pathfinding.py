import pytest

from algorithms import shortest_path_a_star, shortest_path_dijkstra
from entities.map import Map


@pytest.fixture
def setup():
    return Map(50, 50, 3)


def test_path_length_is_correct_dijkstra(setup: Map):
    path = shortest_path_dijkstra(
        setup, setup.get_cell((0, 0)), setup.get_cell((49, 49)))
    assert len(path) == 99
    path = shortest_path_dijkstra(
        setup, setup.get_cell((0, 0)), setup.get_cell((0, 0)))
    assert len(path) == 1


def test_path_length_is_correct_a_star(setup: Map):
    path = shortest_path_a_star(
        setup, setup.get_cell((0, 0)), setup.get_cell((49, 49)))
    assert len(path) == 99
    path = shortest_path_a_star(
        setup, setup.get_cell((0, 0)), setup.get_cell((0, 0)))
    assert len(path) == 1
