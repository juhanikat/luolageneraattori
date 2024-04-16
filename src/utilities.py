from entities.geometry import Vertex

# Default arguments used for generating the dungeon.
DEFAULT_ARGS = {
    "room_min_size": "2",
    "room_max_size": "4",
    "room_exact_size": "0",
    "can_overlap": False,
    "map_size_x": "20",
    "map_size_y": "20"
}

# Weights given to ifferent types of cells on the map.
ROOM_WEIGHT = 2
PATH_WEIGHT = 0.9
EMPTY_WEIGHT = 1


def validate_int(name: str, input: str) -> int:
    """Checks that an input is not empty, can be converted to an integer, and is not less than 1.

    Args:
        name (str): Used to identify the problem in error message.
        input (str): The input string to validate.

    Raises:
        ValueError: If any of the checks fail.

    Returns:
        int: Input value as an integer.
    """
    if input.strip() == "":
        raise ValueError(f"{name} must not be empty.")
    try:
        input = int(input)
    except ValueError as exception:
        raise ValueError(f"{name} must be a number.") from exception
    if input < 1:
        raise ValueError(f"{name} cannot be less than 1.")
    return input


def convert_rooms_to_x_y_coords(rooms: list) -> list:
    """Takes a list of room objects and converts them to the x, y coordinates of the rooms.

    Args:
        rooms (list): Rooms to convert.

    Returns:
        list: A list of (x, y) coordinates.
    """
    coords = []
    for room in rooms:
        coords.append(room.bottom_left_coords)
    return coords


def convert_rooms_to_vertices(rooms: list) -> list:
    """Takes a list of room objects and converts them to vertices.

    Args:
        rooms (list): Rooms to convert.

    Returns:
        list: A list of vertices.
    """
    vertices = []
    for room in rooms:
        vertices.append(
            Vertex(room.bottom_left_coords[0], room.bottom_left_coords[1]))
    return vertices
