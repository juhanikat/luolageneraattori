from algorithms import bowyer_watson


def test_3_rooms_results_in_one_triangle():
    triangles = bowyer_watson([(0, 0), (10, 10), (0, 5)])
    assert len(triangles) == 1
    triangles = bowyer_watson([(0, 0), (1, 2), (2, 2)])
    assert len(triangles) == 1


def test_thousand_rooms():
    coords = []
    for i in range(1000):
        x = i
        y = i**2
        coords.append((x, y))
    triangles = bowyer_watson(coords)
    assert len(triangles) == 512


def test_rooms_that_are_on_the_same_line_result_in_0_triangles():
    triangles = bowyer_watson([(0, 0), (10, 0), (56, 0)])
    assert len(triangles) == 0
    triangles = bowyer_watson([(10, -6), (13, -6), (-6, -6)])
    assert len(triangles) == 0
    triangles = bowyer_watson([(0, 5), (0, 23), (0, 123456)])
    assert len(triangles) == 0
    triangles = bowyer_watson([(0, -6), (0, -5), (0, -4)])
    assert len(triangles) == 0
    triangles = bowyer_watson([(0, 0), (1, 1), (2, 2)])
    assert len(triangles) == 0
    triangles = bowyer_watson([(1, 1), (0, 0), (20, 20)])
    assert len(triangles) == 0
