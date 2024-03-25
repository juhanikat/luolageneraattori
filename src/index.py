import argparse
from entities.room import Room
from entities.map import Map, RoomPlacementError
from matplotlib import pyplot
from matplotlib.patches import Rectangle
from bowyer import bowyer_watson
from ui.ui import UI




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
    print(args)
    map = Map(args.map_size_x, args.map_size_y)
    ui = UI(map)
    ui.start()
    return
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
    triangles = bowyer_watson((x_y_coords))
    display_figure(triangles, rooms, (args.map_size_x, args.map_size_y))
    print(map)


if __name__ == "__main__":
    main()
