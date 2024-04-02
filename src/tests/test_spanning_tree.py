from algorithms import Edge, Vertex, spanning_tree


def test_triangle_turns_into_2_edges():
    edge1 = Edge(Vertex(0, 0), Vertex(0, 1))
    edge2 = Edge(Vertex(0, 0), Vertex(1, 1))
    edge3 = Edge(Vertex(0, 1), Vertex(1, 1))
    result = spanning_tree([edge1, edge2, edge3])
    assert len(result) == 2
