import random

from entities.cell import Cell
from entities.hallway import Hallway

from .room import Room


class RoomSizeError(Exception):
    """Raised if room size parameters are invalid.
    """


class RoomPlacementError(Exception):
    """Raised if rooms cannot be placed on the map.
    """


class RoomAmountError(Exception):
    """Raised if room amount parameter is invalid.
    """


class Map:
    """A class that holds all placed rooms.
    """

    def __init__(self, size_x, size_y) -> None:
        self.size_x = size_x
        self.size_y = size_y
        self.cells = {(x, y): Cell(x, y, 1)
                      for x in range(size_x) for y in range(size_y)}
        self.placed_rooms = []
        self.added_hallways = []

    def get_size(self) -> tuple:
        """Returns a tuple containing the width and length of the map.

        Returns:
            tuple: Map dimensions in (width, length) format.
        """
        return (self.size_x, self.size_y)

    def create_rooms(self, amount: int, room_min_size: int = 2,
                     room_max_size: int = 5, room_exact_size: int = 0) -> list:
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

    def place_new_room(self, room: Room, overlap=False) -> Room | bool:
        """Places a room on the map, if able.

        Args:
            room (Room): The room to be placed.

        Returns:
            Room | bool: Returns the placed room if there was room for it, otherwise returns False.
        """
        x_coord = random.randint(0, self.size_x - room.size_x)
        y_coord = random.randint(0, self.size_y - room.size_y)
        room.bottom_left_coords = (x_coord, y_coord)
        if overlap is False:
            for coord in room.get_all_coords():
                for placed_room in self.placed_rooms:
                    if placed_room.covers(coord):  # if rooms overlap
                        return False
        return room

    def place_rooms(self, amount: int = 10, room_min_size: int = 2, room_max_size: int = 5,
                    room_exact_size: int = 0, overlap: bool = False) -> None:
        """Creates rooms and places them on the map.

        Args:
            amount (int, optional): Amount of rooms. Defaults to 10.
            room_min_size (int, optional): Minimum size of rooms. Defaults to 2.
            room_max_size (int, optional): Maximum size of rooms. Defaults to 5.
            room_exact_size (int, optional): Exact size of rooms. 
            If used, room_min_size and room_max_size do nothing. Defaults to 0.
            overlap (bool, optional): If True, rooms can overlap with each other. Defaults to False.

        Raises:
            RoomSizeError: Raised if room size parameters are invalid.
            RoomAmountError: Raised if room amount parameter is invalid.
            RoomPlacementError: Raised if rooms cannot be placed on the map in reasonable time.
        """

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
        created_rooms = self.create_rooms(
            amount=amount,
            room_min_size=room_min_size,
            room_max_size=room_max_size,
            room_exact_size=room_exact_size)
        while True:
            tries += 1
            if tries >= 500:
                print(
                    f"Tried to place room {tries} times, removing all rooms to try again.")
                self.placed_rooms.clear()
                created_rooms = self.create_rooms(
                    amount=amount,
                    room_min_size=room_min_size,
                    room_max_size=room_max_size,
                    room_exact_size=room_exact_size)
                tries = 0
                strikes += 1
                if strikes == 5:
                    raise RoomPlacementError(
                        "Rooms cannot be placed in reasonable time, they are likely too large to fit the map.")
                index = 0
                continue
            placed = self.place_new_room(created_rooms[index], overlap=overlap)
            if placed:
                self.placed_rooms.append(placed)
                for coord in placed.get_all_coords():
                    self.cells[coord] = Cell(coord[0], coord[1], 10)
                index += 1
                if index == len(created_rooms):
                    break

    def add_hallway(self, hallway: Hallway):
        self.added_hallways.append(hallway)
        for coord in hallway.coords:
            self.cells[coord] = Cell(coord[0], coord[1], 0.5)

    def get_cell(self, coord: tuple) -> Cell:
        return self.cells[coord]

    def check_hallway_overlap(self, hallway1: Hallway, hallway2: Hallway):
        for coord in hallway1.coords:
            if coord in hallway2.coords:
                return True
        return False

    def __str__(self) -> str:
        representation = f"\n Map size: Y{self.size_y} * X{self.size_x} \n"
        representation += f"Rooms: {len(self.placed_rooms)} \n"
        for index, room in enumerate(self.placed_rooms):
            representation += f"Room {index}: {room} \n"
        return representation
