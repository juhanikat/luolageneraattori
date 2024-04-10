from entities.geometry import Edge, Vertex
from services.turn_edge_to_hallway import turn_edge_to_hallway


def test_edge_gets_turned_into_correct_coords():
    edge = Edge(Vertex(0, 1), Vertex(4, 4))
    hallway = turn_edge_to_hallway(edge)
    assert hallway.coords == [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3),
                              (2, 4), (3, 4), (4, 4)]
    edge = Edge(Vertex(0, 2), Vertex(2, 1))
    hallway = turn_edge_to_hallway(edge)
    assert hallway.coords == [(0, 1), (0, 2), (1, 1), (2, 1)]
