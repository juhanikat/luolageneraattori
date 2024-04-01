import math
import random


class Vertex:
    """This represents a node in the network."""

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __str__(self) -> str:
        return f"x: {self.x} y: {self.y}"


class Edge:
    """This represents a line in the network that connects two vertices together.

        Attributes:
            v0 (Vertex): First vertex.
            v1 (Vertex): Second vertex.
            length (float): Length of the edge.
    """

    def __init__(self, v0: Vertex, v1: Vertex) -> None:
        """
        Args:
            v0 (Vertex): First vertex.
            v1 (Vertex): Second vertex.
        """
        self.id = random.randint(0, 999999999)
        self.v0 = v0
        self.v1 = v1
        self.length = math.sqrt(
            ((self.v0.x - self.v1.x)**2 + (self.v0.y - self.v1.y)**2))

    def __eq__(self, other) -> bool:
        return (self.v0 == other.v0 and self.v1 == other.v1) or \
            (self.v0 == other.v1 and self.v1 == other.v0)

    def __str__(self) -> str:
        return f"length: {self.length} vertex 0: {self.v0} vertex 1: {self.v1}"


class Triangle:
    """A triangle between 3 vertices.

        Attributes:
            lots
    """

    def __init__(self, v0: Vertex, v1: Vertex, v2: Vertex) -> None:
        """A triangle between 3 vertices.

        Args:
            v0 (Vertex): First vertex.
            v1 (Vertex): Second vertex.
            v2 (Vertex): Third vertex.
        """
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        self.edge0 = Edge(v0, v1)
        self.edge1 = Edge(v1, v2)
        self.edge2 = Edge(v2, v0)

        edge0_length = self.edge0.length
        edge1_length = self.edge1.length
        edge2_length = self.edge2.length

        divisor = (math.sqrt(
            (edge0_length + edge1_length + edge2_length) *
            (edge1_length + edge2_length - edge0_length) *
            (edge2_length + edge0_length - edge1_length) *
            (edge0_length + edge1_length - edge2_length)))
        if divisor == 0:
            print("Divisor in triangle is zero!")
            print(self)
            print(f"divisor: {divisor}")
            exit()
        self.circumcircle_radius = (
            edge0_length * edge1_length * edge2_length) / divisor

        ax = v0.x
        ay = v0.y
        bx = v1.x
        by = v1.y
        cx = v2.x
        cy = v2.y
        d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
        ux = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by)
              * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
        uy = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by)
              * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
        self.circumcenter = (ux, uy)

    def vertex_in_circumcirc(self, vertex: Vertex) -> bool:
        """Checks if a given vertex is in the circumcircle of this triangle.

        Args:
            vertex (Vertex): The vertex that is checked.

        Returns:
            _type_: True if vertex is inside the circumcircle, and False otherwise.
        """
        dx = self.circumcenter[0] - vertex.x
        dy = self.circumcenter[1] - vertex.y
        return math.sqrt(dx * dx + dy * dy) <= self.circumcircle_radius

    def __str__(self) -> str:
        return f"vertices: \n {self.v0} \n {self.v1} \n {self.v2} \n edges: \n {self.edge0} \n {self.edge1} \n {self.edge2} \n"


def get_unique_edges(edges: list) -> list:
    """Takes a list of edges and filters out non-unique ones.

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
        if triangle.vertex_in_circumcirc(vertex):
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
    """_summary_

    Args:
        edge (Edge): _description_
        used_vertices (list): _description_
        next_to (list): _description_
        result (list): _description_

    Returns:
        list: _description_
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
    next_to = {}
    for edge in edges:
        next_to[edge.id] = []
        for edge2 in edges:
            if edge.v0 == edge2.v0 \
                    or edge.v0 == edge2.v1 \
                    or edge.v1 == edge2.v0 \
                    or edge.v1 == edge2.v1:
                next_to[edge.id].append(edge2)
    return search(edges[0], [], next_to, [])
