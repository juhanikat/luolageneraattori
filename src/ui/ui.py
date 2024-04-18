import time
import tkinter as tk

import numpy as np
from matplotlib import pyplot
from matplotlib.patches import Rectangle

from entities.map import (Map, RoomAmountError, RoomPlacementError,
                          RoomSizeError)
from entities.room import Room
from services.generate import NoTrianglesError, generate_dungeon
from utilities import DEFAULT_ARGS, validate_int


class UI:

    def __init__(self) -> None:
        self.map = None
        self.root = tk.Tk()
        self.error_message = None
        self.run_button_text = tk.StringVar()
        self.create_ui()

    def change_run_button_text(self, text: str):
        self.run_button_text.set(text)

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
            self.change_run_button_text("Loading...")
            self.root.update_idletasks()
            self.map = Map(map_size_x, map_size_y, amount, room_min_size=room_min_size,
                           room_max_size=room_max_size)
            edges = generate_dungeon(self.map)
        except (ValueError, RoomAmountError, RoomSizeError, RoomPlacementError, NoTrianglesError) as exception:
            self.error_message.config(text=exception)
            self.change_run_button_text("Run")
            return
        if not edges:
            self.error_message.config(
                text="Dungeon cannot be generated with these parameters, try increasing amount of rooms.")
            self.change_run_button_text("Run")
            return

        display_map(self.map)
        self.change_run_button_text("Run")
        self.error_message.config(text="")

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

        self.run_button.pack()

    def start(self):
        self.root.mainloop()


def display_map(map: Map):
    start = time.time()
    pyplot.style.use("bmh")
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

    room: Room
    for room in map.placed_rooms:
        rectangle = Rectangle(room.bottom_left_coords,
                              room.size_x, room.size_y, fc=(1, 0, 0, 0.5), ec=(0, 0, 0, 0.1))
        axis.add_patch(rectangle)
    for hallway in map.added_hallways:
        for coord in hallway.coords:
            square = Rectangle(coord, 1, 1, fc=(0, 1, 0, 0.5))
            axis.add_patch(square)
    axis.add_patch(Rectangle((0, 0), map.get_size()[
                   0], map.get_size()[1], alpha=1, fill=True, edgecolor=(1, 0, 1, 0.6), facecolor="none"))
    print(f"drawing figure: {time.time() - start:.03f}")
    pyplot.show()
