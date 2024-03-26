import tkinter as tk
from entities.map import Map, RoomAmountError, RoomSizeError, RoomPlacementError
from bowyer import bowyer_watson
from utilities import display_figure, convert_rooms_to_x_y_coords, validate_int, DEFAULT_ARGS


class UI:

    def __init__(self, map: Map) -> None:
        self.map = map
        self.root = tk.Tk()
        self.error_message = None
        self.create_ui()

    def handle_button_click(self, amount,
                            room_min_size,
                            room_max_size):
        try:
            amount = validate_int("Amount", amount)
            if room_min_size.strip() == "":
                room_min_size = DEFAULT_ARGS["room_min_size"]
            if room_max_size.strip() == "":
                room_max_size = DEFAULT_ARGS["room_max_size"]

                amount = int(amount)
                room_min_size = int(room_min_size)
                room_max_size = int(room_max_size)
                self.map.place_rooms(
                    amount=amount, room_min_size=room_min_size, room_max_size=room_max_size)
        except ValueError as exception:
            self.error_message.config(
                text=exception)
            return
        except (RoomAmountError, RoomSizeError, RoomPlacementError) as exception:
            self.error_message.config(text=exception)
            return
        rooms = self.map.placed_rooms
        x_y_coords = convert_rooms_to_x_y_coords(rooms)
        triangles = bowyer_watson(x_y_coords)
        display_figure(triangles, rooms, (self.map.size_x, self.map.size_y))

    def create_ui(self):
        amount = tk.StringVar(self.root)
        room_min_size = tk.StringVar(self.root)
        room_max_size = tk.StringVar(self.root)

        self.error_message = tk.Label(self.root, text="")

        amount_label = tk.Label(self.root, text="Amount of rooms")
        room_min_size_label = tk.Label(
            self.root, text=f'Minimum room size (default: {DEFAULT_ARGS["room_min_size"]})')
        room_max_size_label = tk.Label(
            self.root, text=f'Maximum room size (default: {DEFAULT_ARGS["room_max_size"]})')

        amount_entry = tk.Entry(self.root, textvariable=amount)
        room_min_size_entry = tk.Entry(self.root, textvariable=room_min_size)
        room_max_size_entry = tk.Entry(self.root, textvariable=room_max_size)

        self.error_message.pack()
        amount_label.pack()
        amount_entry.pack()
        room_min_size_label.pack()
        room_min_size_entry.pack()
        room_max_size_label.pack()
        room_max_size_entry.pack()

        button = tk.Button(self.root, text="Run",
                           command=lambda: self.handle_button_click(amount.get(), room_min_size.get(), room_max_size.get()))
        button.pack()

    def start(self):
        self.root.mainloop()
