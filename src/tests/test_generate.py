import pytest

from entities.map import Map
from services.generate import generate_dungeon


@pytest.fixture
def setup() -> Map:
    return Map(10000, 10000)


def test_100_rooms(setup: Map):
    setup.place_rooms(100)
    edges = generate_dungeon(setup)
    assert len(edges) >= 100
