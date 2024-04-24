import pytest

from algorithms import shortest_path_a_star
from entities.map import Map

TEST_ROOM_WEIGHT = 5
TEST_ROOM_WEIGHT_2 = 4
TEST_EMPTY_WEIGHT = 1


@pytest.fixture
def setup():
    return Map(50, 50, 3)


def test_path_length_is_correct_a_star(setup: Map):
    path = shortest_path_a_star(
        setup, setup.get_cell((0, 0)), setup.get_cell((49, 49)))
    assert len(path) == 99
    path = shortest_path_a_star(
        setup, setup.get_cell((0, 0)), setup.get_cell((0, 0)))
    assert len(path) == 1
    setup.cells[(1, 0)].weight = TEST_ROOM_WEIGHT
    setup.cells[(1, 1)].weight = TEST_ROOM_WEIGHT
    path = shortest_path_a_star(
        setup, setup.get_cell((0, 0)), setup.get_cell((2, 0)))
    assert len(path) == 7
    setup.cells[(1, 0)].weight = TEST_ROOM_WEIGHT_2
    setup.cells[(1, 1)].weight = TEST_ROOM_WEIGHT_2
    path = shortest_path_a_star(
        setup, setup.get_cell((0, 0)), setup.get_cell((2, 0)))
    assert len(path) == 3
