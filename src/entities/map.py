import random

from entities.cell import Cell
from entities.geometry import Vertex
from entities.hallway import Hallway
from utilities import (DEFAULT_ARGS, EMPTY_WEIGHT, PATH_WEIGHT, ROOM_WEIGHT,
                       convert_rooms_to_vertices)

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
    """A class that holds all placed rooms and hallways.
    """

    def __init__(self, size_x: int, size_y: int, amount: int, room_min_size: int = -1, room_max_size: int = -1, room_exact_size: int = -1, overlap=False) -> None:
        """_summary_

        Args:
            size_x (int): Width of the map.
            size_y (int): Height of the map.
        """
        self.size_x = size_x
        self.size_y = size_y
        self.cells = {(x, y): Cell(x, y, EMPTY_WEIGHT)
                      for x in range(size_x) for y in range(size_y)}
        self.created_rooms = []
        self.placed_rooms = []
        self.added_hallways = []

        try:
            self.check_args(amount,
                            room_min_size,
                            room_max_size,
                            room_exact_size)
        except (RoomSizeError, RoomAmountError) as _:
            raise

        self.amount = amount
        self.room_min_size = room_min_size
        self.room_max_size = room_max_size
        self.room_exact_size = room_exact_size
        self.overlap = overlap

    def reset_placement(self):
        self.placed_rooms.clear()
        self.cells = {(x, y): Cell(x, y, EMPTY_WEIGHT)
                      for x in range(self.size_x) for y in range(self.size_y)}

    def check_args(self, amount: int, room_min_size: int, room_max_size: int, room_exact_size: int) -> tuple:
        """Validates the arguments that are given to the map, or gives default values to them.

        Args:
            amount (int): Amount of rooms.
            room_min_size (int): Minimum size of rooms.
            room_max_size (int): Maximum size of rooms.
            room_exact_size (int): Exact size of rooms. If present, room_min_size and room_max_size do nothing.

        Raises:
            RoomSizeError: Raised if a room size argument is invalid.
            RoomAmountError: Raised if amount of rooms is invalid.
        """
        if room_min_size == -1:
            room_min_size = int(DEFAULT_ARGS["room_min_size"])
        if room_max_size == -1:
            room_max_size = int(DEFAULT_ARGS["room_max_size"])
        if room_exact_size == -1:
            room_exact_size = int(DEFAULT_ARGS["room_exact_size"])

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
        if room_exact_size != 0 and (room_exact_size > self.size_x
                                     or room_exact_size > self.size_y):
            raise RoomSizeError(
                "Exact room size cannot be larger than map size.")
        if amount < 3:
            raise RoomAmountError("Amount of rooms cannot be less than 3.")

        self.amount = amount
        self.room_min_size = room_min_size
        self.room_max_size = room_max_size
        self.room_exact_size = room_exact_size
        return None

    def check_parallel(self, vertex1: Vertex, vertex2: Vertex, vertex3: Vertex):
        formula = vertex3.x * vertex2.y + vertex1.x * vertex3.y + vertex2.x * vertex1.y - \
            vertex1.x * vertex2.y - vertex3.x * vertex1.y - vertex2.x * vertex3.y
        print(f"formula: {formula}")
        return formula == 0

    def get_size(self) -> tuple:
        """Returns a tuple containing the width and length of the map.

        Returns:
            tuple: Map dimensions in (width, length) format.
        """
        return (self.size_x, self.size_y)

    def get_cell(self, coords: tuple) -> Cell:
        """Finds the Cell object at the given coordinates.

        Args:
            coords (tuple): The coordinate to look for.

        Returns:
            The Cell object at the coordinates specified, 
            or None if coords is outside the map's area.
        """
        return self.cells.get(coords, None)

    def create_rooms(self) -> list:
        """Creates rooms with sizes between room-min-size and room-max-size.

        Args:
            amount (int): Amount of rooms to create.

        Returns:
            list: The list of created rooms.
        """
        rooms = []
        for _ in range(self.amount):
            if self.room_exact_size:
                room_size_x = self.room_exact_size
                room_size_y = self.room_exact_size
            else:
                room_size_x = random.randint(
                    self.room_min_size, self.room_max_size)
                room_size_y = random.randint(
                    self.room_min_size, self.room_max_size)
            new_room = Room(room_size_x, room_size_y)
            rooms.append(new_room)
        self.created_rooms = rooms

    def place_new_room(self, room: Room) -> Room | bool:
        """Randomly places a room on the map, if able.

        Args:
            room (Room): The room to be placed.

        Returns:
            Room | bool: Returns the placed room if there was room for it, otherwise returns False.
        """
        x_coord = random.randint(0, self.size_x - room.size_x)
        y_coord = random.randint(0, self.size_y - room.size_y)
        room.bottom_left_coords = (x_coord, y_coord)
        if self.overlap is False:
            for coord in room.get_all_coords():
                for placed_room in self.placed_rooms:
                    if placed_room.covers(coord):  # if rooms overlap
                        return False
        return room

    def place_rooms(self) -> None:
        """Creates rooms and places them on the map.

        Args:
            amount (int, optional): Amount of rooms.
            room_min_size (int, optional): Minimum size of rooms.
            room_max_size (int, optional): Maximum size of rooms
            room_exact_size (int, optional): Exact size of rooms. 
            If used, room_min_size and room_max_size do nothing.
            overlap (bool, optional): If True, rooms can overlap with each other. Defaults to False.

        Raises:
            RoomSizeError: Raised if room size parameters are invalid.
            RoomAmountError: Raised if room amount parameter is invalid.
            RoomPlacementError: Raised if rooms cannot be placed on the map in reasonable time.
        """

        self.reset_placement()
        tries = 0
        strikes = 0
        index = 0
        while True:
            print("loop")
            tries += 1
            if tries >= 500:
                print(
                    f"Tried to place room {tries} times, removing all rooms to try again.")
                self.reset_placement()
                self.create_rooms()
                tries = 0
                strikes += 1
                if strikes == 5:
                    raise RoomPlacementError(
                        "Rooms cannot be placed in reasonable time, " +
                        "try adjusting room amount or room size.")
                index = 0
                continue
            print(index)
            placed = self.place_new_room(self.created_rooms[index])
            if placed:
                print("placed")
                self.placed_rooms.append(placed)
                for coord in placed.get_all_coords():
                    self.cells[coord] = Cell(coord[0], coord[1], ROOM_WEIGHT)
                index += 1
                if index == len(self.created_rooms):
                    print("done")
                    print(index)
                    print(self.placed_rooms)
                    if len(self.created_rooms) == 3:
                        print(self.created_rooms)
                        parallel = self.check_parallel(
                            *convert_rooms_to_vertices(self.placed_rooms))
                        if parallel:
                            print("parallel")
                            self.reset_placement()
                            self.create_rooms()
                            tries = 0
                            strikes += 1
                            if strikes == 5:
                                raise RoomPlacementError(
                                    "Rooms cannot be placed in reasonable time, " +
                                    "try adjusting room amount or room size.")
                            index = 0
                            continue
                    break

    def add_hallway(self, hallway: Hallway):
        """Adds a hallway to the map.

        Args:
            hallway (Hallway): The hallway that will be added.
        """
        self.added_hallways.append(hallway)
        for coord in hallway.coords:
            self.cells[coord] = Cell(coord[0], coord[1], PATH_WEIGHT)

    def __str__(self) -> str:
        representation = f"\n Map size: Y{self.size_y} * X{self.size_x} \n"
        representation += f"Rooms: {len(self.placed_rooms)} \n"
        for index, room in enumerate(self.placed_rooms):
            representation += f"Room {index}: {room} \n"
        return representation
