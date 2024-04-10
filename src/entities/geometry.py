"""The classes in this module are used by algorithms in algorithms.py."""
import math
import uuid


class BadTriangleError(Exception):
    """Raised if a triangle constructor is given 3 points that cannot be made into a triangle.
    """


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
        self.id = uuid.uuid4()
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

        self.circumcircle_radius = self.calculate_circumcircle_radius(
            self.edge0, self.edge1, self.edge2)

        self.circumcenter = self.calculate_circumcenter(v0, v1, v2)

    def calculate_circumcircle_radius(self, edge0: Edge, edge1: Edge, edge2: Edge):
        divisor = (math.sqrt(
            (edge0.length + edge1.length + edge2.length) *
            (edge1.length + edge2.length - edge0.length) *
            (edge2.length + edge0.length - edge1.length) *
            (edge0.length + edge1.length - edge2.length)))
        if divisor == 0:
            raise BadTriangleError(
                f"The vertices ({edge0}), ({edge1}), ({edge2}) \
                cannot be made into a triangle.")
        return (edge0.length * edge1.length * edge2.length) / divisor

    def calculate_circumcenter(self, v0: Vertex, v1: Vertex, v2: Vertex):
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
        return (ux, uy)

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