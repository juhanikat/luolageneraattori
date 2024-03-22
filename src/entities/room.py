class Room():

    def __init__(self, size_x, size_y) -> None:
        self.size_x = size_x
        self.size_y = size_y
        self.area = size_x*size_y
        self.bottom_left_coords = None  # (X, Y)

    def get_all_coords(self):
        coords = []
        for x in range(self.bottom_left_coords[0], self.bottom_left_coords[0] + self.size_x):
            for y in range(self.bottom_left_coords[1], self.bottom_left_coords[1] + self.size_y):
                coords.append((x, y))
        return coords

    def covers(self, coord: tuple):
        coords = self.get_all_coords()
        return coord in coords

    def __str__(self) -> str:
        return f"bottom left {self.bottom_left_coords}, size x: {self.size_x}, size y: {self.size_y}"
