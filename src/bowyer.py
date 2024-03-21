import math
from matplotlib import pyplot
import random


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

    print(len(valid_triangles))
    return valid_triangles


def main(vertices: list):
    st = Triangle(Vertex(-2000000, -2000000),
                  Vertex(0, 2000000), Vertex(2000000, -2000000))

    triangles = [st]

    for vertex in vertices:
        triangles = add_vertex_and_update(vertex, triangles)
    print(len(triangles))
    triangles = [triangle for triangle in triangles if not (
        triangle.v0 == st.v0 or triangle.v0 == st.v1 or triangle.v0 == st.v2 or
        triangle.v1 == st.v0 or triangle.v1 == st.v1 or triangle.v1 == st.v2 or
        triangle.v2 == st.v0 or triangle.v2 == st.v1 or triangle.v2 == st.v2
    )]
    print(len(triangles))
    pyplot.ion()
    for triangle in triangles:
        pyplot.plot([triangle.v0.x, triangle.v1.x, triangle.v2.x, triangle.v0.x],
                    [triangle.v0.y, triangle.v1.y, triangle.v2.y, triangle.v0.y])
        pyplot.pause(0.5)
    # pyplot.plot([st.v0.x, st.v1.x, st.v2.x, st.v0.x],
        # [st.v0.y, st.v1.y, st.v2.y, st.v0.y])
    # pyplot.xticks(range(-1000000, 1000000, 100000))
    pyplot.pause(0.5)
    pyplot.ioff()
    pyplot.show()


if __name__ == "__main__":
    vertices = []
    for i in range(20):
        vertex = Vertex(random.randint(-7000000, 7000000),
                        random.randint(-7000000, 7000000))
        vertices.append(vertex)
    main(vertices)
