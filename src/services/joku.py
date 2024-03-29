from algorithms import bowyer_watson, spanning_tree
from entities.map import Map
from utilities import convert_rooms_to_x_y_coords


def generate_dungeon(map: Map):
    x_y_coords = convert_rooms_to_x_y_coords(map.placed_rooms)
    triangles = bowyer_watson(x_y_coords)
    edges = []
    for triangle in triangles:
        edges.append(triangle.edge0)
        edges.append(triangle.edge1)
        edges.append(triangle.edge2)
    result = spanning_tree(edges)
    return result
