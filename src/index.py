import argparse
from entities.room import Room
from entities.map import Map, RoomPlacementError
from matplotlib import pyplot
from matplotlib.patches import Rectangle
from bowyer import bowyer_watson


def display_figure(triangles: list, rooms: list, map_size: tuple) -> None:
    """Displays a figure showing the output of the program.

    Args:
        triangles (list): List of triangles.
        rooms (list): List of rooms. These will be used to place Rectangles on the figure.
    """

    draw_circumcircles = False
    _, axis = pyplot.subplots(1)
    axis.set_xlabel("After removing supertriangle and adjacent triangles")
    pyplot.gca().set_aspect('equal')
    pyplot.xlim(-10, map_size[0] + 10)
    pyplot.ylim(-10, map_size[1] + 10)
    for room in rooms:
        rectangle = Rectangle(room.bottom_left_coords,
                              room.size_x, room.size_y, fc=(0, 0, 0, 0.1), ec=(0, 0, 0, 0.1))
        axis.add_patch(rectangle)
    pyplot.ion()

    for triangle in triangles:
        print(triangle)
        axis.plot([triangle.v0.x, triangle.v1.x, triangle.v2.x, triangle.v0.x],
                  [triangle.v0.y, triangle.v1.y, triangle.v2.y, triangle.v0.y])
        if draw_circumcircles:
            circumcircle = pyplot.Circle(
                triangle.circumcenter, triangle.circumcircle_radius, color='r', fill=False, linestyle="dashed")
            axis.add_artist(circumcircle)
        pyplot.pause(0.2)
    pyplot.ioff()
    pyplot.show()


def main():
    def parse_args():
        parser = argparse.ArgumentParser()
        parser.add_argument("--amount", type=int, default=5)
        parser.add_argument("--room-min-size", type=int, default=2)
        parser.add_argument("--room-max-size", type=int, default=4)
        parser.add_argument("--room-exact-size", type=int, default=0)
        parser.add_argument(
            "--can-overlap", action=argparse.BooleanOptionalAction, default=False)

        parser.add_argument("--map-size-x", type=int, default=20)
        parser.add_argument("--map-size-y", type=int, default=20)
        args = parser.parse_args()
        return args

    args = parse_args()
    map = Map(args.map_size_x, args.map_size_y)
    try:
        map.place_rooms(amount=args.amount, room_min_size=args.room_min_size,
                        room_max_size=args.room_max_size, room_exact_size=args.room_exact_size, overlap=args.can_overlap)
    except (RoomPlacementError) as exception:
        print(exception)
        exit()
    x_y_coords = []
    rooms = map.placed_rooms
    for room in rooms:
        x_y_coords.append(room.bottom_left_coords)
    triangles = bowyer_watson(x_y_coords)
    display_figure(triangles, rooms, (args.map_size_x, args.map_size_y))
    print(map)


if __name__ == "__main__":
    main()
