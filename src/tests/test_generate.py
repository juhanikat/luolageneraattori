import pytest

from entities.map import Map
from services.generate import generate_dungeon


@pytest.fixture
def setup() -> Map:
    return Map(100, 100)


def test_10_rooms_are_connected(setup: Map):
    setup.place_rooms(10)
    edges = generate_dungeon(setup, extra_edges=False)
    assert len(edges) == 9


def test_placing_rooms_many_times():
    for i in range(5000):
        test_map = Map(100, 100)
        test_map.place_rooms(3)
        edges = generate_dungeon(test_map, extra_edges=False)
        assert len(edges) == 2
