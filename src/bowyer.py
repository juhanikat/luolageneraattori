import math


class Vertex:

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y


class Edge:

    def __init__(self, v0: Vertex, v1: Vertex) -> None:
        self.v0 = v0
        self.v1 = v1
        self.length = math.sqrt(
            ((self.v0.x - self.v1.x)**2 + (self.v0.y - self.v1.y)**2))

    def __eq__(self, other) -> bool:
        return (self.v0 == other.v0 and self.v1 == other.v1) or \
            (self.v0 == other.v1 and self.v1 == other.v0)


class Triangle:

    def __init__(self, v0: Vertex, v1: Vertex, v2: Vertex) -> None:
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        self.edge0 = Edge(v0, v1)
        self.edge1 = Edge(v1, v2)
        self.edge2 = Edge(v2, v0)

        edge0_length = self.edge0.length
        edge1_length = self.edge1.length
        edge2_length = self.edge2.length
        self.circumcircle_radius = (
            edge0_length * edge1_length * edge2_length) / (math.sqrt(
                (edge0_length + edge1_length + edge2_length) *
                (edge1_length + edge2_length - edge0_length) *
                (edge2_length + edge0_length - edge1_length) *
                (edge0_length + edge1_length - edge2_length)))
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

    def vertex_in_circumcirc(self, vertex: Vertex):
        dx = self.circumcenter[0] - vertex.x
        dy = self.circumcenter[1] - vertex.y
        return math.sqrt(dx * dx + dy * dy) <= self.circumcircle_radius


def get_unique_edges(edges: list):
    unique_edges = []

    for i in range(len(edges)):
        unique = True
        for j in range(len(edges)):
            if i != j and edges[i] == edges[j]:
                unique = False
                break
        if unique:
            unique_edges.append(edges[i])

    return unique_edges


def add_vertex_and_update(vertex: Vertex, triangles: list) -> list:
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
    Implemented with the help this tutorial: 
    https://www.gorillasun.de/blog/bowyer-watson-algorithm-for-delaunay-triangulation/#an-intuitive-explanation-of-the-algorithm

    Args:
        vertices (list): List of vertices (points) that are added to the triangulation.

    Returns:
        list: List of triangles that are in the valid Delaunay triangulation.
    """

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
