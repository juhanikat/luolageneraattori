class Room:
    """Represents a room on the map. 
    Rooms have a length, a width and a location (x, y coordinate pair)."""

    def __init__(self, size_x: int, size_y: int) -> None:
        self.size_x = size_x
        self.size_y = size_y
        self.area = size_x*size_y
        self.bottom_left_coords = ()
        self.all_coords = []

    def get_all_coords(self):
        """Returns coordinates of all cells that make up the room.

        Returns:
            list: All coordinates in (x, y) format.
        """
        if len(self.all_coords) == 0:
            # sets self.all_coords if it hasn't been set yet
            coords = []
            for x in range(self.bottom_left_coords[0],
                           self.bottom_left_coords[0] + self.size_x):
                for y in range(self.bottom_left_coords[1],
                               self.bottom_left_coords[1] + self.size_y):
                    coords.append((x, y))
            self.all_coords = coords
        return self.all_coords

    def covers(self, coord: tuple) -> bool:
        """Checks if a cell at the given coordinate is part of the room.

        Args:
            coord (tuple): The coordinate to check.

        Returns:
            bool: True if coordinate is part of the room, and False otherwise.
        """
        coords = self.get_all_coords()
        return coord in coords

    def __str__(self) -> str:
        return f"coords: {self.bottom_left_coords}, size x: {self.size_x}, size y: {self.size_y}"
