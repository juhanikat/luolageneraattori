class Cell:

    def __init__(self, x: int, y: int, weight=1) -> None:
        self.coords = (x, y)
        self.weight = weight

    def __repr__(self) -> str:
        return f"coords: {self.coords} weight: {self.weight}"

    def __lt__(self, other):
        return self.weight < other.weight
