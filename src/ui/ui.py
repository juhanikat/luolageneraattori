import tkinter as tk

import numpy as np
from matplotlib import pyplot
from matplotlib.patches import Rectangle

from entities.hallway import Hallway
from entities.map import (Map, RoomAmountError, RoomPlacementError,
                          RoomSizeError)
from entities.room import Room
from services.generate import NoTrianglesError, generate_dungeon
from values import (DEFAULT_ARGS, MAX_AMOUNT_OF_ROOMS, MAX_MAP_SIZE_X,
                    MAX_MAP_SIZE_Y)


def validate_int(name: str, checked: str) -> int:
    """Checks that an input is not empty, can be converted to an integer, and is not less than 1.

    Args:
        name (str): Used to identify the problem in error message.
        checked (str): The input string to validate.

    Raises:
        ValueError: If any of the checks fail.

    Returns:
        int: Input value as an integer.
    """
    if checked.strip() == "":
        raise ValueError(f"{name} must not be empty.")
    try:
        checked = int(checked)
    except ValueError as exception:
        raise ValueError(f"{name} must be a number.") from exception
    if checked < 1:
        raise ValueError(f"{name} cannot be less than 1.")
    return checked


class UI:

    def __init__(self) -> None:
        self.map = None
        self.root = tk.Tk()
        self.error_message = None
        self.run_button_text = tk.StringVar()
        self.create_ui()

    def change_run_button_text(self, text: str):
        self.run_button_text.set(text)

    def change_error_text(self, text: str):
        self.error_message.config(text=text, fg="red")

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
            if amount > MAX_AMOUNT_OF_ROOMS:
                raise ValueError(
                    f"The maximum amount of rooms is {MAX_AMOUNT_OF_ROOMS}.")
            room_min_size = validate_int("Minimum room size", room_min_size)
            room_max_size = validate_int("Maximum room size", room_max_size)
            map_size_x = validate_int("Map size x", map_size_x)
            map_size_y = validate_int("Map size y", map_size_y)
            if map_size_x * map_size_y > MAX_MAP_SIZE_X * MAX_MAP_SIZE_Y:
                raise ValueError(
                    f"Map size cannot be larger than {MAX_MAP_SIZE_X}x{MAX_MAP_SIZE_Y}.")
            self.change_error_text("")
            self.change_run_button_text("Loading...")
            self.root.update_idletasks()
            self.map = Map(map_size_x, map_size_y, amount, room_min_size=room_min_size,
                           room_max_size=room_max_size)
            edges = generate_dungeon(self.map)
        except (ValueError, RoomAmountError, RoomSizeError, RoomPlacementError, NoTrianglesError) as exception:
            self.change_error_text(exception)
            self.change_run_button_text("Run")
            return
        if not edges:
            self.change_error_text(
                "Dungeon cannot be generated with these parameters, try increasing amount of rooms.")
            self.change_run_button_text("Run")
            return

        display_map(self.map)
        self.change_run_button_text("Run")
        self.change_error_text("")

    def create_ui(self):
        amount = tk.StringVar(self.root)
        room_min_size = tk.StringVar(self.root)
        room_max_size = tk.StringVar(self.root)
        map_size_x = tk.StringVar(self.root)
        map_size_y = tk.StringVar(self.root)

        self.change_run_button_text("Run")
        self.error_message = tk.Label(self.root, text="")
        self.run_button = tk.Button(self.root, textvariable=self.run_button_text,
                                    command=lambda: self.handle_button_click(
                                        amount.get(),
                                        room_min_size.get(),
                                        room_max_size.get(),
                                        map_size_x.get(),
                                        map_size_y.get()))

        amount_label = tk.Label(
            self.root, text=f"Amount of rooms (max: {MAX_AMOUNT_OF_ROOMS})")
        room_min_size_label = tk.Label(
            self.root, text=f'Minimum room size (default: {DEFAULT_ARGS["room_min_size"]})')
        room_max_size_label = tk.Label(
            self.root, text=f'Maximum room size (default: {DEFAULT_ARGS["room_max_size"]})')
        map_size_x_label = tk.Label(
            self.root, text=f'X size of map (default: {DEFAULT_ARGS["map_size_x"]}, max: {MAX_MAP_SIZE_X})')
        map_size_y_label = tk.Label(
            self.root, text=f'Y size of map (default: {DEFAULT_ARGS["map_size_y"]}, max: {MAX_MAP_SIZE_Y})')
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

        self.run_button.pack()

    def start(self):
        self.root.mainloop()


def display_map(map: Map):
    pyplot.style.use("Solarize_Light2")
    map_width = map.get_size()[0]
    map_height = map.get_size()[1]
    figure = pyplot.figure()
    figure.canvas.manager.set_window_title(
        f"Dungeon {map_width}x{map_height}, {len(map.placed_rooms)} rooms")
    axis = figure.add_subplot(1, 1, 1)
    axis.set_aspect('equal')
    axis.set_xlim(0, map_width)
    axis.set_ylim(0, map_height)
    larger_dimension = max(map_width, map_height)
    major_ticks = np.arange(0, larger_dimension, 20)
    minor_ticks = np.arange(0, larger_dimension, 1)
    axis.set_xticks(major_ticks)
    axis.set_xticks(minor_ticks, minor=True)
    axis.set_yticks(major_ticks)
    axis.set_yticks(minor_ticks, minor=True)
    axis.grid(which='both')
    axis.grid(which='minor', alpha=0.2)
    axis.grid(which='major', alpha=0.5)

    hallway: Hallway
    for hallway in map.added_hallways:
        for coord in hallway.coords:
            square = Rectangle(coord, 1, 1, fc=(1, 0.4, 0.4, 1))
            axis.add_patch(square)

    room: Room
    for room in map.placed_rooms:
        rectangle = Rectangle(room.bottom_left_coords,
                              room.size_x, room.size_y, fc=(0.3, 0.3, 0.3, 1))
        door = Rectangle(room.bottom_left_coords, 1, 1, fc=(0.3, 0.3, 0.7, 1))
        axis.add_patch(rectangle)
        axis.add_patch(door)

    # Adds a rectangle showing the map's limits
    axis.add_patch(Rectangle((0, 0), map.get_size()[
                   0], map.get_size()[1], alpha=1, fill=True, edgecolor=(1, 0, 1, 0.6), facecolor="none"))
    pyplot.show()
