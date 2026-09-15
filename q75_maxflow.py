"""
module7_maxflow.py - Q7.5: Ford-Fulkerson
Khong su dung bat ky thu vien nao
"""

from graph import Graph
from examples import create_flow_graph



def get_capacity(graph, u, v):
    for nb, w in graph.get_neighbors(u):
        if nb == v:
            return w
    return 0


def bfs_augmenting_path(graph, source, sink, flow):
    visited = {}
    parent = {}
    queue = [source]
    visited[source] = 1

    while len(queue) > 0:
        u = queue.pop(0)
        for v, w in graph.get_neighbors(u):
            residual = w - flow.get((u, v), 0)
            if v not in visited and residual > 0:
                visited[v] = 1
                parent[v] = u
                queue.append(v)
                if v == sink:
                    path = []
                    current = sink
                    while current != source:
                        prev = parent[current]
                        path.append((prev, current))
                        current = prev
                    path.reverse()
                    return path
    return None


def ford_fulkerson(graph, source, sink):
    flow = {}
    max_flow = 0
    step = 0

    while True:
        path = bfs_augmenting_path(graph, source, sink, flow)
        if path is None:
            break
        min_r = 999999999
        for u, v in path:
            r = get_capacity(graph, u, v) - flow.get((u, v), 0)
            if r < min_r:
                min_r = r
        for u, v in path:
            flow[(u, v)] = flow.get((u, v), 0) + min_r
            flow[(v, u)] = flow.get((v, u), 0) - min_r
        max_flow += min_r
        step += 1
        path_str = " -> ".join(str(u) for u, v in path) + " -> " + str(sink)
        print("  Buoc " + str(step) + ": " + path_str + " (+" + str(min_r) + ")")

    return flow, max_flow


def run_module7():
    print("\n" + "=" * 60)
    print("  MODULE 7.5: LUONG TOI DA - FORD-FULKERSON")
    print("=" * 60)

    print("\nChon do thi luong:")
    print("  1. Do thi luong mau (8 dinh)")
    print("  2. Do thi luong nho (7 dinh)")
    choice = input("Chon (1-2): ").strip()

    if choice == "1":
        graph = create_flow_graph()
        source = 0
        sink = 7
    elif choice == "2":
        edges = [(0, 1, 10), (0, 2, 8), (1, 3, 5), (1, 4, 7), (2, 4, 3), (2, 5, 6), (3, 6, 8), (4, 6, 5), (4, 5, 3), (5, 6, 7)]
        graph = Graph(nodes=[0, 1, 2, 3, 4, 5, 6], edges=edges, is_directed=True, weighted=True)
        source = 0
        sink = 6
    else:
        graph = create_flow_graph()
        source = 0
        sink = 7

    graph._source = source
    graph._sink = sink

    print("\nDo thi: " + str(len(graph.nodes)) + " dinh, " + str(len(graph.get_all_edges())) + " canh")
    print("Nguon: " + str(source) + ", Dich: " + str(sink))

    print("\nDung luong cac canh:")
    for u, v, w in graph.get_all_edges():
        print("  " + str(u) + " -> " + str(v) + ": " + str(w))

    print("\n" + "-" * 40)
    print("  FORD-FULKERSON")
    print("-" * 40)

    flow, max_flow = ford_fulkerson(graph, source, sink)
    print("\nLUONG TOI DA: " + str(max_flow))

    print("\nLuong tren moi canh:")
    for u, v, w in graph.get_all_edges():
        f = flow.get((u, v), 0)
        if f > 0:
            print("  " + str(u) + " -> " + str(v) + ": " + str(f) + "/" + str(w))

    cap_dict = {}
    for u, v, w in graph.get_all_edges():
        cap_dict[(u, v)] = w

    hl = [(u, v) for u, v, w in graph.get_all_edges() if flow.get((u, v), 0) > 0]
    graph.draw_graph(
        filename="graph_maxflow.png",
        title="Luong toi da (Ford-Fulkerson)",
        highlight_edges=hl,
    )
    print("  Da luu: graph_maxflow.png")

    print("\n--- Hoan thanh Module 7 ---")


if __name__ == "__main__":
    run_module7()
