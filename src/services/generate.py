import random
import time

from algorithms import BellmanFord, Edge, Vertex, bowyer_watson, spanning_tree
from entities.hallway import Hallway
from entities.map import Map
from utilities import convert_rooms_to_x_y_coords

from .turn_edge_to_hallway import NoLengthError, turn_edge_to_hallway


def generate_dungeon(map: Map) -> list:
    """Generates a path through the dungeon that visits every room.
    This is done by: \n
    1. Creating a delaunay triangulation using the rooms on the map, \n
    2. Creating a spanning tree from the triangulation, removing unnecessary edges, 
    3. Randomly adding some removed edges back into the spanning tree, to make the resulting hallways look more natural.
    4. Converting the edges into hallways.
    5. Adding these hallways to the map object.

    Args:
        map (Map): A Map object containing the rooms.

    Returns:
        list: The hallways that make up the path.
    """
    start = time.time()
    x_y_coords = convert_rooms_to_x_y_coords(map.placed_rooms)
    print(f"convert rooms to x, y: {time.time()-start:.03f}")
    start = time.time()
    triangles = bowyer_watson(x_y_coords)
    print(f"bowyer-watson: {time.time()-start:.03f}")
    edges = []
    for triangle in triangles:
        edges.append(triangle.edge0)
        edges.append(triangle.edge1)
        edges.append(triangle.edge2)
    start = time.time()
    result = spanning_tree(edges)
    print(f"spanning tree: {time.time()-start:.03f}")
    for edge in edges:
        if random.randint(1, 10) == 10 and edge not in result:
            # 10% chance to add removed edge back into the result
            # result.append(edge)
            pass
    hallways = []
    b = BellmanFord(map)
    hallway: Hallway
    edge: Edge
    random.shuffle(result)
    start = time.time()
    for edge in result:
        """
        try:
            hallway = turn_edge_to_hallway(edge)
            hallways.append(hallway)
        except NoLengthError as exception:
            print(exception)

    for hallway in hallways:
        map.add_hallway(hallway)
        """

        hallway = Hallway(b.shortest_path(
            map.cells[(edge.v0.x, edge.v0.y)], map.cells[(edge.v1.x, edge.v1.y)]))
        hallways.append(hallway)
    print(f"calculating shortest paths: {time.time()-start:.03f}")
    start = time.time()
    for hallway in hallways:
        map.add_hallway(hallway)
    print(f"adding hallways to map: {time.time()-start:.03f}")
    return hallways
