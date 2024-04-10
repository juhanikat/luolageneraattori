from algorithms import Edge
from entities.hallway import Hallway


class NoLengthError(Exception):
    """Raised if length of the edge is zero."""


def turn_edge_to_hallway(edge: Edge) -> list:
    start = edge.v0
    end = edge.v1
    if start.x > end.x:
        first = -1
        first2 = -1
    else:
        first = 1
        first2 = 1
    if start.y > end.y:
        second = -1
        second2 = -1
    else:
        second = 1
        second2 = 1

    x_coords = list(range(start.x, end.x+first2, first))
    y_coords = list(range(start.y, end.y+second2, second))

    if len(y_coords) == 0 and len(x_coords) == 0:
        raise NoLengthError(f"The edge seems to have a length of zero: {edge}")
    if len(y_coords) == 0:
        return [(x, start.y) for x in x_coords]
    if len(x_coords) == 0:
        return [(start.x, y) for y in y_coords]

    result = []
    ix = 0
    iy = 0
    result.append((x_coords[ix], y_coords[iy]))
    while True:
        if iy != len(y_coords) - 1:
            iy += 1
            result.append((x_coords[ix], y_coords[iy]))
        if ix != len(x_coords)-1:
            ix += 1
            result.append((x_coords[ix], y_coords[iy]))
        if ix == len(x_coords) - 1 and iy == len(y_coords) - 1:
            break

    return Hallway(result)
