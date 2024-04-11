import pytest

from entities.hallway import Hallway
from entities.map import Map, RoomPlacementError, RoomSizeError
from utilities import PATH_WEIGHT


@pytest.fixture
def setup() -> Map:
    return Map(1000, 1000)


def test_rooms_are_generated(setup: Map):
    setup.place_rooms(2)
    assert len(setup.placed_rooms) == 2
    setup.place_rooms(100)
    assert len(setup.placed_rooms) == 100


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


def test_max_room_size_cannot_be_larger_than_map_size(setup: Map):
    with pytest.raises(RoomSizeError):
        setup.place_rooms(2, room_max_size=1001)


def test_max_room_size_cannot_be_less_than_1(setup: Map):
    with pytest.raises(RoomSizeError):
        setup.place_rooms(2, room_min_size=0)
    with pytest.raises(RoomSizeError):
        setup.place_rooms(2, room_min_size=-2)


def test_max_room_size_cannot_be_less_than_min_room_size(setup: Map):
    with pytest.raises(RoomSizeError):
        setup.place_rooms(2, room_min_size=5, room_max_size=4)


def test_2_rooms_with_same_size_as_map_cannot_be_placed_by_default(setup: Map):
    with pytest.raises(RoomPlacementError):
        setup.place_rooms(2, room_exact_size=1000)


def test_2_rooms_with_same_size_as_map_can_be_placed_with_overlap_on(setup: Map):
    setup.place_rooms(2, room_exact_size=1000, overlap=True)
