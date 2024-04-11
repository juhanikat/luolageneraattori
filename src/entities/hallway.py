class Hallway:
    """Connects rooms together."""

    def __init__(self, coords: list) -> None:
        self.coords = sorted(coords)
