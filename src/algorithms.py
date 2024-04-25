"""Various algorithms that are used in generating paths in the dungeon."""
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
    If so, it will remove those triangles and adds new triangles in their place 
    that have the new vertex as one of their vertices.

    Args:
        vertex (Vertex): The vertex that will be added.
        triangles (list): All triangles in the triangulation so far.

    Returns:
        list: The updated triangles.
    """
    edges = []
    valid_triangles = []

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

    x_coords = []
    y_coords = []
    for coord in x_y_coords:
        x_coords.append(coord[0])
        y_coords.append(coord[1])

    largest_x = max(x_coords)
    smallest_x = min(x_coords)
    largest_y = max(y_coords)
    smallest_y = min(y_coords)

    # create a supertriangle that is big enough to include all vertices inside its circumcircle
    st = Triangle(Vertex(smallest_x - 1000, smallest_y - 1000),
                  Vertex(0, largest_y + 1000), Vertex(largest_x + 1000, smallest_y - 1000))

    # the list that will contain all our triangles
    triangles = [st]

    # adds vertices one at a time, and removes and adds triangles as needed
    for vertex in vertices:
        triangles = add_vertex_and_update(vertex, triangles)

    st_vertices = [st.v0, st.v1, st.v2]
    # remove supertriangle and all triangles sharing its vertices for the final result
    valid_triangles = [triangle for triangle in triangles if not (
        triangle.v0 in st_vertices or triangle.v1 in st_vertices or triangle.v2 in st_vertices
    )]

    return valid_triangles


class UnionFind:
    """Used by kruskal's algorithm.
    Copied from TIRA 2024 course material.
    """

    def __init__(self, nodes: list):
        self.link = {node: None for node in nodes}
        self.size = {node: 1 for node in nodes}

    def find(self, x: Vertex):
        while self.link[x]:
            x = self.link[x]
        return x

    def union(self, a: Vertex, b: Vertex):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return

        if self.size[a] > self.size[b]:
            a, b = b, a
        self.link[a] = b
        self.size[b] += self.size[a]


def kruskal(nodes: list, edges: list) -> list:
    """Creates a minimum spanning tree.

    Args:
        nodes (list): List of nodes.
        edges (list): List of edges connecting the nodes.

    Returns:
        list: The minimum spanning tree.
    """
    edges.sort(key=lambda x: x.length)
    uf = UnionFind(nodes)
    tree_weight = 0
    result = []

    edge: Edge
    for edge in edges:
        node_a, node_b, weight = edge.v0, edge.v1, edge.length
        if uf.find(node_a) != uf.find(node_b):
            print(uf.find(node_a), uf.find(node_b))
            print(edge)
            uf.union(node_a, node_b)
            tree_weight += weight
            result.append(edge)

    return result


def shortest_path_a_star(map: Map, start_cell: Cell, end_cell: Cell) -> list:
    """Copied from TIRA 2024 course material with some changes. \n
    Calculates the shortest path between start_cell and end_cell. 
    Going through rooms is expensive, and going through existing hallways is cheap.

    Args:
        start_cell (Cell): The cell where the algorithm starts.
        end_cell (Cell): The cell where the algorithm ends.

    Returns:
        list: A list of coordinate tuples that is the shortest path between the 2 cells.
    """

    def heuristic(cell1: Cell, cell2: Cell):
        return abs((cell1.coords[0] - cell2.coords[0]) + (cell1.coords[1] - cell2.coords[1]))

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
        if cell1 is end_cell:
            break
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
                new_pair = (new_distance + heuristic(cell2, end_cell), cell2)
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
