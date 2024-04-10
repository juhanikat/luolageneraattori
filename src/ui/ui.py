import tkinter as tk

from matplotlib import pyplot
from matplotlib.patches import Rectangle

from entities.map import (Map, RoomAmountError, RoomPlacementError,
                          RoomSizeError)
from entities.room import Room
from services.generate import generate_dungeon
from utilities import DEFAULT_ARGS, validate_int


class UI:

    def __init__(self) -> None:
        self.map = Map(20, 20)
        self.root = tk.Tk()
        self.error_message = None
        self.create_ui()

    def handle_button_click(self, amount,
                            room_min_size,
                            room_max_size,
                            map_size_x,
                            map_size_y):
        if room_min_size.strip() == "":
            room_min_size = DEFAULT_ARGS["room_min_size"]
        if room_max_size.strip() == "":
            room_max_size = DEFAULT_ARGS["room_max_size"]
        if map_size_x.strip() == "":
            map_size_x = DEFAULT_ARGS["map_size_x"]
        if map_size_y.strip() == "":
            map_size_y = DEFAULT_ARGS["map_size_y"]
        try:
            amount = validate_int("Amount", amount)
            room_min_size = validate_int("Minimum room size", room_min_size)
            room_max_size = validate_int("Maximum room size", room_max_size)
            map_size_x = validate_int("Map size x", map_size_x)
            map_size_y = validate_int("Map size y", map_size_y)
            self.map = Map(map_size_x, map_size_y)
            self.map.place_rooms(
                amount=amount,
                room_min_size=room_min_size,
                room_max_size=room_max_size)

        except ValueError as exception:
            self.error_message.config(
                text=exception)
            return
        except (ValueError, RoomAmountError, RoomSizeError, RoomPlacementError) as exception:
            self.error_message.config(text=exception)
            return
        edges = generate_dungeon(self.map)
        if not edges:
            self.error_message.config(
                text="Dungeon cannot be generated with these parameters, try increasing amount of rooms.")

        display_map(self.map)

    def create_ui(self):
        amount = tk.StringVar(self.root)
        room_min_size = tk.StringVar(self.root)
        room_max_size = tk.StringVar(self.root)
        map_size_x = tk.StringVar(self.root)
        map_size_y = tk.StringVar(self.root)

        self.error_message = tk.Label(self.root, text="")

        amount_label = tk.Label(self.root, text="Amount of rooms")
        room_min_size_label = tk.Label(
            self.root, text=f'Minimum room size (default: {DEFAULT_ARGS["room_min_size"]})')
        room_max_size_label = tk.Label(
            self.root, text=f'Maximum room size (default: {DEFAULT_ARGS["room_max_size"]})')
        map_size_x_label = tk.Label(
            self.root, text=f'X size of map (default: {DEFAULT_ARGS["map_size_x"]})')
        map_size_y_label = tk.Label(
            self.root, text=f'Y size of map (default: {DEFAULT_ARGS["map_size_y"]})')

        amount_entry = tk.Entry(self.root, textvariable=amount)
        room_min_size_entry = tk.Entry(self.root, textvariable=room_min_size)
        room_max_size_entry = tk.Entry(self.root, textvariable=room_max_size)
        map_size_x_entry = tk.Entry(self.root, textvariable=map_size_x)
        map_size_y_entry = tk.Entry(self.root, textvariable=map_size_y)

        self.error_message.pack()
        amount_label.pack()
        amount_entry.pack()
        room_min_size_label.pack()
        room_min_size_entry.pack()
        room_max_size_label.pack()
        room_max_size_entry.pack()
        map_size_x_label.pack()
        map_size_x_entry.pack()
        map_size_y_label.pack()
        map_size_y_entry.pack()

        button = tk.Button(self.root, text="Run",
                           command=lambda: self.handle_button_click(
                               amount.get(),
                               room_min_size.get(),
                               room_max_size.get(),
                               map_size_x.get(),
                               map_size_y.get()))
        button.pack()

    def start(self):
        self.root.mainloop()


def display_map(map: Map):
    _, axis = pyplot.subplots(1, ncols=1)
    pyplot.grid(True, which="both", linestyle="--", alpha=0.5)
    pyplot.gca().set_aspect('equal')
    pyplot.minorticks_on()
    pyplot.xlim(-10, map.get_size()[0] + 10)
    pyplot.ylim(-10, map.get_size()[1] + 10)

    room: Room
    for room in map.placed_rooms:
        rectangle = Rectangle(room.bottom_left_coords,
                              room.size_x, room.size_y, fc=(0, 0, 0, 0.1), ec=(0, 0, 0, 0.1))
        axis.add_patch(rectangle)
    for hallway in map.added_hallways:
        for coord in hallway.coords:
            square = Rectangle(coord, 1, 1, fc=(0, 1, 0, 0.5))
            axis.add_patch(square)

    pyplot.show()
