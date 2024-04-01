from entities.room import Room


def test_room_area_is_correct():
    room = Room(5, 5)
    assert room.area == 25
    room = Room(0, 5)
    assert room.area == 0


def test_room_coords_are_correct():
    room = Room(2, 2)
    room.bottom_left_coords = (0, 0)
    coords = room.get_all_coords()
    assert coords == [(0, 0), (0, 1), (1, 0), (1, 1)]
    room = Room(2, 2)
    room.bottom_left_coords = (5, 5)
    coords = room.get_all_coords()
    assert coords == [(5, 5), (5, 6), (6, 5), (6, 6)]
    room = Room(0, 0)
    room.bottom_left_coords = (0, 0)
    coords = room.get_all_coords()
    assert coords == []
