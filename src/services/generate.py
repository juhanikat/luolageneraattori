import random

from algorithms import (Edge, bowyer_watson, shortest_path_a_star,
                        shortest_path_dijkstra, spanning_tree)
from entities.hallway import Hallway
from entities.map import Map
from utilities import convert_rooms_to_x_y_coords

TRIANGULATION_TRIES = 10
EXTRA_EDGE_CHANCE = 10


class NoTrianglesError(Exception):
    """Raised if bowyer-watson algorithm could not generate the triangulation."""


def generate_dungeon(map: Map, extra_edges=True) -> list:
    """Generates a path through the dungeon that visits every room.
    This is done by: \n
    1. Creating a delaunay triangulation using the rooms on the map.
    2. Creating a spanning tree from the triangulation, removing unnecessary edges.
    3. Randomly adding some removed edges back into the spanning tree, 
    to make the resulting hallways look more natural.
    4. Converting the edges into hallways.
    5. Adding these hallways to the map.

    Args:
        map (Map): A Map object containing the rooms.

    Returns:
        list: The hallways that make up the path.
    """
    triangles = []
    tries = 0
    map.place_rooms()
    x_y_coords = convert_rooms_to_x_y_coords(map.placed_rooms)
    while not triangles:
        triangles = bowyer_watson(x_y_coords)
        if not triangles:
            map.place_rooms()
            x_y_coords = convert_rooms_to_x_y_coords(map.placed_rooms)
        tries += 1
        if tries == TRIANGULATION_TRIES:
            raise NoTrianglesError("Could not triangulate.")

    edges = []
    for triangle in triangles:
        edges.append(triangle.edge0)
        edges.append(triangle.edge1)
        edges.append(triangle.edge2)
    result = spanning_tree(edges)

    if extra_edges:
        for edge in edges:
            if random.randint(1, 100) <= EXTRA_EDGE_CHANCE and edge not in result:
                # chance to add removed edge back into the result
                result.append(edge)

    hallway: Hallway
    edge: Edge
    random.shuffle(result)
    added_hallways = []
    for edge in result:
        hallway = Hallway(shortest_path_a_star(map,
                                               map.cells[(
                                                   edge.v0.x, edge.v0.y)],
                                               map.cells[(edge.v1.x, edge.v1.y)]))
        map.add_hallway(hallway)
        added_hallways.append(hallway)

    return added_hallways
