class Hallway:
    """Connects rooms together."""

    def __init__(self, coords: list) -> None:
        """Connects rooms together.

        Args:
            coords (list): List of coordinates in (x, y) format that make up the hallway.
        """
        self.coords = sorted(coords)
