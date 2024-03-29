
import pytest

from ..entities.map import Map, RoomSizeError, RoomPlacementError
from ..entities.room import Room


@pytest.fixture
def setup() -> Map:
    return Map(10, 10)


def test_rooms_are_generated(setup: Map):
    setup.place_rooms(2)
    assert len(setup.placed_rooms) == 2


def test_max_room_size_cannot_be_larger_than_map_size(setup: Map):
    with pytest.raises(RoomSizeError):
        setup.place_rooms(2, room_max_size=11)


def test_max_room_size_cannot_be_less_than_1(setup: Map):
    with pytest.raises(RoomSizeError):
        setup.place_rooms(2, room_min_size=0)
    with pytest.raises(RoomSizeError):
        setup.place_rooms(2, room_min_size=-1)


def test_max_room_size_cannot_be_less_than_min_room_size(setup: Map):
    with pytest.raises(RoomSizeError):
        setup.place_rooms(2, room_min_size=5, room_max_size=4)


def test_2_rooms_with_same_size_as_map_cannot_be_placed_by_default(setup: Map):
    with pytest.raises(RoomPlacementError):
        setup.place_rooms(2, room_exact_size=10)


def test_2_rooms_with_same_size_as_map_can_be_placed_with_overlap_on(setup: Map):
    setup.place_rooms(2, room_exact_size=10, overlap=True)
