from entities.room import Room


def debug_overlapping(new_room: Room, existing_room: Room, map_visual: list):
    """Used to show visually how two rooms overlap.

    Args:
        new_room (Room): The room that was placed to cause the overlap.
        existing_room (Room): The room that was already on the map.
        map_visual (list): Visual representation of the map.
    """
    print(
        f"new room: {new_room}")
    print(
        f"conflicting room: {existing_room}")
    for coord in existing_room.get_all_coords():
        map_visual[coord[0]][coord[1]] = "O"
    for coord in new_room.get_all_coords():
        if existing_room.covers(coord):
            map_visual[coord[0]][coord[1]] = "!"
        else:
            map_visual[coord[0]][coord[1]] = "N"
    print(map_visual)
