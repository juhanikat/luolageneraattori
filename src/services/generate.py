import random

from algorithms import bowyer_watson, spanning_tree
from entities.map import Map
from utilities import convert_rooms_to_x_y_coords


def generate_dungeon(map: Map) -> list:
    """Generates a path through the dungeon that visits every room.
    This is done by: \n
    1. Creating a delaunay triangulation using the rooms on the map, \n
    2. Creating a spanning tree from the triangulation, removing unnecessary edges, 
    3. Randomly adding some removed edges back into the spanning tree, to make the resulting hallways look more natural.

    Args:
        map (Map): A Map object containing the rooms.

    Returns:
        list: The edges that make up the path.
    """
    x_y_coords = convert_rooms_to_x_y_coords(map.placed_rooms)
    triangles = bowyer_watson(x_y_coords)
    edges = []
    for triangle in triangles:
        edges.append(triangle.edge0)
        edges.append(triangle.edge1)
        edges.append(triangle.edge2)
    result = spanning_tree(edges)
    for edge in edges:
        if random.randint(1, 10) == 10 and edge not in result:
            # 10% chance to add removed edge back into the result
            result.append(edge)
    return result
