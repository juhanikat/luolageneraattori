from entities.map import Map
from services.generate import generate_dungeon


def test_rooms_are_connected():
    map = Map(100, 100, 10)
    hallways = generate_dungeon(map, extra_edges=False)
    assert len(hallways) == 9
    map = Map(500, 500, 100)
    hallways = generate_dungeon(map, extra_edges=False)
    assert len(hallways) == 99


def test_placing_rooms_many_times():
    for _ in range(200):
        map = Map(100, 100, 3)
        hallways = generate_dungeon(map, extra_edges=False)
        assert len(hallways) == 2
