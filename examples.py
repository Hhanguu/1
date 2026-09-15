"""
examples.py - Do thi mau dung xuyen suot de tai (10 dinh, 21 canh)
Va cac do thi bo sung de test
"""

from graph import Graph


def create_sample_graph():
    """
    DO THI MAU 10 DINH, 21 CANH - dung xuyen suot bao cao
    Co huong, co trong so
    """
    edges = [
        ("A", "B", 4),
        ("A", "C", 2),
        ("A", "D", 7),
        ("B", "C", 1),
        ("B", "E", 5),
        ("C", "D", 2),
        ("C", "E", 3),
        ("C", "F", 4),
        ("D", "C", 5),
        ("D", "G", 6),
        ("E", "F", 3),
        ("E", "H", 5),
        ("F", "G", 2),
        ("F", "I", 6),
        ("F", "J", 1),
        ("G", "I", 1),
        ("G", "J", 4),
        ("H", "I", 3),
        ("H", "J", 2),
        ("I", "J", 4),
    ]
    return Graph(
        nodes=["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
        edges=edges,
        is_directed=True,
        weighted=True,
    )


def create_eulerian_square():
    edges = [
        ("A", "B", 1),
        ("B", "C", 2),
        ("C", "D", 3),
        ("D", "A", 4),
    ]
    return Graph(
        nodes=["A", "B", "C", "D"],
        edges=edges,
        is_directed=False,
        weighted=True,
    )


def create_small_graph():
    edges = [
        (0, 1, 4), (0, 2, 2), (1, 3, 5),
        (2, 3, 8), (2, 4, 3), (3, 5, 7), (4, 5, 1),
    ]
    return Graph(
        nodes=[0, 1, 2, 3, 4, 5], edges=edges, is_directed=False, weighted=True
    )


def create_small_directed():
    edges = [
        (0, 1, 4), (0, 2, 2), (1, 3, 5), (2, 3, 1),
        (2, 4, 3), (3, 5, 2), (4, 5, 1), (5, 0, 6),
    ]
    return Graph(
        nodes=[0, 1, 2, 3, 4, 5], edges=edges, is_directed=True, weighted=True
    )


def create_20_undirected():
    edges = [
        (0, 1, 4), (0, 2, 8), (0, 3, 5),
        (1, 4, 7), (1, 5, 3), (2, 5, 6), (2, 6, 9),
        (3, 6, 4), (3, 7, 2),
        (4, 8, 5), (4, 9, 1), (5, 9, 8), (5, 10, 3),
        (6, 10, 7), (6, 11, 2),
        (7, 11, 6), (7, 12, 4),
        (8, 13, 9), (9, 13, 5), (9, 14, 2),
        (10, 14, 8), (10, 15, 4),
        (11, 15, 7), (11, 16, 3),
        (12, 16, 6), (12, 17, 8),
        (13, 17, 4), (13, 18, 1),
        (14, 18, 9), (14, 19, 5),
        (15, 19, 7), (16, 19, 2),
        (17, 19, 6), (18, 19, 3),
        (1, 10, 12), (3, 12, 9), (8, 16, 13), (11, 19, 6),
    ]
    return Graph(nodes=list(range(20)), edges=edges, is_directed=False, weighted=True)


def create_20_directed():
    edges = [
        (0, 1, 4), (0, 2, 8), (0, 3, 5),
        (1, 4, 7), (1, 5, 3), (2, 5, 6), (2, 6, 9),
        (3, 6, 4), (3, 7, 2),
        (4, 8, 5), (4, 9, 1), (5, 9, 8), (5, 10, 3),
        (6, 10, 7), (6, 11, 2),
        (7, 11, 6), (7, 12, 4),
        (8, 13, 9), (9, 13, 5), (9, 14, 2),
        (10, 14, 8), (10, 15, 4),
        (11, 15, 7), (11, 16, 3),
        (12, 16, 6), (12, 17, 8),
        (13, 17, 4), (13, 18, 1),
        (14, 18, 9), (14, 19, 5),
        (15, 19, 7), (16, 19, 2),
        (17, 19, 6), (18, 19, 3),
        (5, 1, -2), (10, 6, -3),
    ]
    return Graph(nodes=list(range(20)), edges=edges, is_directed=True, weighted=True)


def create_eulerian_graph():
    edges = [
        (0, 1, 3), (1, 2, 5), (2, 3, 2), (3, 4, 7),
        (4, 5, 4), (5, 6, 8), (6, 7, 6), (7, 8, 3),
        (8, 9, 5), (9, 0, 4),
        (0, 5, 6), (1, 6, 3), (2, 7, 9), (3, 8, 2), (4, 9, 7),
        (0, 3, 5), (1, 4, 8), (2, 5, 4), (6, 8, 7), (7, 9, 3),
    ]
    return Graph(nodes=list(range(10)), edges=edges, is_directed=False, weighted=True)


def create_flow_graph():
    edges = [
        (0, 1, 10), (0, 2, 8), (0, 3, 5),
        (1, 4, 7), (1, 5, 5),
        (2, 4, 3), (2, 5, 6),
        (3, 5, 4), (3, 6, 6),
        (4, 7, 12), (5, 7, 9), (6, 7, 8),
    ]
    nodes = list(range(8))
    g = Graph(nodes=nodes, edges=edges, is_directed=True, weighted=True)
    g._source = 0
    g._sink = 7
    return g
