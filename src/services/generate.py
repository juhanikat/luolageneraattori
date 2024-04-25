import random

from algorithms import Edge, bowyer_watson, kruskal, shortest_path_a_star
from entities.hallway import Hallway
from entities.map import Map

TRIANGULATION_TRIES = 10
EXTRA_EDGE_CHANCE = 5


class NoTrianglesError(Exception):
    """Raised if bowyer-watson algorithm could not generate the triangulation."""


def convert_rooms_to_x_y_coords(rooms: list) -> list:
    """Takes a list of room objects and converts them to the x, y coordinates of the rooms.

    Args:
        rooms (list): Rooms to convert.

    Returns:
        list: A list of (x, y) coordinates.
    """
    coords = []
    for room in rooms:
        coords.append(room.bottom_left_coords)
    return coords


def generate_dungeon(map: Map, extra_edges=True) -> list:
    """Generates a path through the dungeon that visits every room.
    This is done by: \n
    1. Creating a delaunay triangulation using the rooms on the map.
    2. Creating a minimum spanning tree from the triangulation, removing unnecessary edges.
    3. Randomly adding some removed edges back into the graph, 
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
            raise NoTrianglesError("Could not triangulate, try again.")

    vertices = []
    edges = []
    for triangle in triangles:
        vertices.append(triangle.edge0.v0)
        vertices.append(triangle.edge0.v1)
        vertices.append(triangle.edge1.v0)
        vertices.append(triangle.edge1.v1)
        vertices.append(triangle.edge2.v0)
        vertices.append(triangle.edge2.v1)
        edges.append(triangle.edge0)
        edges.append(triangle.edge1)
        edges.append(triangle.edge2)

    result = kruskal(vertices, edges)

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
