from itertools import zip_longest

from algorithms import Edge


def turn_edge_to_hallway(edge: Edge):
    start = edge.v0
    end = edge.v1
    x_coords = list(range(start.x, end.x + 1))
    y_coords = list(range(start.y, end.y + 1))
    if len(x_coords) < len(y_coords):
        fill_value = x_coords[-1]
    elif len(x_coords) > len(y_coords):
        fill_value = y_coords[-1]
    else:
        fill_value = None
    return list(zip_longest(x_coords, y_coords, fillvalue=fill_value))
