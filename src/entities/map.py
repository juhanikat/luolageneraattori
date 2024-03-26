import random
from .room import Room


class RoomSizeError(Exception):
    pass


class RoomPlacementError(Exception):
    pass


class RoomAmountError(Exception):
    pass


class Map():

    def __init__(self, size_x=10, size_y=10) -> None:
        self.size_x = size_x
        self.size_y = size_y
        self.placed_rooms = []
        self.visual = [["." for _ in range(0, size_x)]
                       for _ in range(0, size_y)]

    def place_rooms(self, amount, room_min_size=3, room_max_size=3, room_exact_size=None, overlap=False) -> None:

        def create_rooms(amount: int) -> list:
            """Creates rooms with sizes between <room-min-size> and <room-max-size>.

            Args:
                amount (int): Amount of rooms to create.

            Returns:
                list: The list of created rooms.
            """
            rooms = []
            for _ in range(amount):
                if room_exact_size:
                    room_size_x = room_exact_size
                    room_size_y = room_exact_size
                else:
                    room_size_x = random.randint(room_min_size, room_max_size)
                    room_size_y = random.randint(room_min_size, room_max_size)
                new_room = Room(room_size_x, room_size_y)
                rooms.append(new_room)
            return rooms

        def place_new_room(room: Room) -> Room | bool:
            """Places a room on the map, if able.

            Args:
                room (Room): The room to be placed.

            Returns:
                Room | bool: Returns the placed room if there was room for it, otherwise returns False.
            """
            x_coord = random.randint(0, self.size_x - room.size_x)
            y_coord = random.randint(0, self.size_y - room.size_y)
            room.bottom_left_coords = (x_coord, y_coord)
            if overlap == False:
                for coord in room.get_all_coords():
                    for placed_room in self.placed_rooms:
                        if placed_room.covers(coord):  # if rooms overlap
                            return False

            for y in range(y_coord, y_coord + room.size_y):
                for x in range(x_coord, x_coord + room.size_x):
                    self.visual[y][x] = "#"
            return room

        if room_min_size < 1:
            raise RoomSizeError("Minimum room size cannot be less than 1.")
        if room_max_size > self.size_x or room_max_size > self.size_y:
            raise RoomSizeError(
                "Maximum room size cannot be larger than the map size.")
        if room_max_size < room_min_size:
            raise RoomSizeError(
                "Maximum room size cannot be less than minimum room size.")
        if room_exact_size and room_exact_size < 0:
            raise RoomSizeError("Exact room size cannot be less than 1.")
        if room_exact_size and (room_exact_size > self.size_x or room_exact_size > self.size_y):
            raise RoomSizeError(
                "Exact room size cannot be larger than map size.")
        if amount < 1:
            raise RoomAmountError("Amount of rooms cannot be less than 1.")

        self.placed_rooms.clear()  # remove all previous rooms
        tries = 0
        strikes = 0
        index = 0
        created_rooms = create_rooms(amount=amount)
        while True:
            tries += 1
            if tries >= 1000:
                print(
                    f"Tried to place room {tries} times, removing all rooms to try again.")
                self.placed_rooms.clear()
                created_rooms = create_rooms(amount=amount)
                tries = 0
                strikes += 1
                if strikes == 10:
                    raise RoomPlacementError(
                        "Rooms cannot be placed in reasonable time, they are likely too large to fit the map.")
                index = 0
                continue
            placed = place_new_room(created_rooms[index])
            if placed:
                self.placed_rooms.append(placed)
                index += 1
                if index == len(created_rooms):
                    break

    def __str__(self) -> str:
        representation = f"  {' '.join(str(x) for x in list(range(0, self.size_x)))} \n"
        for index, row in enumerate(self.visual):
            representation += f"{index} {' '.join(row)} \n"
        representation += f"\n Map size: Y{self.size_y} * X{self.size_x} \n"
        representation += f"Rooms: {len(self.placed_rooms)} \n"
        for index, room in enumerate(self.placed_rooms):
            representation += f"Room {index}: {room} \n"
        return representation
