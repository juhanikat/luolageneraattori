class Cell:
    """Represents a square on the map. 
    Cells are compared to each other by using their weight.
    """

    def __init__(self, x: int, y: int, weight=1) -> None:
        """Represents a square on the map. 

        Args:
            x (int): x-coordinate of the cell.
            y (int): y-coordinate of the cell.
            weight (int, optional): The weight of the cell,
            used by pathfinding algorithms to decide whether to go through the cell or not. Defaults to 1.
        """
        self.coords = (x, y)
        self.weight = weight

    def __lt__(self, other: object):
        return self.weight < other.weight
