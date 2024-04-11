import heapq
import random

from entities.cell import Cell
from entities.geometry import Edge, Triangle, Vertex
from entities.map import Map


def get_unique_edges(edges: list) -> list:
    """Takes a list of edges and filters out non-unique ones.
    Edges that share the same 2 vertices are not unique.

    Args:
        edges (list): The list of edges to filter.

    Returns:
        list: The filtered list of edges.
    """
    unique_edges = []

    for i, edge1 in enumerate(edges):
        unique = True
        for j, edge2 in enumerate(edges):
            if i != j and edge1 == edge2:
                unique = False
                break
        if unique:
            unique_edges.append(edge1)

    return unique_edges


def add_vertex_and_update(vertex: Vertex, triangles: list) -> list:
    """Adds a vertex to the triangulation and checks if it is inside any triangle's circumcircle.
    If so, it will remove those triangles and adds new triangles in their place that have the new vertex as one of their vertices.

    Args:
        vertex (Vertex): The vertex that will be added.
        triangles (list): All triangles in the triangulation so far.

    Returns:
        list: The updated triangles.
    """
    edges = []
    valid_triangles = []  # triangles that won't be deleted

    triangle: Triangle
    for triangle in triangles:
        if triangle.vertex_in_circumcircle(vertex):
            edges.append(triangle.edge0)
            edges.append(triangle.edge1)
            edges.append(triangle.edge2)
        else:
            valid_triangles.append(triangle)

    edges = get_unique_edges(edges)
    edge: Edge
    for edge in edges:
        valid_triangles.append(Triangle(edge.v0, edge.v1, vertex))

    return valid_triangles


def bowyer_watson(x_y_coords: list) -> list:
    """An implementation of the Bowyer-Watson algorithm.

    Args:
        vertices (list): List of (x, y) coordinates (representing rooms)
        that are added to the triangulation.

    Returns:
        list: List of triangles that are in the valid Delaunay triangulation.
    """
    # converts x,y coordinate pairs into Vertices
    vertices = []
    for coord in x_y_coords:
        vertices.append(Vertex(coord[0], coord[1]))

    # create a supertriangle that is big enough to include all vertices inside its circumcircle
    st = Triangle(Vertex(-2500000, -2500000),
                  Vertex(0, 2500000), Vertex(2500000, -2500000))

    # the list that will contain all our triangles
    triangles = [st]

    # adds vertices one at a time, and removes and adds triangles as needed
    for vertex in vertices:
        triangles = add_vertex_and_update(vertex, triangles)

    # remove supertriangle and all triangles sharing its vertices for the final result
    valid_triangles = [triangle for triangle in triangles if not (
        triangle.v0 == st.v0 or triangle.v0 == st.v1 or triangle.v0 == st.v2 or
        triangle.v1 == st.v0 or triangle.v1 == st.v1 or triangle.v1 == st.v2 or
        triangle.v2 == st.v0 or triangle.v2 == st.v1 or triangle.v2 == st.v2
    )]

    return valid_triangles


def search(edge: Edge, used_vertices: list, next_to: list, result: list) -> list:
    """Used by spanning_tree to remove unnecessary edges.

    Returns:
        list: The edges that are in the spanning tree.
    """
    if edge.v0 in used_vertices and edge.v1 in used_vertices:
        return None
    result.append(edge)
    used_vertices.append(edge.v0)
    used_vertices.append(edge.v1)
    for next_edge in next_to[edge.id]:
        search(next_edge, used_vertices, next_to, result)
    return result


def spanning_tree(edges: list) -> list:
    """Takes a list of edges and creates a non-looping path.

    Args:
        edges (list): The list of edges.

    Returns:
        list: The edges that are in the spanning tree.
    """
    if not edges:
        return None
    next_to = {}
    edge: Edge
    edge2: Edge
    for edge in edges:
        next_to[edge.id] = []
        for edge2 in edges:
            if edge.v0 == edge2.v0 \
                    or edge.v0 == edge2.v1 \
                    or edge.v1 == edge2.v0 \
                    or edge.v1 == edge2.v1:
                next_to[edge.id].append(edge2)
    return search(edges[0], [], next_to, [])


def shortest_path_dijkstra(map: Map, start_cell: Cell, end_cell: Cell) -> list:
    """Copied from TIRA 2024 course material with some changes. \n
    Calculates the shortest path between start_cell and end_cell. Going through rooms is expensive, and going through existing hallways is cheap.

    Args:
        start_cell (_type_): The cell where the algorithm starts.
        end_cell (_type_): The cell where the algorithm ends.

    Returns:
        list: A list of coordinate tuples that is the shortest path between the 2 cells.
    """
    cells = map.cells.values()
    distances = {}
    for cell in cells:
        distances[cell] = float("inf")

    distances[start_cell] = 0
    previous = {}
    previous[start_cell] = None

    queue = []
    heapq.heappush(queue, (0, start_cell))

    visited = set()
    while queue:
        cell1 = heapq.heappop(queue)[1]
        if cell1 in visited:
            continue
        visited.add(cell1)

        neighbor1 = map.get_cell((cell1.coords[0], cell1.coords[1] + 1))
        neighbor2 = map.get_cell(
            (cell1.coords[0], cell1.coords[1] - 1))
        neighbor3 = map.get_cell(
            (cell1.coords[0] + 1, cell1.coords[1]))
        neighbor4 = map.get_cell(
            (cell1.coords[0] - 1, cell1.coords[1]))
        neighbors = [neighbor1, neighbor2, neighbor3, neighbor4]
        # possibly makes hallway generation more natural
        random.shuffle(neighbors)

        for cell2 in neighbors:
            if cell2 is None:
                continue
            weight = cell2.weight
            new_distance = distances[cell1] + weight
            if new_distance < distances[cell2]:
                distances[cell2] = new_distance
                previous[cell2] = cell1
                new_pair = (new_distance, cell2)
                heapq.heappush(queue, new_pair)

    if distances[end_cell] == float("inf"):
        return None

    path = []
    cell = end_cell
    while cell:
        path.append(cell.coords)
        cell = previous[cell]

    path.reverse()
    return path
