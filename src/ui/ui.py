import tkinter as tk
from entities.map import Map, RoomAmountError, RoomSizeError, RoomPlacementError
from bowyer import bowyer_watson
from utilities import display_figure, convert_rooms_to_x_y_coords


class UI:

    def __init__(self,  map: Map) -> None:
        self.map = map
        self.root = tk.Tk()
        self.error_message = None
        self.create_ui()

    def handle_button_click(self, amount):
        if type(amount) != int:
            return
        try:
            self.map.place_rooms(amount=amount)
        except (RoomAmountError, RoomSizeError, RoomPlacementError) as exception:
            print(exception)
            self.error_message.text = exception
            return
        rooms = self.map.placed_rooms
        x_y_coords = convert_rooms_to_x_y_coords(rooms)
        triangles = bowyer_watson(x_y_coords)
        display_figure(triangles, rooms, (self.map.size_x, self.map.size_y))

    def create_ui(self):
        amount = tk.IntVar(self.root)
        self.error_message = tk.Label(self.root, text="")
        self.error_message.pack()
        label = tk.Label(self.root, text="Amount of rooms")
        label.pack()
        entry = tk.Entry(self.root, textvariable=amount)
        entry.pack()

        button = tk.Button(self.root, text="Run",
                           command=lambda: self.handle_button_click(amount.get()))
        button.pack()

    def start(self):
        self.root.mainloop()
