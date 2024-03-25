from entities.room import Room
from matplotlib import pyplot
from matplotlib.patches import Rectangle


def convert_rooms_to_x_y_coords(rooms: list) -> list:
    coords = []
    for room in rooms:
        coords.append(room.bottom_left_coords)
    return coords


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


def display_figure(triangles: list, rooms: list, map_size: tuple, circumcircles=False) -> None:
    """Displays a figure showing the output of the program.

    Args:
        triangles (list): List of triangles.
        rooms (list): List of rooms. These will be used to place Rectangles on the figure.
        map_size (tuple): Map size in (x, y) coordinate format. Will be used to set the axis values.
        circumcircles (bool, optional): Whether to draw circumcircles around triangles. Defaults to False.
    """

    _, axis = pyplot.subplots(1)
    pyplot.gca().set_aspect('equal')
    pyplot.xlim(-10, map_size[0] + 10)
    pyplot.ylim(-10, map_size[1] + 10)
    for room in rooms:
        rectangle = Rectangle(room.bottom_left_coords,
                              room.size_x, room.size_y, fc=(0, 0, 0, 0.1), ec=(0, 0, 0, 0.1))
        axis.add_patch(rectangle)
    pyplot.ion()

    for triangle in triangles:
        axis.plot([triangle.v0.x, triangle.v1.x, triangle.v2.x, triangle.v0.x],
                  [triangle.v0.y, triangle.v1.y, triangle.v2.y, triangle.v0.y])
        if circumcircles:
            circumcircle = pyplot.Circle(
                triangle.circumcenter, triangle.circumcircle_radius, color='r', fill=False, linestyle="dashed")
            axis.add_artist(circumcircle)
        pyplot.pause(0.2)
    pyplot.ioff()
    pyplot.show()
