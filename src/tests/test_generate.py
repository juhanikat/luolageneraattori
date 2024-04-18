from entities.map import Map
from services.generate import generate_dungeon


def test_rooms_are_connected():
    map = Map(100, 100, 10)
    edges = generate_dungeon(map, extra_edges=False)
    assert len(edges) == 9
    map = Map(500, 500, 100)
    edges = generate_dungeon(map, extra_edges=False)
    assert len(edges) == 99


def test_placing_rooms_many_times():
    for _ in range(10):
        map = Map(100, 100, 3)
        edges = generate_dungeon(map, extra_edges=False)
        assert len(edges) == 2
