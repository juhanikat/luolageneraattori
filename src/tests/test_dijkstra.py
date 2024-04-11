import pytest

from algorithms import shortest_path_dijkstra
from entities.map import Map


@pytest.fixture
def setup():
    return Map(50, 50)


def test_path_length_is_correct(setup: Map):
    path = shortest_path_dijkstra(
        setup, setup.get_cell((0, 0)), setup.get_cell((49, 49)))
    assert len(path) == 99
    path = shortest_path_dijkstra(
        setup, setup.get_cell((0, 0)), setup.get_cell((0, 0)))
    assert len(path) == 1
