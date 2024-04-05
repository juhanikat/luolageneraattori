from algorithms import Edge, Vertex, spanning_tree


def test_triangle_turns_into_2_edges():
    edge1 = Edge(Vertex(0, 0), Vertex(0, 1))
    edge2 = Edge(Vertex(0, 0), Vertex(1, 1))
    edge3 = Edge(Vertex(0, 1), Vertex(1, 1))
    result = spanning_tree([edge1, edge2, edge3])
    assert len(result) == 2


def test_rectangle_turns_into_3_edges():
    edge1 = Edge(Vertex(0, 0), Vertex(0, 1))
    edge2 = Edge(Vertex(0, 0), Vertex(1, 0))
    edge3 = Edge(Vertex(0, 1), Vertex(1, 1))
    edge4 = Edge(Vertex(1, 1), Vertex(1, 0))
    result = spanning_tree([edge1, edge2, edge3, edge4])
    assert len(result) == 3


def test_linear_path_does_not_get_modified():
    edge1 = Edge(Vertex(0, 0), Vertex(0, 1))
    edge2 = Edge(Vertex(0, 1), Vertex(0, 3))
    edge3 = Edge(Vertex(0, 3), Vertex(5, 4))
    edge4 = Edge(Vertex(0, 0), Vertex(-5, 0))
    result = spanning_tree([edge1, edge2, edge3, edge4])
    assert len(result) == 4
