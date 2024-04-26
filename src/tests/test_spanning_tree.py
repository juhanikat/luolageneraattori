import pytest

from algorithms import bowyer_watson, kruskal
from entities.geometry import Edge, Vertex


def test_triangle():
    edge1 = Edge(Vertex(0, 0), Vertex(0, 1))
    edge2 = Edge(Vertex(0, 0), Vertex(1, 1))
    edge3 = Edge(Vertex(0, 1), Vertex(1, 1))
    result = kruskal([edge1.v0, edge1.v1, edge2.v0, edge2.v1,
                     edge3.v0, edge3.v1], [edge1, edge2, edge3])
    assert len(result) == 3


def test_rectangle():
    edge1 = Edge(Vertex(0, 0), Vertex(0, 1))
    edge2 = Edge(Vertex(0, 0), Vertex(1, 0))
    edge3 = Edge(Vertex(0, 1), Vertex(1, 1))
    edge4 = Edge(Vertex(1, 1), Vertex(1, 0))
    result = kruskal([edge1.v0, edge1.v1, edge2.v0, edge2.v1, edge3.v0, edge3.v1, edge4.v0, edge4.v1], [
        edge1, edge2, edge3, edge4])
    assert len(result) == 4


def test_linear_path_does_not_get_modified():
    edge1 = Edge(Vertex(0, 0), Vertex(0, 1))
    edge2 = Edge(Vertex(0, 1), Vertex(0, 3))
    edge3 = Edge(Vertex(0, 3), Vertex(5, 4))
    edge4 = Edge(Vertex(0, 0), Vertex(-5, 0))
    result = kruskal([edge1.v0, edge1.v1, edge2.v0, edge2.v1, edge3.v0,
                     edge3.v1, edge4.v0, edge4.v1], [edge1, edge2, edge3, edge4])
    assert len(result) == 4
