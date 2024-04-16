import pytest

from entities.map import Map
from services.generate import generate_dungeon


@pytest.fixture
def setup() -> Map:
    return Map(100, 100, 10)


def test_10_rooms_are_connected(setup: Map):
    setup.place_rooms()
    edges = generate_dungeon(setup, extra_edges=False)
    assert len(edges) == 9


def test_placing_rooms_many_times():
    for _ in range(5000):
        test_map = Map(100, 100, 3)
        test_map.place_rooms()
        edges = generate_dungeon(test_map, extra_edges=False)
        assert len(edges) == 2
