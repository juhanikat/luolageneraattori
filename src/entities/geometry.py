"""The classes in this module are used by algorithms in algorithms.py."""
import math
import uuid


class BadTriangleError(Exception):
    """Raised if a triangle constructor is given 3 points that cannot be made into a triangle."""


class Vertex:
    """Represents a node in the network."""

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __str__(self) -> str:
        return f"x: {self.x} y: {self.y}"


class Edge:
    """Represents a line that connects two vertices together.
    Two edges are equal if they share the same 2 vertices.

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
    # TODO

    def __init__(self, v0: Vertex, v1: Vertex, v2: Vertex) -> None:
        """A triangle between 3 vertices.

        Args:
            v0 (Vertex): First vertex.
            v1 (Vertex): Second vertex.
            v2 (Vertex): Third vertex.

        Raises:
            BadTriangleError: Raised if all vertices have the same x- or y-coordinate,
            because a triangle cannot be formed then.
        """
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2

        if (v0.x == v1.x == v2.x) or (v0.y == v1.y == v2.y):
            raise BadTriangleError(
                f"The vertices ({v0}), ({v1}), ({v2}) \
                cannot be made into a triangle, \
                because they all have the same x - or y-coordinates.")
        self.edge0 = Edge(v0, v1)
        self.edge1 = Edge(v1, v2)
        self.edge2 = Edge(v2, v0)

        self.circumcircle_radius = self.calculate_circumcircle_radius(
            self.edge0, self.edge1, self.edge2)

        self.circumcenter = self.calculate_circumcenter(v0, v1, v2)

    def calculate_circumcircle_radius(self, edge0: Edge, edge1: Edge, edge2: Edge) -> float:
        """Calculates the radius of the circumcircle of the triangle. 
        A circumcircle is a circle drawn through the 3 vertices of the triangle.

        Args:
            edge0(Edge): First edge of triangle.
            edge1(Edge): Second edge of triangle.
            edge2(Edge): Third edge of triangle.

        Returns:
            float: The radius of the circumcircle.
        """
        divisor = (math.sqrt(
            (edge0.length + edge1.length + edge2.length) *
            (edge1.length + edge2.length - edge0.length) *
            (edge2.length + edge0.length - edge1.length) *
            (edge0.length + edge1.length - edge2.length)))
        return (edge0.length * edge1.length * edge2.length) / divisor

    def calculate_circumcenter(self, v0: Vertex, v1: Vertex, v2: Vertex) -> tuple:
        """Calculates the circumcenter of the triangle's circumcircle.
        A circumcircle is a circle drawn through the 3 vertices of the triangle.

        Args:
            v0(Vertex): First vertex of triangle.
            v1(Vertex): Second vertex of triangle.
            v2(Vertex): Third vertex of triangle.

        Returns:
            tuple: The coordinates of the circumcenter in (x, y) format.
        """
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

    def vertex_in_circumcircle(self, vertex: Vertex) -> bool:
        """Checks if a given vertex is in the circumcircle of this triangle.

        Args:
            vertex(Vertex): The vertex that is checked.

        Returns:
            bool: True if vertex is inside the circumcircle, and False otherwise.
        """
        dx = self.circumcenter[0] - vertex.x
        dy = self.circumcenter[1] - vertex.y
        return math.sqrt(dx * dx + dy * dy) <= self.circumcircle_radius

    def __str__(self) -> str:
        return f"Edges: \n {self.edge0} \n {self.edge1} \n {self.edge2}"
