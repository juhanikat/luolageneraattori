import pytest

from entities.hallway import Hallway
from entities.map import Map, RoomPlacementError, RoomSizeError
from utilities import PATH_WEIGHT


@pytest.fixture
def setup() -> Map:
    return Map(1000, 1000, 3)


def test_rooms_are_generated():
    map = Map(1000, 1000, 3)
    map.create_rooms()
    map.place_rooms()
    assert len(map.placed_rooms) == 3

    map = Map(1000, 1000, 100)
    map.create_rooms()
    map.place_rooms()
    assert len(map.placed_rooms) == 100


def test_hallways_are_added(setup: Map):
    setup.add_hallway(Hallway([(0, 0), (0, 1), (0, 2), (1, 2)]))
    assert len(setup.added_hallways) == 1
    hallway_cells = 0
    for cell in setup.cells.values():
        if cell.weight == PATH_WEIGHT:
            hallway_cells += 1
    assert hallway_cells == 4


def test_map_size_is_correct(setup: Map):
    assert setup.get_size()[0] == 1000
    assert setup.get_size()[1] == 1000


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


def test_3_rooms_with_same_size_as_map_cannot_be_placed_by_default():
    with pytest.raises(RoomPlacementError):
        Map(1000, 1000, 3, room_exact_size=1000).place_rooms()


def test_3_rooms_with_same_size_as_map_can_be_placed_with_overlap_on():
    Map(1000, 1000, 3, room_exact_size=1000, overlap=True).place_rooms()
