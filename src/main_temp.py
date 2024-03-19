import random
import uuid
import argparse


class RoomSizeError(Exception):
    pass


class Room():

    def __init__(self, size_y, size_x) -> None:
        self.id = uuid.uuid4()
        self.size_x = size_x
        self.size_y = size_y
        self.area = size_x*size_y
        self.top_left_coords = None  # (Y, X)

    def get_all_coords(self):
        coords = []
        for y in range(self.top_left_coords[0], self.top_left_coords[0] + self.size_y):
            for x in range(self.top_left_coords[1], self.top_left_coords[1] + self.size_x):
                coords.append((y, x))
        return coords

    def covers(self, coord: tuple):
        coords = self.get_all_coords()
        return coord in coords


class Map():

    def __init__(self, size_x=10, size_y=10) -> None:
        self.size_x = size_x
        self.size_y = size_y
        self.rooms = []
        self.map = [["." for _ in range(0, size_x)] for _ in range(0, size_y)]

    def place_rooms(self, amount, room_min_size=3, room_max_size=3, room_exact_size=None, overlap=False) -> None:
        def place_new_room(room: Room) -> bool:
            x_coord = random.randint(0, self.size_x - room_size_x)
            y_coord = random.randint(0, self.size_y - room_size_y)
            new_room.top_left_coords = (y_coord, x_coord)
            if overlap == False:
                for coord in new_room.get_all_coords():
                    for room in self.rooms:
                        if room.covers(coord):  # if rooms overlap
                            return False  # remove this to debug overlapping
                            print("overlap!!")
                            print(
                                f"new room: {str(new_room.id)[:5]} {new_room.top_left_coords}, size x: {new_room.size_x}, size y: {new_room.size_y}")
                            print(
                                f"conflicting room: {str(room.id)[:5]} {room.top_left_coords}, size x: {room.size_x}, size y: {room.size_y}")
                            for coord in room.get_all_coords():
                                self.map[coord[0]][coord[1]] = "O"
                            for coord in new_room.get_all_coords():
                                if room.covers(coord):
                                    self.map[coord[0]][coord[1]] = "!"
                                else:
                                    self.map[coord[0]][coord[1]] = "N"
                            print(self)
                            exit()

            self.rooms.append(new_room)

            for y in range(y_coord, y_coord + room_size_y):
                for x in range(x_coord, x_coord + room_size_x):
                    self.map[y][x] = "#"
            return True

        if room_min_size < 1:
            raise RoomSizeError("Minimum room size cannot be less than 1.")
        if room_max_size > self.size_x or room_max_size > self.size_y:
            raise RoomSizeError(
                "Maximum room size cannot be larger than the map size.")
        for _ in range(amount):
            if room_exact_size:
                room_size_x = room_exact_size
                room_size_y = room_exact_size
            else:
                room_size_x = random.randint(room_min_size, room_max_size)
                room_size_y = random.randint(room_min_size, room_max_size)
            new_room = Room(room_size_y, room_size_x)

            count = 0
            while True:
                count += 1
                if count >= 1000:
                    print(
                        f"Tried to place room {count} times, room probably cannot be placed.")
                    exit()
                placed = place_new_room(new_room)
                if placed:
                    break

    def __str__(self) -> str:
        representation = "  " + " ".join(str(x)
                                         for x in list(range(0, self.size_x))) + "\n"
        for index, row in enumerate(self.map):
            representation += f"{index} {' '.join(row)} \n"
        representation += f"Map size: Y{self.size_y} * X{self.size_x} \n"
        representation += f"Rooms: {len(self.rooms)}"
        return representation


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--amount", type=int, default=2)
    parser.add_argument("--room_min_size", type=int, default=2)
    parser.add_argument("--room_max_size", type=int, default=4)
    parser.add_argument("--room_exact_size", type=int, default=0)
    parser.add_argument(
        "--can-overlap", action=argparse.BooleanOptionalAction, default=False)

    args = parser.parse_args()

    print(f"Arguments: {args}")
    map = Map()
    map.place_rooms(amount=args.amount, room_min_size=args.room_min_size,
                    room_max_size=args.room_max_size, room_exact_size=args.room_exact_size, overlap=args.can_overlap)
    print(map)
