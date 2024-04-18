import pytest

from entities.cell import Cell
from entities.hallway import Hallway
from entities.map import Map, RoomPlacementError, RoomSizeError
from utilities import EMPTY_WEIGHT, PATH_WEIGHT, ROOM_WEIGHT


def test_initial_cells_are_correct():
    map = Map(100, 100, 3)
    sum_weights = 0
    for x in range(100):
        for y in range(100):
            assert (x, y) in map.cells
            assert isinstance(map.cells[(x, y)], Cell)
            sum_weights += map.cells[(x, y)].weight
    assert sum_weights == EMPTY_WEIGHT * 10000


def test_rooms_are_placed():
    map = Map(100, 100, 10, room_exact_size=2)
    map.place_rooms()
    assert len(map.placed_rooms) == 10
    sum_weights = 0
    for cell in map.cells.values():
        sum_weights += cell.weight
    assert sum_weights == EMPTY_WEIGHT * 9960 + ROOM_WEIGHT * 40

    map = Map(800, 200, 50, room_exact_size=5)
    map.place_rooms()
    assert len(map.placed_rooms) == 50
    sum_weights = 0
    for cell in map.cells.values():
        sum_weights += cell.weight
    assert sum_weights == EMPTY_WEIGHT * 158750 + ROOM_WEIGHT * 1250


def test_hallways_are_added():
    map = Map(10, 10, 3)
    map.add_hallway(Hallway([(0, 0), (0, 1), (0, 2), (1, 2)]))
    assert len(map.added_hallways) == 1
    hallway_cells = 0
    for cell in map.cells.values():
        if cell.weight == PATH_WEIGHT:
            hallway_cells += 1
    assert hallway_cells == 4


def test_map_size_is_correct():
    map = Map(1000, 1000, 3)
    assert map.get_size()[0] == 1000
    assert map.get_size()[1] == 1000


def test_max_room_size_cannot_be_larger_than_map_size():
    with pytest.raises(RoomSizeError):
        Map(1000, 1000, 3, room_max_size=1001).place_rooms()


def test_max_room_size_cannot_be_less_than_1():
    with pytest.raises(RoomSizeError):
        Map(1000, 1000, 3, room_max_size=0).place_rooms()
    with pytest.raises(RoomSizeError):
        Map(1000, 1000, 3, room_max_size=-2).place_rooms()


def test_max_room_size_cannot_be_less_than_min_room_size():
    with pytest.raises(RoomSizeError):
        Map(1000, 1000, 3, room_min_size=5, room_max_size=4).place_rooms()


def test_3_rooms_with_same_size_as_map_cannot_be_placed():
    with pytest.raises(RoomPlacementError):
        Map(100, 100, 3, room_exact_size=100).place_rooms()
