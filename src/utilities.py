from matplotlib import pyplot
from matplotlib.patches import Rectangle

from entities.room import Room


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


DEFAULT_ARGS = {
    "amount": "5",
    "room_min_size": "2",
    "room_max_size": "4",
    "room_exact_size": "0",
    "can_overlap": False,
    "map_size_x": "20",
    "map_size_y": "20"
}


def convert_rooms_to_x_y_coords(rooms: list) -> list:
    """Takes a list of room objects and converts them to the x, y coordinates of the rooms.

    Args:
        rooms (list): Rooms to convert.

    Returns:
        list: A list of x, y coordinates.
    """
    coords = []
    for room in rooms:
        coords.append(room.bottom_left_coords)
    return coords


def display_rooms_and_edges(edges: list, rooms: list, map_size: tuple) -> None:
    if not edges:
        return None
    _, axis = pyplot.subplots(1, ncols=1)
    pyplot.grid(True, which="both", linestyle="--", alpha=0.5)
    pyplot.gca().set_aspect('equal')
    pyplot.minorticks_on()
    pyplot.xlim(-10, map_size[0] + 10)
    pyplot.ylim(-10, map_size[1] + 10)
    for room in rooms:
        rectangle = Rectangle(room.bottom_left_coords,
                              room.size_x, room.size_y, fc=(0, 0, 0, 0.1), ec=(0, 0, 0, 0.1))
        axis.add_patch(rectangle)
    pyplot.ion()

    for edge in edges:
        """
        print(edge)
        pyplot.plot((edge.v0.x, edge.v1.x), (edge.v0.y, edge.v1.y))
        continue
    """
        for coord in edge:
            square = Rectangle(coord, 1, 1, fc=(0, 1, 0, 0.5))
            axis.add_patch(square)

        pyplot.pause(0.01)
    pyplot.ioff()
    pyplot.show()
